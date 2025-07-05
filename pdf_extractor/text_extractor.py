"""Text extraction from PDF files using multiple libraries."""

from pathlib import Path
from typing import Union
import logging

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

logger = logging.getLogger(__name__)


class TextExtractor:
    """Extract text content from PDF files."""
    
    def __init__(self, method: str = "auto") -> None:
        """
        Initialize text extractor.
        
        Args:
            method: Extraction method ("pypdf2", "pdfplumber", or "auto")
        """
        self.method = method
        
        if method == "pypdf2" and PyPDF2 is None:
            raise ImportError("PyPDF2 is required for pypdf2 method")
        elif method == "pdfplumber" and pdfplumber is None:
            raise ImportError("pdfplumber is required for pdfplumber method")
    
    def extract(self, pdf_path: Union[str, Path]) -> str:
        """
        Extract text from PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if self.method == "pypdf2":
            return self._extract_with_pypdf2(pdf_path)
        elif self.method == "pdfplumber":
            return self._extract_with_pdfplumber(pdf_path)
        else:  # auto method
            # Try pdfplumber first (generally better text extraction)
            if pdfplumber is not None:
                try:
                    return self._extract_with_pdfplumber(pdf_path)
                except Exception as e:
                    logger.warning(f"pdfplumber failed: {e}, trying PyPDF2")
            
            # Fallback to PyPDF2
            if PyPDF2 is not None:
                return self._extract_with_pypdf2(pdf_path)
            
            raise ImportError("No PDF processing library available")
    
    def _extract_with_pypdf2(self, pdf_path: Path) -> str:
        """Extract text using PyPDF2."""
        text_content = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(f"--- Page {page_num + 1} ---\n")
                        text_content.append(text)
                        text_content.append("\n\n")
                except Exception as e:
                    logger.warning(f"Error extracting page {page_num + 1}: {e}")
        
        return "".join(text_content)
    
    def _extract_with_pdfplumber(self, pdf_path: Path) -> str:
        """Extract text using pdfplumber."""
        text_content = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                try:
                    text = page.extract_text()
                    if text and text.strip():
                        text_content.append(f"--- Page {page_num + 1} ---\n")
                        text_content.append(text)
                        text_content.append("\n\n")
                except Exception as e:
                    logger.warning(f"Error extracting page {page_num + 1}: {e}")
        
        return "".join(text_content)