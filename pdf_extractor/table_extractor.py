"""Table extraction from PDF files and conversion to Polars DataFrames."""

from pathlib import Path
from typing import List, Union
import logging

import polars as pl
import pandas as pd

try:
    import tabula
except ImportError:
    tabula = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

logger = logging.getLogger(__name__)


class TableExtractor:
    """Extract tabular data from PDF files and convert to Polars DataFrames."""
    
    def __init__(self, method: str = "auto") -> None:
        """
        Initialize table extractor.
        
        Args:
            method: Extraction method ("tabula", "pdfplumber", or "auto")
        """
        self.method = method
        
        if method == "tabula" and tabula is None:
            raise ImportError("tabula-py is required for tabula method")
        elif method == "pdfplumber" and pdfplumber is None:
            raise ImportError("pdfplumber is required for pdfplumber method")
    
    def extract(self, pdf_path: Union[str, Path]) -> List[pl.DataFrame]:
        """
        Extract tables from PDF file as Polars DataFrames.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of Polars DataFrames containing table data
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if self.method == "tabula":
            return self._extract_with_tabula(pdf_path)
        elif self.method == "pdfplumber":
            return self._extract_with_pdfplumber(pdf_path)
        else:  # auto method
            # Try tabula first (generally better for complex tables)
            if tabula is not None:
                try:
                    tables = self._extract_with_tabula(pdf_path)
                    if tables:  # If we found tables, return them
                        return tables
                except Exception as e:
                    logger.warning(f"tabula failed: {e}, trying pdfplumber")
            
            # Fallback to pdfplumber
            if pdfplumber is not None:
                return self._extract_with_pdfplumber(pdf_path)
            
            raise ImportError("No table extraction library available")
    
    def _extract_with_tabula(self, pdf_path: Path) -> List[pl.DataFrame]:
        """Extract tables using tabula-py."""
        try:
            # Extract all tables from all pages
            pandas_tables = tabula.read_pdf(
                str(pdf_path), 
                pages='all', 
                multiple_tables=True,
                pandas_options={'header': 0}
            )
            
            # Convert pandas DataFrames to Polars DataFrames
            polars_tables = []
            for i, df in enumerate(pandas_tables):
                if not df.empty:
                    # Clean up the DataFrame
                    df = df.dropna(how='all')  # Remove completely empty rows
                    df = df.dropna(axis=1, how='all')  # Remove completely empty columns
                    
                    if not df.empty:
                        # Convert to Polars
                        polars_df = pl.from_pandas(df)
                        polars_tables.append(polars_df)
            
            return polars_tables
            
        except Exception as e:
            logger.error(f"Error extracting tables with tabula: {e}")
            return []
    
    def _extract_with_pdfplumber(self, pdf_path: Path) -> List[pl.DataFrame]:
        """Extract tables using pdfplumber."""
        polars_tables = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        tables = page.extract_tables()
                        
                        for table_num, table in enumerate(tables):
                            if table and len(table) > 1:  # Must have header + at least one data row
                                # Convert table to pandas DataFrame first
                                df = pd.DataFrame(table[1:], columns=table[0])
                                
                                # Clean up the DataFrame
                                df = df.dropna(how='all')
                                df = df.dropna(axis=1, how='all')
                                
                                if not df.empty:
                                    # Convert to Polars
                                    polars_df = pl.from_pandas(df)
                                    polars_tables.append(polars_df)
                    
                    except Exception as e:
                        logger.warning(f"Error extracting tables from page {page_num + 1}: {e}")
        
        except Exception as e:
            logger.error(f"Error extracting tables with pdfplumber: {e}")
        
        return polars_tables