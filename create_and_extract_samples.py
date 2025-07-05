"""Complete script to create sample PDFs and demonstrate extraction."""

import sys
from pathlib import Path
import traceback

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️  ReportLab not available. Install with: uv add reportlab")

from datetime import datetime
from pdf_extractor import PDFExtractor


def create_legal_pdf():
    """Create the legal document PDF."""
    if not REPORTLAB_AVAILABLE:
        return None
        
    output_path = Path("examples/legal_document_sample.pdf")
    output_path.parent.mkdir(exist_ok=True)
    
    print("📄 Creating legal document PDF...")
    
    # Create document
    doc = SimpleDocTemplate(str(output_path), pagesize=letter, 
                          topMargin=1*inch, bottomMargin=1*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=20,
        spaceAfter=12
    )
    
    # Document Header
    story.append(Paragraph("SMITH & ASSOCIATES LAW FIRM", title_style))
    story.append(Paragraph("LEGAL SERVICES AGREEMENT & CASE SUMMARY", styles['Heading2']))
    story.append(Spacer(1, 0.3*inch))
    
    # Client Information Section
    story.append(Paragraph("CLIENT INFORMATION", header_style))
    
    client_info_text = """
    This Legal Services Agreement ("Agreement") is entered into on March 15, 2024, 
    between Smith & Associates Law Firm, a professional corporation ("Firm"), and 
    ABC Corporation ("Client"). The Client hereby retains the Firm to provide legal 
    services in connection with corporate restructuring, contract negotiations, and 
    regulatory compliance matters.
    
    The scope of representation includes but is not limited to: (1) reviewing and 
    drafting commercial contracts, (2) providing regulatory compliance advice, 
    (3) representing the Client in negotiations with third parties, and (4) general 
    corporate legal counsel as requested by the Client.
    """
    
    story.append(Paragraph(client_info_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Fee Structure Table
    story.append(Paragraph("FEE STRUCTURE", header_style))
    
    fee_data = [
        ['Service Type', 'Attorney', 'Hourly Rate', 'Estimated Hours', 'Total Cost'],
        ['Senior Partner', 'John Smith, Esq.', '$450.00', '25', '$11,250.00'],
        ['Associate Attorney', 'Sarah Johnson, Esq.', '$275.00', '40', '$11,000.00'],
        ['Paralegal Services', 'Mike Davis', '$125.00', '30', '$3,750.00'],
        ['Document Review', 'Lisa Wilson', '$150.00', '20', '$3,000.00'],
        ['Court Filings', 'Various', '$95.00', '10', '$950.00'],
        ['', '', '', 'TOTAL:', '$29,950.00']
    ]
    
    fee_table = Table(fee_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
    fee_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.lightblue),
        ('BACKGROUND', (0, -1), (-1, -1), colors.yellow),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('SPAN', (0, -1), (3, -1)),
    ]))
    
    story.append(fee_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Terms and Conditions
    terms_text = """
    TERMS AND CONDITIONS: Payment is due within thirty (30) days of invoice date. 
    A retainer of $10,000.00 is required before commencement of work. The Client 
    agrees to cooperate fully with the Firm and provide all necessary documents 
    and information. This Agreement shall be governed by the laws of the State 
    of California.
    """
    
    story.append(Paragraph(terms_text, styles['Normal']))
    story.append(PageBreak())
    
    # Case Summary Section
    story.append(Paragraph("ACTIVE CASES SUMMARY", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    case_summary_text = """
    The following table summarizes all active cases currently being handled by 
    Smith & Associates Law Firm. Each case is assigned a unique case number and 
    is tracked for billing and progress monitoring purposes. The status indicates 
    the current phase of litigation or legal proceedings.
    """
    
    story.append(Paragraph(case_summary_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Active Cases Table
    story.append(Paragraph("ACTIVE CASES", header_style))
    
    cases_data = [
        ['Case No.', 'Client Name', 'Case Type', 'Status', 'Lead Attorney', 'Date Filed'],
        ['2024-001', 'TechCorp Inc.', 'Contract Dispute', 'Discovery', 'J. Smith', '2024-01-15'],
        ['2024-002', 'Green Energy LLC', 'Regulatory Compliance', 'Active', 'S. Johnson', '2024-02-03'],
        ['2024-003', 'Metro Properties', 'Real Estate Transaction', 'Closing', 'M. Davis', '2024-02-20'],
        ['2024-004', 'DataSafe Systems', 'IP Infringement', 'Litigation', 'J. Smith', '2024-03-01'],
        ['2024-005', 'HealthFirst Medical', 'Employment Law', 'Mediation', 'L. Wilson', '2024-03-10'],
        ['2024-006', 'AutoParts Direct', 'Product Liability', 'Investigation', 'S. Johnson', '2024-03-12']
    ]
    
    cases_table = Table(cases_data, colWidths=[0.8*inch, 1.2*inch, 1.2*inch, 1*inch, 1*inch, 0.8*inch])
    cases_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(cases_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Billing Summary Table
    story.append(Paragraph("MONTHLY BILLING SUMMARY - MARCH 2024", header_style))
    
    billing_data = [
        ['Week', 'Billable Hours', 'Non-Billable', 'Total Hours', 'Revenue', 'Expenses'],
        ['Week 1', '127.5', '23.0', '150.5', '$31,875.00', '$2,450.00'],
        ['Week 2', '134.0', '19.5', '153.5', '$33,500.00', '$1,890.00'],
        ['Week 3', '142.5', '21.0', '163.5', '$35,625.00', '$3,220.00'],
        ['Week 4', '156.0', '24.5', '180.5', '$39,000.00', '$2,980.00'],
        ['TOTAL', '560.0', '88.0', '648.0', '$140,000.00', '$10,540.00']
    ]
    
    billing_table = Table(billing_data)
    billing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.lavender),
        ('BACKGROUND', (0, -1), (-1, -1), colors.orange),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(billing_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Footer text
    footer_text = """
    This document contains confidential and privileged information protected by 
    attorney-client privilege. Any unauthorized disclosure or distribution of this 
    document is strictly prohibited. For questions regarding this agreement or 
    billing matters, please contact our office at (555) 123-4567.
    
    Document prepared on: """ + datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    story.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"✓ Legal PDF created: {output_path}")
    return output_path


def create_business_report_pdf():
    """Create a business report PDF with different table types."""
    if not REPORTLAB_AVAILABLE:
        return None
        
    output_path = Path("examples/business_report_sample.pdf")
    output_path.parent.mkdir(exist_ok=True)
    
    print("📄 Creating business report PDF...")
    
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    story.append(Paragraph("QUARTERLY BUSINESS REPORT", styles['Title']))
    story.append(Spacer(1, 0.5*inch))
    
    # Executive Summary
    exec_summary = """
    This quarterly report provides a comprehensive overview of our company's 
    performance for Q1 2024. Key highlights include revenue growth of 15%, 
    expansion into new markets, and successful product launches. The following 
    sections detail our financial performance, sales metrics, and operational 
    achievements.
    """
    story.append(Paragraph(exec_summary, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Financial Performance Table
    story.append(Paragraph("FINANCIAL PERFORMANCE", styles['Heading2']))
    
    financial_data = [
        ['Metric', 'Q1 2023', 'Q4 2023', 'Q1 2024', 'YoY Change'],
        ['Revenue', '$2.1M', '$2.8M', '$2.4M', '+14.3%'],
        ['Gross Profit', '$1.3M', '$1.7M', '$1.5M', '+15.4%'],
        ['Operating Expenses', '$0.9M', '$1.1M', '$1.0M', '+11.1%'],
        ['Net Income', '$0.4M', '$0.6M', '$0.5M', '+25.0%'],
        ['EBITDA', '$0.5M', '$0.7M', '$0.6M', '+20.0%']
    ]
    
    financial_table = Table(financial_data)
    financial_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(financial_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Regional Sales Table
    story.append(Paragraph("REGIONAL SALES BREAKDOWN", styles['Heading2']))
    
    sales_data = [
        ['Region', 'Q1 Sales', 'Target', 'Achievement', 'Top Product'],
        ['North America', '$850,000', '$800,000', '106.3%', 'Product A'],
        ['Europe', '$650,000', '$700,000', '92.9%', 'Product B'],
        ['Asia Pacific', '$720,000', '$650,000', '110.8%', 'Product C'],
        ['Latin America', '$180,000', '$200,000', '90.0%', 'Product A'],
        ['TOTAL', '$2,400,000', '$2,350,000', '102.1%', '-']
    ]
    
    sales_table = Table(sales_data)
    sales_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.lightpink),
        ('BACKGROUND', (0, -1), (-1, -1), colors.gold),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(sales_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Employee Data Table
    story.append(Paragraph("WORKFORCE SUMMARY", styles['Heading2']))
    
    workforce_data = [
        ['Department', 'Headcount', 'New Hires', 'Departures', 'Net Change'],
        ['Engineering', '45', '8', '2', '+6'],
        ['Sales & Marketing', '28', '5', '3', '+2'],
        ['Operations', '22', '3', '1', '+2'],
        ['Finance & Admin', '15', '1', '2', '-1'],
        ['Customer Success', '12', '4', '0', '+4'],
        ['TOTAL', '122', '21', '8', '+13']
    ]
    
    workforce_table = Table(workforce_data)
    workforce_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.lightgreen),
        ('BACKGROUND', (0, -1), (-1, -1), colors.yellow),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(workforce_table)
    
    doc.build(story)
    print(f"✓ Business report PDF created: {output_path}")
    return output_path


def extract_and_convert_pdf(pdf_path, description):
    """Extract text and tables from a PDF and save in multiple formats."""
    if not pdf_path or not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return
    
    print(f"\n🔍 Extracting from {description}: {pdf_path.name}")
    print("=" * 60)
    
    extractor = PDFExtractor()
    output_dir = Path("examples/output")
    output_dir.mkdir(exist_ok=True)
    
    # Extract text
    try:
        text = extractor.extract_text(pdf_path)
        print(f"📝 Text extracted: {len(text):,} characters")
        
        # Save text
        text_file = output_dir / f"{pdf_path.stem}_text.txt"
        extractor.save_text_to_file(text, text_file)
        print(f"   💾 Saved: {text_file}")
        
        # Show text preview
        print(f"   📖 Preview: {text[:200]}...")
        
    except Exception as e:
        print(f"❌ Text extraction failed: {e}")
    
    # Extract tables
    try:
        tables = extractor.extract_tables(pdf_path)
        print(f"📊 Tables extracted: {len(tables)}")
        
        if tables:
            for i, table in enumerate(tables):
                print(f"\n   📋 Table {i+1}: {table.shape[0]} rows × {table.shape[1]} columns")
                print(f"      Columns: {list(table.columns)}")
                
                # Save in multiple formats
                base_name = f"{pdf_path.stem}_table_{i+1}"
                
                # Parquet
                parquet_file = output_dir / f"{base_name}.parquet"
                table.write_parquet(parquet_file)
                
                # CSV
                csv_file = output_dir / f"{base_name}.csv"
                table.write_csv(csv_file)
                
                # JSON
                json_file = output_dir / f"{base_name}.json"
                table.write_json(json_file)
                
                print(f"      💾 Saved: {parquet_file.name}, {csv_file.name}, {json_file.name}")
                
                # Show preview
                if table.height > 0:
                    print("      📖 Preview:")
                    df_preview = table.head(3).to_pandas()
                    print("         " + df_preview.to_string(index=False).replace('\n', '\n         '))
        else:
            print("   ⚠️  No tables detected (this might be due to formatting or missing dependencies)")
            
    except Exception as e:
        print(f"❌ Table extraction failed: {e}")
        traceback.print_exc()


def main():
    """Create sample PDFs and demonstrate extraction."""
    print("🚀 PDF EXTRACTOR DEMONSTRATION")
    print("=" * 60)
    
    # Create output directory
    Path("examples/output").mkdir(exist_ok=True)
    
    # Create sample PDFs
    pdfs_created = []
    
    legal_pdf = create_legal_pdf()
    if legal_pdf:
        pdfs_created.append((legal_pdf, "Legal Document"))
    
    business_pdf = create_business_report_pdf()
    if business_pdf:
        pdfs_created.append((business_pdf, "Business Report"))
    
    if not pdfs_created:
        print("❌ Could not create PDFs. Install reportlab: uv add reportlab")
        return
    
    print(f"\n✅ Created {len(pdfs_created)} sample PDFs")
    
    # Extract and convert each PDF
    for pdf_path, description in pdfs_created:
        extract_and_convert_pdf(pdf_path, description)
    
    # Summary
    print(f"\n🎉 EXTRACTION COMPLETE")
    print("=" * 60)
    output_dir = Path("examples/output")
    if output_dir.exists():
        files = list(output_dir.glob("*"))
        print(f"📁 Output files created: {len(files)}")
        for file in sorted(files):
            size_kb = file.stat().st_size / 1024
            print(f"   • {file.name} ({size_kb:.1f} KB)")
    
    print(f"\n💡 Next steps:")
    print("   • Check examples/output/ for converted files")
    print("   • Open .csv files to view table data")
    print("   • Use .parquet files for data analysis with Polars")
    print("   • Read .txt files for extracted text content")


if __name__ == "__main__":
    main()