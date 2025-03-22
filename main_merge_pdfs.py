import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

input_folder = './input'
output_pdf_path = './merged_output.pdf'


def add_header(input_pdf, output_pdf, header_text):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(0, 0, header_text)
    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(input_pdf)
    output = PdfWriter()

    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)

    with open(output_pdf, 'wb') as outputStream:
        output.write(outputStream)


def merge_pdfs(input_folder, output_pdf_path):
    pdf_writer = PdfWriter()
    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            input_pdf_path = os.path.join(input_folder, filename)
            temp_pdf_path = os.path.join(input_folder, 'temp_' + filename)
            add_header(input_pdf_path, temp_pdf_path, filename)
            pdf_reader = PdfReader(temp_pdf_path)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
            os.remove(temp_pdf_path)

    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)


merge_pdfs(input_folder, output_pdf_path)
