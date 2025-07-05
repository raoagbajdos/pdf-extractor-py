"""Command-line interface for PDF extractor."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .extractor import PDFExtractor


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Extract text and tables from PDF files")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Extract text command
    text_parser = subparsers.add_parser("extract-text", help="Extract text from PDF")
    text_parser.add_argument("input", help="Input PDF file path")
    text_parser.add_argument("output", nargs="?", help="Output text file path (optional)")
    
    # Extract tables command
    table_parser = subparsers.add_parser("extract-tables", help="Extract tables from PDF")
    table_parser.add_argument("input", help="Input PDF file path")
    table_parser.add_argument("output_dir", nargs="?", help="Output directory (optional)")
    
    # Extract all command
    all_parser = subparsers.add_parser("extract-all", help="Extract both text and tables")
    all_parser.add_argument("input", help="Input PDF file path")
    all_parser.add_argument("output_dir", nargs="?", help="Output directory (optional)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    extractor = PDFExtractor()
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found")
        sys.exit(1)
    
    try:
        if args.command == "extract-text":
            output_path = args.output if args.output else None
            text = extractor.extract_and_save_text(input_path, output_path)
            output_file = output_path or input_path.with_suffix('.txt')
            print(f"Text extracted and saved to: {output_file}")
            print(f"Extracted {len(text)} characters")
        
        elif args.command == "extract-tables":
            output_dir = args.output_dir if args.output_dir else None
            tables = extractor.extract_and_save_tables(input_path, output_dir)
            print(f"Extracted {len(tables)} tables")
            for i, table in enumerate(tables):
                print(f"Table {i}: {table.shape[0]} rows, {table.shape[1]} columns")
        
        elif args.command == "extract-all":
            output_dir = Path(args.output_dir) if args.output_dir else input_path.parent
            output_dir.mkdir(exist_ok=True)
            
            # Extract text
            text_output = output_dir / f"{input_path.stem}.txt"
            text = extractor.extract_and_save_text(input_path, text_output)
            print(f"Text extracted and saved to: {text_output}")
            print(f"Extracted {len(text)} characters")
            
            # Extract tables
            tables = extractor.extract_and_save_tables(input_path, output_dir)
            print(f"Extracted {len(tables)} tables to: {output_dir}")
            for i, table in enumerate(tables):
                print(f"Table {i}: {table.shape[0]} rows, {table.shape[1]} columns")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()