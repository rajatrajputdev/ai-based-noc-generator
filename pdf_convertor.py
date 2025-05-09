from fpdf import FPDF
from io import BytesIO
import unicodedata

def sanitize_text(text):
    normalized = unicodedata.normalize("NFKD", text)
    return normalized.encode("latin-1", "ignore").decode("latin-1")

def print_line(pdf, text, line_height=10, bold=False):
    try:
        if bold:
            pdf.set_font("Arial", "B", size=12)
        else:
            pdf.set_font("Arial", "", size=12)
    except:
        pdf.set_font("Helvetica", "B" if bold else "", size=12)
    pdf.multi_cell(0, line_height, text)

def text_to_pdf(text):
    try:
        text = (text.replace("•", "-")
                    .replace("“", '"')
                    .replace("”", '"')
                    .replace("—", "-")
                    .replace("–", "-")
                    .replace("’", "'")
                    .replace("…", "...")
                    .replace("©", "(c)"))

        text = sanitize_text(text)

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_margins(15, 15, 15)
        pdf.set_font("Arial", "B", size=12)

        pdf.cell(0, 10, "NO OBJECTION CERTIFICATE (NOC)", 0, 1, "C")
        pdf.ln(10)

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
            print_line(pdf, line, line_height=10, bold=is_bold)

        # Output PDF to bytes
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        return True, BytesIO(pdf_bytes)

    except Exception as e:
        return False, str(e)
