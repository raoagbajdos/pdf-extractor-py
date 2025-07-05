"""Advanced example showing different extraction methods and error handling."""

from pathlib import Path
import logging
from pdf_extractor import PDFExtractor
from pdf_extractor.text_extractor import TextExtractor
from pdf_extractor.table_extractor import TableExtractor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def compare_text_extraction_methods(pdf_path: Path):
    """Compare different text extraction methods."""
    print("\n=== Comparing Text Extraction Methods ===")
    
    methods = ["auto", "pypdf2", "pdfplumber"]
    
    for method in methods:
        try:
            extractor = TextExtractor(method=method)
            text = extractor.extract(pdf_path)
            print(f"{method.upper()}: {len(text)} characters extracted")
            
            # Save for comparison
            output_file = Path(f"examples/output/text_{method}.txt")
            output_file.parent.mkdir(exist_ok=True)
            output_file.write_text(text, encoding='utf-8')
            
        except Exception as e:
            print(f"{method.upper()}: Failed - {e}")


def compare_table_extraction_methods(pdf_path: Path):
    """Compare different table extraction methods."""
    print("\n=== Comparing Table Extraction Methods ===")
    
    methods = ["auto", "tabula", "pdfplumber"]
    
    for method in methods:
        try:
            extractor = TableExtractor(method=method)
            tables = extractor.extract(pdf_path)
            print(f"{method.upper()}: {len(tables)} tables extracted")
            
            for i, table in enumerate(tables):
                print(f"  Table {i + 1}: {table.shape[0]} rows × {table.shape[1]} columns")
                
                # Save for comparison
                output_file = Path(f"examples/output/table_{method}_{i + 1}.parquet")
                output_file.parent.mkdir(exist_ok=True)
                table.write_parquet(output_file)
                
        except Exception as e:
            print(f"{method.upper()}: Failed - {e}")


def batch_processing_example():
    """Example of processing multiple PDF files."""
    print("\n=== Batch Processing Example ===")
    
    extractor = PDFExtractor()
    pdf_dir = Path("examples/sample_pdfs")
    output_dir = Path("examples/batch_output")
    output_dir.mkdir(exist_ok=True)
    
    if not pdf_dir.exists():
        print(f"Sample PDF directory not found: {pdf_dir}")
        print("Please create the directory and add PDF files to process")
        return
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in: {pdf_dir}")
        return
    
    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        
        try:
            # Extract text
            text = extractor.extract_text(pdf_file)
            text_output = output_dir / f"{pdf_file.stem}_text.txt"
            extractor.save_text_to_file(text, text_output)
            print(f"  Text: {len(text)} characters → {text_output}")
            
            # Extract tables
            tables = extractor.extract_tables(pdf_file)
            print(f"  Tables: {len(tables)} found")
            
            for i, table in enumerate(tables):
                table_output = output_dir / f"{pdf_file.stem}_table_{i + 1}.parquet"
                table.write_parquet(table_output)
                print(f"    Table {i + 1}: {table.shape} → {table_output}")
                
        except Exception as e:
            logger.error(f"Error processing {pdf_file}: {e}")


def main():
    """Run advanced examples."""
    sample_pdf = Path("examples/sample_with_tables.pdf")
    
    if sample_pdf.exists():
        compare_text_extraction_methods(sample_pdf)
        compare_table_extraction_methods(sample_pdf)
    else:
        print(f"Sample PDF not found: {sample_pdf}")
        print("Some examples will be skipped")
    
    batch_processing_example()


if __name__ == "__main__":
    main()