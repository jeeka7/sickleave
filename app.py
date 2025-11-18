import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

st.title("Sick Leave Application PDF Generator")

name = st.text_input("Employee Name")
designation = st.text_input("Designation")
company = st.text_input("Company Name")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
phone = st.text_input("Phone Number")

if st.button("Generate PDF"):
    # Create a PDF in memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    x = 50  
    y = 800  

    line_gap = 20  

    def line(text):
        nonlocal y
        c.drawString(x, y, text)
        y -= line_gap

    # Format of the letter
    line("To,")
    line("The Manager")
    line(company)
    line("")
    line("Subject: Application for Sick Leave")
    line("")
    line("Respected Sir/Madam,")
    line("")
    line(
        f"I, {name}, working as a {designation}, am unable to attend work "
    )
    line(
        f"from {start_date} to {end_date} due to illness. Kindly grant me"
    )
    line(
        "leave for the mentioned days."
    )
    line("")
    line("Thank you,")
    line("")
    line("Sincerely,")
    line(name)
    line(f"Phone: {phone}")

    c.save()
    buffer.seek(0)

    st.download_button(
        "Download Sick Leave PDF",
        data=buffer,
        file_name="sick_leave_application.pdf",
        mime="application/pdf"
    )

    st.success("PDF generated successfully!")
