"""Example usage of the PDF extractor."""

from pathlib import Path
from pdf_extractor import PDFExtractor


def main():
    """Run example extraction on sample PDF."""
    # Initialize extractor
    extractor = PDFExtractor()
    
    # Try different sample PDFs
    sample_pdfs = [
        Path("examples/legal_document_sample.pdf"),
        Path("examples/sample_with_tables.pdf")
    ]
    
    sample_pdf = None
    for pdf_path in sample_pdfs:
        if pdf_path.exists():
            sample_pdf = pdf_path
            break
    
    if not sample_pdf:
        print("No sample PDF found. Available options:")
        print("1. Run: python create_legal_sample.py (requires: uv add reportlab)")
        print("2. Run: python create_sample_pdf.py (requires: uv add reportlab)")
        print("3. Add your own PDF file to the examples/ directory")
        return
    
    print(f"Processing: {sample_pdf}")
    
    # Extract text
    print("\n=== Extracting Text ===")
    text = extractor.extract_text(sample_pdf)
    print(f"Extracted text length: {len(text)} characters")
    
    # Save text to file
    text_output = Path("examples/output/extracted_text.txt")
    text_output.parent.mkdir(exist_ok=True)
    extractor.save_text_to_file(text, text_output)
    print(f"Text saved to: {text_output}")
    
    # Extract tables
    print("\n=== Extracting Tables ===")
    tables = extractor.extract_tables(sample_pdf)
    print(f"Found {len(tables)} tables")
    
    # Save tables and display info
    output_dir = Path("examples/output")
    output_dir.mkdir(exist_ok=True)
    
    for i, table in enumerate(tables):
        print(f"\nTable {i + 1}:")
        print(f"  Shape: {table.shape[0]} rows × {table.shape[1]} columns")
        print(f"  Columns: {list(table.columns)}")
        
        # Display first few rows
        print("  First 5 rows:")
        print(table.head().to_pandas().to_string(index=False))
        
        # Save as Parquet
        output_file = output_dir / f"table_{i + 1}.parquet"
        table.write_parquet(output_file)
        print(f"  Saved to: {output_file}")
        
        # Also save as CSV for easy viewing
        csv_file = output_dir / f"table_{i + 1}.csv"
        table.write_csv(csv_file)
        print(f"  CSV saved to: {csv_file}")


if __name__ == "__main__":
    main()