# PDF Extractor

A Python tool for extracting text and tabular data from PDF files, with support for converting tabular data to Polars DataFrames.

## Features

- Extract text content from PDF files and save to .txt files
- Extract tabular data from PDFs and convert to Polars DataFrames
- Support for multiple PDF processing libraries (PyPDF2, pdfplumber, tabula-py)
- Command-line interface for easy usage
- Comprehensive examples and test samples

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. First, install uv if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install the project dependencies:

```bash
uv sync
```

For development dependencies:

```bash
uv sync --extra dev
```

## Usage

### Command Line Interface

```bash
# Extract text from PDF to .txt file
uv run pdf-extractor extract-text input.pdf output.txt

# Extract tables from PDF to Polars DataFrame
uv run pdf-extractor extract-tables input.pdf output.parquet

# Extract both text and tables
uv run pdf-extractor extract-all input.pdf
```

### Python API

```python
from pdf_extractor import PDFExtractor

# Initialize extractor
extractor = PDFExtractor()

# Extract text
text = extractor.extract_text("document.pdf")
extractor.save_text_to_file(text, "output.txt")

# Extract tables as Polars DataFrames
tables = extractor.extract_tables("document.pdf")
for i, table in enumerate(tables):
    table.write_parquet(f"table_{i}.parquet")
```

## Examples

See the `examples/` directory for sample PDF files and usage examples.

## Development

```bash
# Run tests
uv run pytest

# Format code
uv run black .

# Lint code
uv run ruff check .

# Type checking
uv run mypy .
```

## License

MIT License