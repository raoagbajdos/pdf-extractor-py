"""Demonstration script to create legal PDF and show extraction results."""

import sys
from pathlib import Path
import subprocess

# Add the parent directory to Python path to import pdf_extractor
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_extractor import PDFExtractor


def create_legal_pdf_if_needed():
    """Create the legal PDF if reportlab is available."""
    legal_pdf = Path("examples/legal_document_sample.pdf")
    
    if legal_pdf.exists():
        print(f"Legal PDF already exists: {legal_pdf}")
        return legal_pdf
    
    try:
        # Try to run the legal PDF creation script
        result = subprocess.run([sys.executable, "create_legal_sample.py"], 
                              capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        if result.returncode == 0:
            print("Legal PDF created successfully!")
            return legal_pdf
        else:
            print(f"Error creating legal PDF: {result.stderr}")
            return None
    except Exception as e:
        print(f"Could not create legal PDF: {e}")
        print("You'll need to install reportlab: uv add reportlab")
        return None


def demonstrate_extraction():
    """Demonstrate text and table extraction from legal PDF."""
    print("=" * 60)
    print("LEGAL PDF EXTRACTION DEMONSTRATION")
    print("=" * 60)
    
    # Create or find the legal PDF
    legal_pdf = create_legal_pdf_if_needed()
    
    if not legal_pdf or not legal_pdf.exists():
        print("No legal PDF available for demonstration.")
        print("Please run: uv add reportlab && python create_legal_sample.py")
        return
    
    # Initialize extractor
    extractor = PDFExtractor()
    
    print(f"\nProcessing: {legal_pdf}")
    print(f"File size: {legal_pdf.stat().st_size / 1024:.1f} KB")
    
    # Extract text
    print("\n" + "=" * 50)
    print("TEXT EXTRACTION RESULTS")
    print("=" * 50)
    
    try:
        text = extractor.extract_text(legal_pdf)
        print(f"Total characters extracted: {len(text):,}")
        print(f"Total words (approx): {len(text.split()):,}")
        print(f"Total lines: {text.count(chr(10)) + 1:,}")
        
        # Save full text
        text_output = Path("examples/output/legal_document_text.txt")
        text_output.parent.mkdir(exist_ok=True)
        extractor.save_text_to_file(text, text_output)
        print(f"✓ Full text saved to: {text_output}")
        
        # Show text preview
        print("\n--- TEXT PREVIEW (First 500 characters) ---")
        print(text[:500] + "..." if len(text) > 500 else text)
        
        print("\n--- TEXT PREVIEW (Last 300 characters) ---")
        print("..." + text[-300:] if len(text) > 300 else text)
        
    except Exception as e:
        print(f"Error extracting text: {e}")
    
    # Extract tables
    print("\n" + "=" * 50)
    print("TABLE EXTRACTION RESULTS")
    print("=" * 50)
    
    try:
        tables = extractor.extract_tables(legal_pdf)
        print(f"Number of tables found: {len(tables)}")
        
        if not tables:
            print("No tables were extracted. This could be due to:")
            print("- PDF formatting that makes tables hard to detect")
            print("- Missing dependencies (tabula-py requires Java)")
            print("- Tables that are actually formatted as text")
            return
        
        # Process each table
        output_dir = Path("examples/output")
        output_dir.mkdir(exist_ok=True)
        
        for i, table in enumerate(tables):
            print(f"\n--- TABLE {i + 1} ---")
            print(f"Shape: {table.shape[0]} rows × {table.shape[1]} columns")
            print(f"Columns: {list(table.columns)}")
            
            # Show data types
            print("Data types:")
            for col in table.columns:
                dtype = table[col].dtype
                print(f"  {col}: {dtype}")
            
            # Display the table
            print("\n📊 Table Contents:")
            try:
                # Convert to pandas for better display
                df_display = table.to_pandas()
                print(df_display.to_string(index=False, max_rows=10))
                
                if table.shape[0] > 10:
                    print(f"... ({table.shape[0] - 10} more rows)")
                
            except Exception as e:
                print(f"Error displaying table: {e}")
                print("Raw table shape:", table.shape)
            
            # Save in multiple formats
            base_name = f"legal_document_table_{i + 1}"
            
            # Parquet (Polars native format)
            parquet_file = output_dir / f"{base_name}.parquet"
            table.write_parquet(parquet_file)
            print(f"✓ Saved as Parquet: {parquet_file}")
            
            # CSV for easy viewing
            csv_file = output_dir / f"{base_name}.csv"
            table.write_csv(csv_file)
            print(f"✓ Saved as CSV: {csv_file}")
            
            # JSON for structured data
            json_file = output_dir / f"{base_name}.json"
            table.write_json(json_file)
            print(f"✓ Saved as JSON: {json_file}")
            
            # Show file sizes
            print("File sizes:")
            print(f"  Parquet: {parquet_file.stat().st_size:,} bytes")
            print(f"  CSV: {csv_file.stat().st_size:,} bytes") 
            print(f"  JSON: {json_file.stat().st_size:,} bytes")
            
    except Exception as e:
        print(f"Error extracting tables: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 50)
    print("EXTRACTION SUMMARY")
    print("=" * 50)
    print(f"📄 Source: {legal_pdf}")
    print(f"📝 Text extraction: {'✓ Success' if 'text' in locals() else '✗ Failed'}")
    print(f"📊 Tables found: {len(tables) if 'tables' in locals() else 0}")
    print(f"💾 Output directory: {output_dir}")
    
    if output_dir.exists():
        output_files = list(output_dir.glob("legal_document*"))
        print(f"📁 Files created: {len(output_files)}")
        for file in sorted(output_files):
            print(f"   • {file.name}")


if __name__ == "__main__":
    demonstrate_extraction()