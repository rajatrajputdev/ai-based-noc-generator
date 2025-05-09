import openai
import config
import re
import streamlit as st
def generate_noc(guest_name, guest_profession, company_name, host_name, recording_date,
                recording_time, recording_location):

    # Configuring OpenAI API
    openai.api_type = "azure"
    openai.api_key = st.secrets["openai"]["API_KEY"]  # Retrieved from .streamlit/secrets.toml
    openai.api_base = st.secrets["openai"]["API_BASE"]  # Retrieved from .streamlit/secrets.toml
    openai.api_version = st.secrets["openai"]["API_VERSION"]  # Retrieved from .streamlit/secrets.toml
    engine = st.secrets["openai"]["ENGINE"]  # Retrieved from .streamlit/secrets.toml


    prompt = f"""
    Generate a formal and legally binding No Objection Certificate (NOC) for a podcast guest.

    Details:
    - Guest Name: {guest_name}
    - Guest Profession: {guest_profession}
    - Company: "Mishka Productions"
    - Host: "Mr. Kunal Kulkarni"
    - Recording Date: {recording_date}
    - Recording Time: {recording_time}
    - Location: {recording_location}

    Your output should follow this general structure:
    1. Begin with: "This is to certify that {guest_name} has been invited as a guest hosted by {host_name} produced by {company_name}."
    2. Include the following legal clauses as numbered points:
        - Media Rights
        - Usage
        - Content Editing
        - No Financial Claims
        - Non-Objection
        - Confidentiality
    3. End with a section titled: "Guest Details", including:
        - Name
        - Profession
        - Signature: ___________
        - Date: ___________
    4. Follow with: "For {company_name}" and signature block:
        - Name: {host_name}
        - Designation: Founder/Producer
        - Signature: ___________
        - Date: ___________

    Keep the tone professional and industry-standard.
    """

    try:
        response = openai.ChatCompletion.create(
            engine=config.ENGINE,
            messages=[
                {"role": "system", "content": "You are a legal document generator specializing in No Objection Certificates."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating NOC: {e}"
