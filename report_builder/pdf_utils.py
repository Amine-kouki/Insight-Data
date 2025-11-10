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

    # --- width logic ---
    available_width = 7.5 * inch
    min_width = 0.6 * inch   # ✅ increased minimum width
    max_width = 2.0 * inch   # ✅ added max width to prevent wide columns
    avg_char_width = 0.075 * inch  # ✅ new: estimate text width per character

    # ✅ fix: compute widths dynamically but within bounds
    max_lengths = [max(len(str(row[i])) for row in data) for i in range(num_cols)]
    col_widths = [min(max(min_width, length * avg_char_width), max_width)
                  for length in max_lengths]

    # ✅ fix: normalize total width to fit page
    total_width = sum(col_widths)
    if total_width:
        scale = available_width / total_width
        col_widths = [w * scale for w in col_widths]

    padding = 4  # ✅ fix: consistent padding on all sides
    table = Table(data, colWidths=col_widths, repeatRows=1)

    # ---- 3️⃣ FIX: Improved style settings ----
    style = TableStyle([
        # ✅ fix: clearer header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2F4F4F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),

        # ✅ fix: word wrapping + vertical alignment
        ('WORDWRAP', (0, 0), (-1, -1), None),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        # ✅ fix: consistent font + size for all data
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),

        # ✅ fix: equal padding everywhere
        ('TOPPADDING', (0, 0), (-1, -1), padding),
        ('BOTTOMPADDING', (0, 0), (-1, -1), padding),
        ('LEFTPADDING', (0, 0), (-1, -1), padding),
        ('RIGHTPADDING', (0, 0), (-1, -1), padding),

        # ✅ fix: clean grid and alternating row backgrounds
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#0e1117')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.white, colors.HexColor('#F5F5F5')]),  # alternating colors
    ])
    table.setStyle(style)
    return table


def convert_plot_to_image(plot_fig):
    """Converts a Plotly Figure object into a ReportLab Image object."""

    # Use Kaleido to write the plot as a static PNG into an in-memory buffer
    img_buffer = io.BytesIO()
    plot_fig.write_image(img_buffer, format='png', scale=2)
    img_buffer.seek(0) # "Rewind" the buffer

    # Create a ReportLab Image, setting a standard width
    img = Image(img_buffer, width=5.5*inch, height=3.5*inch)
    return img


def markdown_to_pdf_html(text):
    """
    Translates simple Markdown into ReportLab's <para> HTML-like tags.
    """
    # --- ORDER IS CRITICAL ---

    # 1. Convert ### Heading to <b>Heading</b><br/><br/>
    # This MUST run before the newline conversion
    text = re.sub(r'###\s+(.*?)\n', r'<b>\1</b><br/><br/>', text, flags=re.MULTILINE)
    
    # 2. Convert bullet points (* item) to &bull; item
    text = re.sub(r'^\s*\*\s+', '&bull; ', text, flags=re.MULTILINE)

    # 3. Convert **bold** to <b>bold</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    # 4. Convert *italic* to <i>italic</i>
    #    (This regex avoids matching the * in markdown bullet points)
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    
    # 5. NOW convert all remaining newlines to <br/>
    text = text.replace('\n', '<br/>')
    
    return text