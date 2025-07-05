"""Script to create a sample legal PDF with text and tabular data."""

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
except ImportError:
    print("This script requires reportlab: uv add reportlab")
    exit(1)

from pathlib import Path
from datetime import datetime


def create_legal_sample_pdf():
    """Create a comprehensive legal PDF with text and tables."""
    output_path = Path("examples/legal_document_sample.pdf")
    output_path.parent.mkdir(exist_ok=True)
    
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
    print(f"Legal sample PDF created: {output_path}")
    return output_path


if __name__ == "__main__":
    create_legal_sample_pdf()