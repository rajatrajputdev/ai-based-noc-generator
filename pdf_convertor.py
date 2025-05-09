from fpdf import FPDF

def print_line(pdf, text, line_height=10, bold=False):
    try:
        if bold:
            try:
                pdf.set_font("Arial", "B", size=12)
            except Exception:
                pdf.set_font("Helvetica", "B", size=12)
        else:
            try:
                pdf.set_font("Arial", "", size=12)
            except Exception:
                pdf.set_font("Helvetica", "", size=12)
    except Exception:
        pdf.set_font("Helvetica", "", size=12)

    # Using multi_cell to display the whole text in case it exceeds the page width
    pdf.multi_cell(0, line_height, text)


def text_to_pdf(text, output_filename="noc_document.pdf"):
    try:
        #H Handling special characters and formatting
        text = (text.replace("•", "-")
                    .replace("“", '"')
                    .replace("”", '"')
                    .replace("—", "-")
                    .replace("–", "-")
                    .replace("’", "'")
                    .replace("…", "...")
                    .replace("©", "(c)"))

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_margins(15, 15, 15)

        # Bold font for the title
        try:
            pdf.set_font("Arial", "B", size=12)
        except Exception:
            pdf.set_font("Helvetica", "B", size=12)

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
            print_line(pdf, line, line_height=10, bold=is_bold)

        pdf.output(output_filename)
        print(f"Your PDF '{output_filename}' is ready!")
        return True, output_filename

    except Exception as e:
        print(f"Something went wrong while creating the PDF: {str(e)}")
        return False, str(e)


if __name__ == "__main__":
    # Testing the logic to see if the PDF is generated correctly
    sample_text = """NO OBJECTION CERTIFICATE (NOC)

This is a sample NOC document to test PDF conversion.

Guest Details:
Name: Test Person (e.g., José, Ömer)
Profession: Software Developer

Media Rights and Usage:
Mishka Productions and Mr. Kunal Kulkarni have the right to record, edit, and publish.

Content Editing: The content can be modified.
No Financial Claims: None.
Non-Objection and Confidentiality: All terms are binding.

Acceptance and Signature:
Guest Signature: ___________________
Host Signature: ___________________
"""

    success, result = text_to_pdf(sample_text, "test_noc.pdf")
    if success:
        print(f"PDF successfully created as {result}")
    else:
        print(f"Error creating PDF: {result}")
