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

# --- App Title (Final Version) ---
st.title("Sick Leave App Generator 📄")
st.write("This app fills a DOCX template with your details. Please provide the required information below.")

# --- Robust Path to Template ---
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_FILE = os.path.join(BASE_DIR, "template.docx")
except NameError:
    BASE_DIR = os.getcwd() # Fallback
    TEMPLATE_FILE = os.path.join(BASE_DIR, "template.docx")


# --- Input Fields ---
with st.form(key="leave_form"):
    
    st.subheader("Company Details")
    # --- NEW FIELDS ---
    company_name = st.text_input("Your Company Name", "Example Inc.")
    company_address = st.text_input("Your Company Address", "123 Example St, City, State")

    st.subheader("Your Details")
    full_name = st.text_input("Your Full Name", "John Doe")
    job_title = st.text_input("Your Job Title", "Software Engineer")
    department = st.text_input("Your Department", "Engineering")
    
    st.subheader("Leave Details")
    manager_name = st.text_input("Manager's Name", "Jane Smith")
    # --- NEW FIELD ---
    manager_title = st.text_input("Manager's Title", "Engineering Manager")
    
    start_date = st.date_input("First Day of Leave", datetime.date.today())
    end_date = st.date_input("Last Day of Leave", datetime.date.today() + datetime.timedelta(days=2))
    reason = st.text_area("Reason for Leave (Brief)", "Experiencing flu-like symptoms and need to rest and recover.")
    
    colleague_name = st.text_input("Colleague's Name (for handover - optional)")


    submit_button = st.form_submit_button(label="Generate Document")

# --- Document Generation ---
if submit_button:
    
    # --- Check for template one last time, right before use ---
    if not os.path.exists(TEMPLATE_FILE):
        st.error(f"FATAL ERROR: Template file 'template.docx' not found at path: {TEMPLATE_FILE}")
        st.info("Please make sure 'template.docx' is in your GitHub repository and re-upload it.")
        st.stop()
        
    try:
        # Load the template using the full path
        doc = DocxTemplate(TEMPLATE_FILE)

        # Format dates
        today_str = datetime.date.today().strftime("%B %d, %Y")
        start_date_str = start_date.strftime("%B %d, %Y")
        end_date_str = end_date.strftime("%B %d, %Y")
        
        # Calculate number of days
        num_days = (end_date - start_date).days + 1
        if num_days <= 0:
            num_days = 1 # Handle same-day leave

        # Create the context dictionary
        context = {
            'today_date': today_str,
            'company_name': company_name,     # --- ADDED ---
            'company_address': company_address, # --- ADDED ---
            'full_name': full_name,
            'job_title': job_title,
            'department': department,
            'manager_name': manager_name,
            'manager_title': manager_title,   # --- ADDED ---
            'start_date': start_date_str,
            'end_date': end_date_str,
            'num_days': num_days,
            'reason': reason,
            'colleague_name': colleague_name.strip().capitalize() # --- ADDED .capitalize() ---
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
        st.warning("This error often means the 'template.docx' file is corrupted or not a valid .docx file.")
        st.info("Please try re-uploading your 'template.docx' file to GitHub using the 'Upload files' button.")
