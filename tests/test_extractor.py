"""Tests for the PDF extractor package."""

import pytest
from pathlib import Path
import tempfile
from unittest.mock import Mock, patch

from pdf_extractor import PDFExtractor
from pdf_extractor.text_extractor import TextExtractor
from pdf_extractor.table_extractor import TableExtractor


class TestTextExtractor:
    """Test cases for TextExtractor."""
    
    def test_init_with_valid_method(self):
        """Test TextExtractor initialization with valid methods."""
        extractor = TextExtractor(method="auto")
        assert extractor.method == "auto"
    
    def test_init_with_invalid_method(self):
        """Test TextExtractor initialization with unsupported method."""
        with patch('pdf_extractor.text_extractor.PyPDF2', None):
            with pytest.raises(ImportError):
                TextExtractor(method="pypdf2")
    
    def test_extract_file_not_found(self):
        """Test extraction with non-existent file."""
        extractor = TextExtractor()
        with pytest.raises(FileNotFoundError):
            extractor.extract("nonexistent.pdf")
    
    @patch('pdf_extractor.text_extractor.pdfplumber')
    def test_extract_with_pdfplumber(self, mock_pdfplumber):
        """Test extraction using pdfplumber."""
        # Mock pdfplumber behavior
        mock_pdf = Mock()
        mock_page = Mock()
        mock_page.extract_text.return_value = "Sample text"
        mock_pdf.pages = [mock_page]
        mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf
        
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            extractor = TextExtractor(method="pdfplumber")
            result = extractor.extract(tmp.name)
            
            assert "Sample text" in result
            assert "--- Page 1 ---" in result


class TestTableExtractor:
    """Test cases for TableExtractor."""
    
    def test_init_with_valid_method(self):
        """Test TableExtractor initialization."""
        extractor = TableExtractor(method="auto")
        assert extractor.method == "auto"
    
    def test_extract_file_not_found(self):
        """Test extraction with non-existent file."""
        extractor = TableExtractor()
        with pytest.raises(FileNotFoundError):
            extractor.extract("nonexistent.pdf")
    
    @patch('pdf_extractor.table_extractor.tabula')
    @patch('pdf_extractor.table_extractor.pl')
    def test_extract_with_tabula(self, mock_pl, mock_tabula):
        """Test table extraction using tabula."""
        # Mock tabula behavior
        import pandas as pd
        mock_df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        mock_tabula.read_pdf.return_value = [mock_df]
        
        # Mock polars conversion
        mock_polars_df = Mock()
        mock_pl.from_pandas.return_value = mock_polars_df
        
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            extractor = TableExtractor(method="tabula")
            result = extractor.extract(tmp.name)
            
            assert len(result) == 1
            assert result[0] == mock_polars_df


class TestPDFExtractor:
    """Test cases for PDFExtractor."""
    
    def test_init(self):
        """Test PDFExtractor initialization."""
        extractor = PDFExtractor()
        assert isinstance(extractor.text_extractor, TextExtractor)
        assert isinstance(extractor.table_extractor, TableExtractor)
    
    def test_save_text_to_file(self):
        """Test saving text to file."""
        extractor = PDFExtractor()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt") as tmp:
            tmp_path = Path(tmp.name)
        
        try:
            extractor.save_text_to_file("test content", tmp_path)
            content = tmp_path.read_text(encoding='utf-8')
            assert content == "test content"
        finally:
            tmp_path.unlink()
    
    @patch.object(TextExtractor, 'extract')
    def test_extract_text(self, mock_extract):
        """Test text extraction delegation."""
        mock_extract.return_value = "extracted text"
        
        extractor = PDFExtractor()
        result = extractor.extract_text("dummy.pdf")
        
        assert result == "extracted text"
        mock_extract.assert_called_once_with("dummy.pdf")
    
    @patch.object(TableExtractor, 'extract')
    def test_extract_tables(self, mock_extract):
        """Test table extraction delegation."""
        mock_tables = [Mock(), Mock()]
        mock_extract.return_value = mock_tables
        
        extractor = PDFExtractor()
        result = extractor.extract_tables("dummy.pdf")
        
        assert result == mock_tables
        mock_extract.assert_called_once_with("dummy.pdf")


@pytest.fixture
def sample_pdf_content():
    """Fixture providing sample PDF content for testing."""
    return "Sample PDF content for testing"


@pytest.fixture
def temp_pdf_file():
    """Fixture providing a temporary PDF file."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    yield tmp_path
    
    # Cleanup
    if tmp_path.exists():
        tmp_path.unlink()