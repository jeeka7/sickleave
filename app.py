import streamlit as st
import datetime
from docxtpl import DocxTemplate
from io import BytesIO
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Document Generator",
    page_icon="📄"
)

# --- App Title ---
st.title("Sick Leave Application Generator 📄")
st.write("This app fills a DOCX template with your details. Please provide the required information below.")

# --- Template File Check ---
TEMPLATE_FILE = "template.docx"

if not os.path.exists(TEMPLATE_FILE):
    st.error(f"Error: Template file '{TEMPLATE_FILE}' not found.")
    st.info(f"Please create a file named '{TEMPLATE_FILE}' in the same directory as this app. See the instructions file for the template text.")
    st.stop()


# --- Input Fields ---
with st.form(key="leave_form"):
    st.subheader("Your Details")
    full_name = st.text_input("Your Full Name", "John Doe")
    job_title = st.text_input("Your Job Title", "Software Engineer")
    department = st.text_input("Your Department", "Engineering")
    
    st.subheader("Leave Details")
    manager_name = st.text_input("Manager's Name", "Jane Smith")
    start_date = st.date_input("First Day of Leave", datetime.date.today())
    end_date = st.date_input("Last Day of Leave", datetime.date.today() + datetime.timedelta(days=2))
    reason = st.text_area("Reason for Leave (Brief)", "Experiencing flu-like symptoms and need to rest and recover.")

    submit_button = st.form_submit_button(label="Generate Document")

# --- Document Generation ---
if submit_button:
    try:
        # Load the template
        # This assumes 'template.docx' is in the same folder as app.py
        # If it were on GitHub, you'd use requests to get the raw file bytes
        doc = DocxTemplate(TEMPLATE_FILE)

        # Format dates
        today_str = datetime.date.today().strftime("%B %d, %Y")
        start_date_str = start_date.strftime("%B %d, %Y")
        end_date_str = end_date.strftime("%B %d, %Y")
        
        # Calculate number of days
        num_days = (end_date - start_date).days + 1

        # Create the context dictionary
        context = {
            'today_date': today_str,
            'full_name': full_name,
            'job_title': job_title,
            'department': department,
            'manager_name': manager_name,
            'start_date': start_date_str,
            'end_date': end_date_str,
            'num_days': num_days,
            'reason': reason,
        }

        # Render the document with the context
        doc.render(context)

        # Save the rendered document to a byte stream
        doc_io = BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)  # Rewind the stream to the beginning

        st.success("Your document has been generated!")

        # Provide the download button
        st.download_button(
            label="Download Application (DOCX)",
            data=doc_io,
            file_name=f"{full_name.replace(' ', '_')}_Sick_Leave.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        st.error(f"An error occurred during document generation: {e}")
