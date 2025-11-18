import streamlit as st
from docxtpl import DocxTemplate
import pypandoc
import os

st.title("Sick Leave Application PDF Generator")

# Input fields from user
employee_name = st.text_input("Employee Name")
designation = st.text_input("Designation")
company_name = st.text_input("Company Name")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
phone_number = st.text_input("Phone Number")

if st.button("Generate PDF"):
    # Load DOCX template
    template = DocxTemplate("sick_leave_template.docx")

    # Merge context values
    context = {
        "employee_name": employee_name,
        "designation": designation,
        "company_name": company_name,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "phone_number": phone_number,
    }

    template.render(context)

    # Save temporary merged docx
    template.save("output.docx")

    # Convert DOCX to PDF
    pypandoc.convert_file(
        "output.docx",
        "pdf",
        outputfile="output.pdf",
        extra_args=["--pdf-engine=xelatex"]
    )

    # Download PDF
    with open("output.pdf", "rb") as f:
        st.download_button(
            label="Download Sick Leave PDF",
            data=f,
            file_name="sick_leave_application.pdf",
            mime="application/pdf"
        )

    st.success("PDF generated successfully!")
