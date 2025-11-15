import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

# Import your *own* modules
from .pdf_utils import convert_df_to_table, convert_plot_to_image ,markdown_to_pdf_html
from agent_logic.analysis_agent import get_professionnal_title


def build_pdf_report(dataset_name, main_overview , data_head , report_cart):
    """Builds a PDF report from the provided components."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.75*inch, bottomMargin=0.75*inch,title=f"Data Analysis Report - {dataset_name}")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='AnalysisText', parent=styles['Normal'], fontSize=12, alignment=TA_JUSTIFY, spaceAfter=6))

    # Customize styles for better readability
    styles['h1'].fontSize = 20
    styles['h1'].spaceAfter = 14 
    styles['h2'].fontSize = 16
    styles['h2'].spaceAfter = 12
    styles['Normal'].fontSize = 12
    styles['Normal'].leading = 12
    
    story = []

    story.append(Paragraph("Data Analysis Report", styles['h1']))
    
    story.append(Paragraph(f"Dataset: {dataset_name}", styles['h2']))
    story.append(Paragraph(markdown_to_pdf_html(main_overview), styles['Normal']))
    story.append(Spacer(1, 0.15*inch))  # Reduced space
    
    story.append(Paragraph("Initial Data Snapshot:", styles['h2']))
    # For data snapshot, we'll use a special compact table style
    story.append(convert_df_to_table(data_head, is_snapshot=True))
    story.append(Spacer(1, 0.15*inch))  # Reduced space

    story.append(Paragraph("Detailed Analysis", styles['h1']))
    for item in report_cart:
        # Get a professional title from our new agent
        title = get_professionnal_title(item['query'])
        story.append(Paragraph(title, styles['h2']))
        
        if item['type'] == 'plot':
            img = convert_plot_to_image(item['result'])
            if img:
                story.append(img)
                
        elif item['type'] == 'data':
            # Use the same compact table style for all tables
            tbl = convert_df_to_table(item['result'], is_snapshot=True)
            story.append(tbl)
            
        elif item['type'] == 'value':
            value_text = str(item['result'])
            story.append(Paragraph(value_text, styles['Normal']))
        
        story.append(Spacer(1, 0.15*inch))
        analysis_html = markdown_to_pdf_html(item['analysis'])
        story.append(Paragraph(analysis_html, styles['AnalysisText']))
        story.append(Spacer(1, 0.25*inch))

    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
