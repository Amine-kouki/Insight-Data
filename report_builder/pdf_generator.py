import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

# Import project modules
from .pdf_utils import convert_df_to_table, convert_plot_to_image, markdown_to_pdf_html
from agent_logic.analysis_agent import get_professionnal_title


def build_pdf_report(dataset_name, main_overview , data_head , report_cart):
    """Builds a PDF report from the provided components."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.75*inch, bottomMargin=0.75*inch,title=f"Data Analysis Report - {dataset_name}")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='MainTitle',
        parent=styles['h1'],
        fontName='Times-Bold',  
        fontSize=22,
        spaceAfter=14
    ))
    styles.add(ParagraphStyle(
        name='SectionTitle',
        parent=styles['h2'],
        fontName='Times-Bold', 
        fontSize=16,
        spaceAfter=8
    ))
    

    body_style = styles['BodyText']
    body_style.fontName = 'Times-Roman'
    body_style.fontSize = 14
    body_style.leading = 17.5
    body_style.alignment = TA_JUSTIFY
    body_style.spaceAfter = 12

    styles.add(ParagraphStyle(
        name='AnalysisText',
        parent=styles['Normal'],
        fontName='Times-Roman', 
        fontSize=14,           
        leading=17.5,             
        alignment=TA_JUSTIFY,
        spaceAfter=12
    ))
    
    story = []

    story.append(Paragraph("Data Analysis Report", styles['MainTitle']))
    
    story.append(Paragraph(f"Dataset: {dataset_name}", styles['SectionTitle']))
    story.append(Paragraph(markdown_to_pdf_html(main_overview), styles['AnalysisText']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("Initial Data Snapshot:", styles['AnalysisText']))
    story.append(convert_df_to_table(data_head, is_snapshot=True))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("Detailed Analysis", styles['h1']))
    for item in report_cart:
        # Generate section title from query
        title = get_professionnal_title(item['query'])
        story.append(Paragraph(title, styles['SectionTitle']))
        
        if item['type'] == 'plot':
            img = convert_plot_to_image(item['result'])
            if img:
                story.append(img)
                
        elif item['type'] == 'data':
            tbl = convert_df_to_table(item['result'], is_snapshot=True)
            story.append(tbl)
            
        elif item['type'] == 'value':
            value_text = str(item['result'])
            story.append(Paragraph(value_text, styles['BodyText']))
        
        story.append(Spacer(1, 0.15*inch))
        analysis_html = markdown_to_pdf_html(item['analysis'])
        story.append(Paragraph(analysis_html, styles['AnalysisText']))
        story.append(Spacer(1, 0.25*inch))

    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
