from fpdf import FPDF
from io import BytesIO

def clean_text(text):
    """
    Replace unsupported Unicode characters with compatible equivalents.
    """
    return (text.replace("\u2003", " ")  # Replace em space with a normal space
                .replace("•", "-")
                .replace("“", '"')
                .replace("”", '"')
                .replace("—", "-")
                .replace("–", "-")
                .replace("’", "'")
                .replace("…", "...")
                .replace("©", "(c)"))

def print_line(pdf, text, line_height=8, bold=False):
    try:
        if bold:
            pdf.set_font("Arial", "B", size=10)  # Reduced font size for bold text
        else:
            pdf.set_font("Arial", "", size=10)  # Reduced font size for normal text
    except Exception:
        pdf.set_font("Helvetica", "", size=10)

    # Using multi_cell to display the whole text in case it exceeds the page width
    pdf.multi_cell(0, line_height, text)

def text_to_pdf(text):
    try:
        # Clean and format text
        text = clean_text(text)

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_margins(15, 15, 15)

        # Bold font for the title
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "NO OBJECTION CERTIFICATE (NOC)", 0, 1, "C")
        pdf.ln(10)

        # Keywords that should be bold
        bold_keywords = [
            "NO OBJECTION CERTIFICATE (NOC)",
            "Mishka Productions",
            "Mr. Kunal Kulkarni",
            "Guest Details:",
            "Media Rights",
            "Usage",
            "Content Editing",
            "No Financial Claims",
            "Non-Objection",
            "Confidentiality",
            "Acceptance and Signature"
        ]

        for line in text.split('\n'):
            is_bold = any(keyword in line for keyword in bold_keywords)
            print_line(pdf, line, line_height=8, bold=is_bold)

        # Save to a BytesIO object
        pdf_output = BytesIO()
        pdf.output(pdf_output, 'F')  # 'F' specifies that the output is written to a file-like object
        pdf_output.seek(0)

        return pdf_output
    except Exception as e:
        raise RuntimeError(f"Error creating PDF: {str(e)}")
