# Legal PDF Extraction Demo

This demonstrates how the PDF extractor converts legal documents with both text and tabular data into structured formats.

## Quick Start

### Option 1: See Expected Output (No Dependencies)
```bash
uv run python show_expected_output.py
```
This shows you exactly what the extraction output looks like without needing to create actual PDFs.

### Option 2: Full Demo with Real PDF
```bash
# Install reportlab for PDF creation
uv add reportlab

# Create and extract from legal PDF
uv run python demo_legal_extraction.py
```

### Option 3: Step by Step
```bash
# 1. Create the legal PDF
uv add reportlab
uv run python create_legal_sample.py

# 2. Run extraction
uv run python examples/basic_usage.py
```

## What Gets Extracted

### Text Content
- Legal agreements and contracts
- Case descriptions
- Terms and conditions
- All formatted as clean UTF-8 text

### Tabular Data (as Polars DataFrames)
1. **Fee Structure Table**
   - Service types, attorneys, hourly rates
   - Estimated hours and costs
   
2. **Active Cases Table**
   - Case numbers, client names, case types
   - Status, lead attorneys, filing dates
   
3. **Billing Summary Table**
   - Weekly billable/non-billable hours
   - Revenue and expenses by period

### Output Formats
- **Text**: `.txt` files (UTF-8)
- **Tables**: `.parquet` (Polars native), `.csv` (human-readable), `.json` (structured)

## Sample Legal PDF Content

The generated legal PDF includes:
- Law firm letterhead and contact info
- Legal services agreement text
- Fee structure table with attorney rates
- Active cases summary with case details
- Monthly billing summary with financial data
- Legal disclaimers and confidentiality notices

Perfect for testing extraction of real-world legal document formats!