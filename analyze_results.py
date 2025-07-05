#!/usr/bin/env python3
"""
Demonstrate PDF extraction and Polars DataFrame analysis capabilities.
"""

import polars as pl
from pathlib import Path
from pdf_extractor import PDFExtractor


def analyze_extracted_data():
    """Analyze the extracted data to demonstrate capabilities."""
    
    print("🎯 PDF EXTRACTION AND ANALYSIS DEMONSTRATION")
    print("=" * 60)
    
    # Load the extracted tables
    output_dir = Path("examples/output")
    
    if not output_dir.exists():
        print("❌ No extracted data found. Please run basic_usage.py first.")
        return
    
    # Load tables as Polars DataFrames
    table_files = list(output_dir.glob("table_*.parquet"))
    if not table_files:
        print("❌ No table files found. Please run basic_usage.py first.")
        return
    
    print(f"📊 Found {len(table_files)} extracted tables")
    print()
    
    # Analyze Table 3 (Billing Summary)
    billing_file = output_dir / "table_3.parquet"
    if billing_file.exists():
        print("💰 BILLING ANALYSIS (Table 3)")
        print("-" * 40)
        
        # Load the billing data
        billing_df = pl.read_parquet(billing_file)
        print("Raw data:")
        print(billing_df)
        print()
        
        # Clean and analyze the data
        # Remove the TOTAL row for calculations
        billing_clean = billing_df.filter(pl.col("Week") != "TOTAL")
        
        print("📈 FINANCIAL INSIGHTS:")
        
        # Calculate averages
        avg_billable = billing_clean.select(pl.col("Billable Hours").mean()).item()
        avg_revenue = billing_clean.select(
            pl.col("Revenue").str.replace_all(r"[$,]", "").cast(pl.Float64).mean()
        ).item()
        
        print(f"• Average weekly billable hours: {avg_billable:.1f}")
        print(f"• Average weekly revenue: ${avg_revenue:,.2f}")
        
        # Find best performing week
        best_week = billing_clean.with_columns(
            pl.col("Revenue").str.replace_all(r"[$,]", "").cast(pl.Float64).alias("revenue_numeric")
        ).sort("revenue_numeric", descending=True).select("Week").item(0, 0)
        
        print(f"• Best performing week: {best_week}")
        print()
    
    # Analyze Table 2 (Active Cases)
    cases_file = output_dir / "table_2.parquet"
    if cases_file.exists():
        print("⚖️  CASE ANALYSIS (Table 2)")
        print("-" * 40)
        
        cases_df = pl.read_parquet(cases_file)
        print("Raw data:")
        print(cases_df)
        print()
        
        print("📋 CASE INSIGHTS:")
        
        # Count cases by status
        if "Status" in cases_df.columns:
            status_counts = cases_df.group_by("Status").count().sort("count", descending=True)
            print("• Cases by status:")
            for row in status_counts.rows():
                print(f"  - {row[0]}: {row[1]} case(s)")
        
        # Count cases by attorney
        if "Lead Attorney" in cases_df.columns:
            attorney_counts = cases_df.group_by("Lead Attorney").count().sort("count", descending=True)
            print("• Cases by attorney:")
            for row in attorney_counts.rows():
                print(f"  - {row[0]}: {row[1]} case(s)")
        
        print()
    
    # Show data transformation capabilities
    print("🔄 DATA TRANSFORMATION EXAMPLES")
    print("-" * 40)
    
    if billing_file.exists():
        billing_df = pl.read_parquet(billing_file)
        
        # Create a cleaned version with numeric columns
        transformed_df = billing_df.filter(pl.col("Week") != "TOTAL").with_columns([
            pl.col("Revenue").str.replace_all(r"[$,]", "").cast(pl.Float64).alias("revenue_numeric"),
            pl.col("Expenses").str.replace_all(r"[$,]", "").cast(pl.Float64).alias("expenses_numeric"),
            pl.col("Billable Hours").cast(pl.Float64),
            pl.col("Non-Billable").cast(pl.Float64)
        ]).with_columns([
            (pl.col("revenue_numeric") - pl.col("expenses_numeric")).alias("net_profit"),
            (pl.col("revenue_numeric") / pl.col("Billable Hours")).alias("revenue_per_hour")
        ])
        
        print("✨ Enhanced billing data with calculated fields:")
        print(transformed_df.select([
            "Week", "Billable Hours", "revenue_numeric", "expenses_numeric", 
            "net_profit", "revenue_per_hour"
        ]))
        print()
    
    # Show export capabilities
    print("💾 EXPORT CAPABILITIES")
    print("-" * 40)
    print("The extracted data can be exported to:")
    print("• CSV files (human-readable)")
    print("• Parquet files (efficient binary format)")
    print("• JSON files (web-friendly)")
    print("• Excel files (with pl.write_excel())")
    print("• Database tables (with connectors)")
    print("• Analysis platforms (pandas, numpy, etc.)")
    print()
    
    print("🎉 SUMMARY")
    print("-" * 40)
    print("✅ PDF successfully extracted to structured data")
    print("✅ Text content preserved with page breaks")
    print("✅ Tables converted to Polars DataFrames")
    print("✅ Data ready for analysis and reporting")
    print("✅ Multiple export formats available")
    print("✅ Fast processing with Polars")


if __name__ == "__main__":
    analyze_extracted_data()
