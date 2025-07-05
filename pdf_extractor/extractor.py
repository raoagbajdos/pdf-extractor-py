"""Main PDF extractor class that combines text and table extraction."""

from pathlib import Path
from typing import List, Optional, Union
import polars as pl

from .text_extractor import TextExtractor
from .table_extractor import TableExtractor


class PDFExtractor:
    """Main class for extracting text and tabular data from PDF files."""
    
    def __init__(self) -> None:
        """Initialize the PDF extractor with text and table extractors."""
        self.text_extractor = TextExtractor()
        self.table_extractor = TableExtractor()
    
    def extract_text(self, pdf_path: Union[str, Path]) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content as string
        """
        return self.text_extractor.extract(pdf_path)
    
    def extract_tables(self, pdf_path: Union[str, Path]) -> List[pl.DataFrame]:
        """
        Extract tabular data from a PDF file as Polars DataFrames.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of Polars DataFrames containing table data
        """
        return self.table_extractor.extract(pdf_path)
    
    def save_text_to_file(self, text: str, output_path: Union[str, Path]) -> None:
        """
        Save extracted text to a .txt file.
        
        Args:
            text: Text content to save
            output_path: Output file path
        """
        output_path = Path(output_path)
        output_path.write_text(text, encoding='utf-8')
    
    def extract_and_save_text(
        self, 
        pdf_path: Union[str, Path], 
        output_path: Optional[Union[str, Path]] = None
    ) -> str:
        """
        Extract text from PDF and save to file.
        
        Args:
            pdf_path: Path to the PDF file
            output_path: Output file path (optional, defaults to PDF name with .txt extension)
            
        Returns:
            Extracted text content
        """
        text = self.extract_text(pdf_path)
        
        if output_path is None:
            pdf_path = Path(pdf_path)
            output_path = pdf_path.with_suffix('.txt')
        
        self.save_text_to_file(text, output_path)
        return text
    
    def extract_and_save_tables(
        self, 
        pdf_path: Union[str, Path], 
        output_dir: Optional[Union[str, Path]] = None
    ) -> List[pl.DataFrame]:
        """
        Extract tables from PDF and save as Parquet files.
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Output directory (optional, defaults to PDF directory)
            
        Returns:
            List of extracted Polars DataFrames
        """
        tables = self.extract_tables(pdf_path)
        
        if output_dir is None:
            pdf_path = Path(pdf_path)
            output_dir = pdf_path.parent
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        pdf_name = Path(pdf_path).stem
        
        for i, table in enumerate(tables):
            output_file = output_dir / f"{pdf_name}_table_{i}.parquet"
            table.write_parquet(output_file)
        
        return tables