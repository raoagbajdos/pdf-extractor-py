"""Show expected output format from legal PDF extraction."""

import polars as pl
from pathlib import Path


def show_expected_legal_pdf_output():
    """Display the expected format of extracted data from legal PDF."""
    
    print("=" * 70)
    print("EXPECTED OUTPUT FROM LEGAL PDF EXTRACTION")
    print("=" * 70)
    
    print("\n📄 TEXT EXTRACTION OUTPUT:")
    print("-" * 40)
    
    # Sample text that would be extracted
    sample_text = """--- Page 1 ---
SMITH & ASSOCIATES LAW FIRM
LEGAL SERVICES AGREEMENT & CASE SUMMARY

CLIENT INFORMATION
This Legal Services Agreement ("Agreement") is entered into on March 15, 2024, 
between Smith & Associates Law Firm, a professional corporation ("Firm"), and 
ABC Corporation ("Client"). The Client hereby retains the Firm to provide legal 
services in connection with corporate restructuring, contract negotiations, and 
regulatory compliance matters.

The scope of representation includes but is not limited to: (1) reviewing and 
drafting commercial contracts, (2) providing regulatory compliance advice, 
(3) representing the Client in negotiations with third parties, and (4) general 
corporate legal counsel as requested by the Client.

FEE STRUCTURE
[TABLE DATA WOULD APPEAR HERE]

TERMS AND CONDITIONS: Payment is due within thirty (30) days of invoice date...

--- Page 2 ---
ACTIVE CASES SUMMARY
The following table summarizes all active cases currently being handled by 
Smith & Associates Law Firm...
"""
    
    print(f"Text Length: {len(sample_text):,} characters")
    print(f"Preview:\n{sample_text[:400]}...")
    
    print("\n📊 TABLE EXTRACTION OUTPUT:")
    print("-" * 40)
    
    # Sample Table 1: Fee Structure
    print("\n🔸 TABLE 1: Fee Structure")
    fee_structure = pl.DataFrame({
        "Service Type": ["Senior Partner", "Associate Attorney", "Paralegal Services", "Document Review", "Court Filings"],
        "Attorney": ["John Smith, Esq.", "Sarah Johnson, Esq.", "Mike Davis", "Lisa Wilson", "Various"],
        "Hourly Rate": ["$450.00", "$275.00", "$125.00", "$150.00", "$95.00"],
        "Estimated Hours": ["25", "40", "30", "20", "10"],
        "Total Cost": ["$11,250.00", "$11,000.00", "$3,750.00", "$3,000.00", "$950.00"]
    })
    
    print(f"Shape: {fee_structure.shape[0]} rows × {fee_structure.shape[1]} columns")
    print(f"Columns: {list(fee_structure.columns)}")
    print("\nData Preview:")
    print(fee_structure.to_pandas().to_string(index=False))
    
    # Sample Table 2: Active Cases
    print("\n🔸 TABLE 2: Active Cases")
    active_cases = pl.DataFrame({
        "Case No.": ["2024-001", "2024-002", "2024-003", "2024-004", "2024-005", "2024-006"],
        "Client Name": ["TechCorp Inc.", "Green Energy LLC", "Metro Properties", "DataSafe Systems", "HealthFirst Medical", "AutoParts Direct"],
        "Case Type": ["Contract Dispute", "Regulatory Compliance", "Real Estate Transaction", "IP Infringement", "Employment Law", "Product Liability"],
        "Status": ["Discovery", "Active", "Closing", "Litigation", "Mediation", "Investigation"],
        "Lead Attorney": ["J. Smith", "S. Johnson", "M. Davis", "J. Smith", "L. Wilson", "S. Johnson"],
        "Date Filed": ["2024-01-15", "2024-02-03", "2024-02-20", "2024-03-01", "2024-03-10", "2024-03-12"]
    })
    
    print(f"Shape: {active_cases.shape[0]} rows × {active_cases.shape[1]} columns")
    print(f"Columns: {list(active_cases.columns)}")
    print("\nData Preview:")
    print(active_cases.to_pandas().to_string(index=False))
    
    # Sample Table 3: Billing Summary
    print("\n🔸 TABLE 3: Monthly Billing Summary")
    billing_summary = pl.DataFrame({
        "Week": ["Week 1", "Week 2", "Week 3", "Week 4", "TOTAL"],
        "Billable Hours": ["127.5", "134.0", "142.5", "156.0", "560.0"],
        "Non-Billable": ["23.0", "19.5", "21.0", "24.5", "88.0"],
        "Total Hours": ["150.5", "153.5", "163.5", "180.5", "648.0"],
        "Revenue": ["$31,875.00", "$33,500.00", "$35,625.00", "$39,000.00", "$140,000.00"],
        "Expenses": ["$2,450.00", "$1,890.00", "$3,220.00", "$2,980.00", "$10,540.00"]
    })
    
    print(f"Shape: {billing_summary.shape[0]} rows × {billing_summary.shape[1]} columns")
    print(f"Columns: {list(billing_summary.columns)}")
    print("\nData Preview:")
    print(billing_summary.to_pandas().to_string(index=False))
    
    print("\n💾 CONVERTED FILE FORMATS:")
    print("-" * 40)
    print("📝 Text files:")
    print("   • legal_document_text.txt (UTF-8 encoded)")
    print("\n📊 Table files (each table saved in multiple formats):")
    print("   • legal_document_table_1.parquet (Polars native, compressed)")
    print("   • legal_document_table_1.csv (human-readable)")
    print("   • legal_document_table_1.json (structured data)")
    print("   • legal_document_table_2.parquet")
    print("   • legal_document_table_2.csv") 
    print("   • legal_document_table_2.json")
    print("   • legal_document_table_3.parquet")
    print("   • legal_document_table_3.csv")
    print("   • legal_document_table_3.json")
    
    print("\n🔍 DATA ANALYSIS POSSIBILITIES:")
    print("-" * 40)
    print("With the extracted Polars DataFrames, you can:")
    print("• Filter cases by status: active_cases.filter(pl.col('Status') == 'Active')")
    print("• Calculate total revenue: billing_summary.select(pl.col('Revenue').str.replace('$','').str.replace(',','').cast(pl.Float64).sum())")
    print("• Group cases by attorney: active_cases.group_by('Lead Attorney').count()")
    print("• Analyze billing trends over weeks")
    print("• Export to Excel, database, or other analysis tools")
    
    print("\n✨ BENEFITS OF POLARS FORMAT:")
    print("-" * 40)
    print("• Fast processing (written in Rust)")
    print("• Memory efficient")
    print("• SQL-like operations")
    print("• Easy integration with data science workflows")
    print("• Supports lazy evaluation for large datasets")


