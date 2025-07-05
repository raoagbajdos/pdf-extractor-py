"""Simple script to create a sample PDF with tables for testing."""

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
except ImportError:
    print("This script requires reportlab: pip install reportlab")
    exit(1)

from pathlib import Path


def create_sample_pdf():
    """Create a sample PDF with text and tables."""
    output_path = Path("examples/sample_with_tables.pdf")
    output_path.parent.mkdir(exist_ok=True)
    
    # Create document
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Add title
    title = Paragraph("Sample Document with Tables", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.5*inch))
    
    # Add introduction text
    intro = Paragraph(
        "This is a sample PDF document created for testing the PDF extractor. "
        "It contains both regular text content and tabular data that can be "
        "extracted and converted to Polars DataFrames.",
        styles['Normal']
    )
    story.append(intro)
    story.append(Spacer(1, 0.3*inch))
    
    # Add first table - Sales Data
    story.append(Paragraph("Sales Data Q1 2024", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    sales_data = [
        ['Month', 'Product A', 'Product B', 'Product C', 'Total'],
        ['January', '$12,500', '$8,300', '$15,700', '$36,500'],
        ['February', '$14,200', '$9,100', '$16,800', '$40,100'],
        ['March', '$13,800', '$8,900', '$17,200', '$39,900'],
        ['Total', '$40,500', '$26,300', '$49,700', '$116,500']
    ]
    
    sales_table = Table(sales_data)
    sales_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(sales_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Add some more text
    middle_text = Paragraph(
        "The sales data above shows consistent performance across all products. "
        "Product C has been the top performer, while Product B shows room for improvement. "
        "Below is employee information for the sales team.",
        styles['Normal']
    )
    story.append(middle_text)
    story.append(Spacer(1, 0.3*inch))
    
    # Add second table - Employee Data
    story.append(Paragraph("Sales Team Information", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    employee_data = [
        ['Employee ID', 'Name', 'Department', 'Start Date', 'Salary'],
        ['EMP001', 'John Smith', 'Sales', '2020-01-15', '$65,000'],
        ['EMP002', 'Sarah Johnson', 'Sales', '2019-03-22', '$68,000'],
        ['EMP003', 'Mike Davis', 'Sales', '2021-07-10', '$62,000'],
        ['EMP004', 'Lisa Wilson', 'Sales', '2020-11-05', '$66,500'],
        ['EMP005', 'Tom Brown', 'Sales Manager', '2018-09-12', '$85,000']
    ]
    
    employee_table = Table(employee_data)
    employee_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(employee_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Add conclusion
    conclusion = Paragraph(
        "This document demonstrates the extraction capabilities of the PDF extractor tool. "
        "The text content can be extracted to .txt files, while the tabular data can be "
        "converted to Polars DataFrames for further analysis and processing.",
        styles['Normal']
    )
    story.append(conclusion)
    
    # Build PDF
    doc.build(story)
    print(f"Sample PDF created: {output_path}")


if __name__ == "__main__":
    create_sample_pdf()