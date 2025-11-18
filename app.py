import streamlit as st
from fpdf import FPDF
from datetime import date

st.title("Sick Leave Application PDF Generator")

name = st.text_input("Employee Name")
designation = st.text_input("Designation")
company = st.text_input("Company Name")
start_date = st.date_input("Start Date", value=date.today())
end_date = st.date_input("End Date", value=date.today())
phone = st.text_input("Phone Number")

if st.button("Generate PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    def add_line(text=""):
        pdf.multi_cell(190, 10, text)

    # Letter format
    add_line("To,")
    add_line("The Manager")
    if company:
        add_line(company)
    add_line("")
    add_line("Subject: Application for Sick Leave")
    add_line("")
    add_line("Respected Sir/Madam,")
    add_line("")
    add_line(
        f"I, {name if name else '_____'}, working as a "
        f"{designation if designation else '_____'}, am unable to attend work "
        f"from {start_date} to {end_date} due to illness."
    )
    add_line("Kindly grant me leave for the mentioned days.")
    add_line("")
    add_line("Thank you,")
    add_line("")
    add_line("Sincerely,")
    add_line(name if name else "_____")
    if phone:
        add_line(f"Phone: {phone}")

    # Correct PDF output (NO .encode())
    pdf_bytes = pdf.output(dest="S")

    st.download_button(
        "Download Sick Leave PDF",
        data=pdf_bytes,
        file_name="sick_leave_application.pdf",
        mime="application/pdf"
    )

    st.success("PDF generated successfully!")