def show_sample_analysis():
    """Show sample data analysis with the extracted tables."""
    print("\n" + "=" * 70)
    print("SAMPLE DATA ANALYSIS")
    print("=" * 70)
    
    # Create sample data for analysis
    active_cases = pl.DataFrame({
        "Case No.": ["2024-001", "2024-002", "2024-003", "2024-004", "2024-005", "2024-006"],
        "Client Name": ["TechCorp Inc.", "Green Energy LLC", "Metro Properties", "DataSafe Systems", "HealthFirst Medical", "AutoParts Direct"],
        "Case Type": ["Contract Dispute", "Regulatory Compliance", "Real Estate Transaction", "IP Infringement", "Employment Law", "Product Liability"],
        "Status": ["Discovery", "Active", "Closing", "Litigation", "Mediation", "Investigation"],
        "Lead Attorney": ["J. Smith", "S. Johnson", "M. Davis", "J. Smith", "L. Wilson", "S. Johnson"]
    })
    
    print("\n🔍 Analysis 1: Cases by Status")
    status_analysis = active_cases.group_by("Status").count().sort("count", descending=True)
    print(status_analysis.to_pandas().to_string(index=False))
    
    print("\n🔍 Analysis 2: Cases by Lead Attorney")
    attorney_analysis = active_cases.group_by("Lead Attorney").count().sort("count", descending=True)
    print(attorney_analysis.to_pandas().to_string(index=False))
    
    print("\n🔍 Analysis 3: Filter Active Cases")
    active_only = active_cases.filter(pl.col("Status").is_in(["Active", "Litigation", "Discovery"]))
    print(f"Active cases count: {active_only.height}")
    print(active_only.select(["Case No.", "Client Name", "Status"]).to_pandas().to_string(index=False))


if __name__ == "__main__":
    show_expected_legal_pdf_output()
    show_sample_analysis()