import streamlit as st
from noc_generator import generate_noc
from pdf_convertor import text_to_pdf
import re

st.set_page_config(page_title="NOC Generator", layout="centered")
st.title("📄 No Objection Certificate (NOC) Generator")
st.markdown("---")
st.markdown("### 🎙️ Guest Information")

with st.form("noc_form"):
    col1, col2 = st.columns(2)
    with col1:
        guest_name = st.text_input("Guest Name")
        recording_date = st.text_input("Recording Date", placeholder="e.g., 15th May 2025")
        recording_time = st.text_input("Recording Time", placeholder="e.g., 3:00 PM to 5:00 PM")
    with col2:
        guest_profession = st.text_input("Guest Profession")
        recording_location = st.text_input("Recording Location")

    submitted = st.form_submit_button("🔍 Generate NOC")

if submitted:
    if not guest_name.strip():
        st.error("Guest name cannot be empty!")
    else:
        company_name = "Mishka Productions"
        host_name = "Mr. Kunal Kulkarni"

        with st.spinner("Talking to AI and generating the document..."):
            noc_text = generate_noc(
                guest_name,
                guest_profession,
                company_name,
                host_name,
                recording_date,
                recording_time,
                recording_location,
            )

        noc_text_cleaned = (noc_text.replace("•", "-")
                                      .replace("“", '"')
                                      .replace("”", '"')
                                      .replace("—", "-")
                                      .replace("–", "-")
                                      .replace("’", "'")
                                      .replace("…", "...")
                                      .replace("©", "(c)"))

        st.session_state["noc_text"] = noc_text_cleaned

if "noc_text" in st.session_state:
    st.markdown("---")
    st.subheader("📝 Review and Edit the NOC Document")

    final_text = st.text_area("Edit below if needed:", value=st.session_state["noc_text"], height=400, key="review_box")
    st.session_state["final_text"] = final_text

    if st.button("📄 Generate PDF"):
        safe_filename = f"NOC_{re.sub(r'[^a-zA-Z0-9_]', '_', guest_name)}.txt"
        with open(safe_filename, "w", encoding="utf-8") as f:
            f.write(st.session_state["final_text"])

        pdf_filename = safe_filename.replace(".txt", ".pdf")
        success, result = text_to_pdf(st.session_state["final_text"], pdf_filename)

        if success:
            with open(pdf_filename, "rb") as f:
                st.success("✅ PDF successfully created!")
                st.download_button("📥 Download PDF", f, file_name=pdf_filename)
        else:
            st.error(f"PDF generation failed: {result}")
