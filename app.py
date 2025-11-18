# app.py
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
from datetime import date

st.set_page_config(page_title="Sick Leave PDF Generator")
st.title("Sick Leave Application PDF Generator")

# --- User inputs ---
name = st.text_input("Employee Name")
designation = st.text_input("Designation")
company = st.text_input("Company Name")
start_date = st.date_input("Start Date", value=date.today())
end_date = st.date_input("End Date", value=date.today())
phone = st.text_input("Phone Number")

if st.button("Generate PDF"):
    # Create a PDF in memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Start a text object (handles multiline automatically)
    left_margin = 50
    top_margin = 800
    textobject = c.beginText(left_margin, top_margin)
    textobject.setFont("Helvetica", 12)
    line_gap = 16  # spacing between lines (textobject.textLine handles this)

    # Build the letter lines
    lines = []
    lines.append("To,")
    lines.append("The Manager")
    if company:
        lines.append(company)
    lines.append("")  # blank line
    lines.append("Subject: Application for Sick Leave")
    lines.append("")  # blank line
    lines.append("Respected Sir/Madam,")
    lines.append("")  # blank line

    # Compose the body as a couple of sentences (keeps them readable)
    body_1 = f"I, {name if name else '______'}, working as a {designation if designation else '______'},"
    body_2 = f"am unable to attend work from {start_date} to {end_date} due to illness."
    body_3 = "Kindly grant me leave for the mentioned days."

    lines.append(body_1)
    lines.append(body_2)
    lines.append(body_3)
    lines.append("")  # blank line
    lines.append("Thank you,")
    lines.append("")  # blank line
    lines.append("Sincerely,")
    lines.append(name if name else "______")
    if phone:
        lines.append(f"Phone: {phone}")

    # Write lines into the PDF
    for ln in lines:
        textobject.textLine(ln)

    c.drawText(textobject)
    c.showPage()
    c.save()

    buffer.seek(0)

    st.download_button(
        "Download Sick Leave PDF",
        data=buffer,
        file_name="sick_leave_application.pdf",
        mime="application/pdf"
    )

    st.success("PDF generated successfully!")
