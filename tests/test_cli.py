"""Integration tests for the PDF extractor CLI."""

import subprocess
import tempfile
from pathlib import Path
import pytest


class TestCLI:
    """Test cases for the command-line interface."""
    
    def test_cli_help(self):
        """Test CLI help output."""
        result = subprocess.run(
            ["python", "-m", "pdf_extractor.cli", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Extract text and tables from PDF files" in result.stdout
    
    def test_cli_no_command(self):
        """Test CLI with no command provided."""
        result = subprocess.run(
            ["python", "-m", "pdf_extractor.cli"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
    
    def test_cli_extract_text_help(self):
        """Test extract-text command help."""
        result = subprocess.run(
            ["python", "-m", "pdf_extractor.cli", "extract-text", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Extract text from PDF" in result.stdout
    
    def test_cli_extract_tables_help(self):
        """Test extract-tables command help."""
        result = subprocess.run(
            ["python", "-m", "pdf_extractor.cli", "extract-tables", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Extract tables from PDF" in result.stdout
    
    def test_cli_extract_all_help(self):
        """Test extract-all command help."""
        result = subprocess.run(
            ["python", "-m", "pdf_extractor.cli", "extract-all", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Extract both text and tables" in result.stdout
    
    def test_cli_file_not_found(self):
        """Test CLI with non-existent input file."""
        result = subprocess.run(
            ["python", "-m", "pdf_extractor.cli", "extract-text", "nonexistent.pdf"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1
        assert "not found" in result.stderr or "not found" in result.stdout