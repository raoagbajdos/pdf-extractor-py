#!/bin/bash

# Setup script for PDF Extractor project

echo "Setting up PDF Extractor project..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "UV is not installed. Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.bashrc
fi

# Install dependencies
echo "Installing dependencies..."
uv sync

# Install development dependencies
echo "Installing development dependencies..."
uv sync --extra dev

# Create output directories
echo "Creating output directories..."
mkdir -p examples/output
mkdir -p examples/sample_pdfs

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add PDF files to examples/sample_pdfs/ for testing"
echo "2. Run examples: uv run python examples/basic_usage.py"
echo "3. Run tests: uv run pytest"
echo "4. Use CLI: uv run pdf-extractor --help"