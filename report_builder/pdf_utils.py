import io
import pandas as pd
from reportlab.platypus import Image, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Image, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import re


def convert_df_to_table(data_object, is_snapshot=False):
    """Convert a pandas DataFrame to a nicely spaced ReportLab Table object."""

    df = data_object.to_frame() if isinstance(data_object, pd.Series) else data_object.copy()

    def format_cell(x):
        if pd.isna(x):
            return ''
        s = str(x)
        max_len = 40 if is_snapshot else 100
        trunc_len = 37 if is_snapshot else 97
        return (s[:trunc_len] + '...') if len(s) > max_len else s

    for col in df.columns:
        df[col] = df[col].map(format_cell)

    data = [df.columns.tolist()] + df.values.tolist()
    num_cols = len(df.columns)

    # Calculate column widths based on content
    available_width = 7.5 * inch
    min_width = 0.6 * inch
    max_width = 2.0 * inch
    avg_char_width = 0.075 * inch

    # Compute widths dynamically with constraints
    max_lengths = [max(len(str(row[i])) for row in data) for i in range(num_cols)]
    col_widths = [min(max(min_width, length * avg_char_width), max_width)
                  for length in max_lengths]

    # Scale widths to fit page width
    total_width = sum(col_widths)
    if total_width:
        scale = available_width / total_width
        col_widths = [w * scale for w in col_widths]

    padding = 4
    table = Table(data, colWidths=col_widths, repeatRows=1)

    # Apply table styling
    style = TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2F4F4F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),

        # Text alignment and wrapping
        ('WORDWRAP', (0, 0), (-1, -1), None),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # Data row fonts
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),

        # Cell padding
        ('TOPPADDING', (0, 0), (-1, -1), padding),
        ('BOTTOMPADDING', (0, 0), (-1, -1), padding),
        ('LEFTPADDING', (0, 0), (-1, -1), padding),
        ('RIGHTPADDING', (0, 0), (-1, -1), padding),

        # Grid and background
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#0e1117')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.white, colors.HexColor('#F5F5F5')])
    ])
    table.setStyle(style)
    return table


def convert_plot_to_image(plot_fig):
    """Converts a Plotly Figure object into a ReportLab Image object."""

    # Export plot as PNG to in-memory buffer
    img_buffer = io.BytesIO()
    plot_fig.write_image(img_buffer, format='png', scale=2)
    img_buffer.seek(0)

    # Create ReportLab Image with standard dimensions
    img = Image(img_buffer, width=5.5*inch, height=3.5*inch)
    return img


def markdown_to_pdf_html(text):
    """
    Convert Markdown formatting to ReportLab HTML tags.
    """
    # Process markdown headers (###) first
    text = re.sub(r'###\s+(.*?)\n', r'<b>\1</b><br/><br/>', text, flags=re.MULTILINE)
    
    # Convert bullet points
    text = re.sub(r'^\s*\*\s+', '&bull; ', text, flags=re.MULTILINE)

    # Convert bold text
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    # Convert italic text
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    
    # Convert newlines to line breaks
    text = text.replace('\n', '<br/>')
    
    return text