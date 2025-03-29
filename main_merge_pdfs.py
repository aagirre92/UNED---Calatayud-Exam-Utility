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
        
        # Add a bookmark (marcador) for the first page of each document
        if i == 0:
            output.add_outline_item(header_text, i)

    with open(output_pdf, 'wb') as outputStream:
        output.write(outputStream)


def merge_pdfs(input_folder, output_pdf_path):
    pdf_writer = PdfWriter()
    page_offset = 0
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            input_pdf_path = os.path.join(input_folder, filename)
            temp_pdf_path = os.path.join(input_folder, 'temp_' + filename)
            
            # Add header and create temporary file with bookmark
            add_header(input_pdf_path, temp_pdf_path, filename)
            
            # Read the temporary file
            pdf_reader = PdfReader(temp_pdf_path)
            
            # Add bookmark to the final merged PDF
            pdf_writer.add_outline_item(filename, page_offset)
            
            # Add all pages from this document
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
            
            # Update page offset for next document's bookmark
            page_offset += len(pdf_reader.pages)
            
            # Clean up the temporary file
            os.remove(temp_pdf_path)

    with open(output_pdf_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)


merge_pdfs(input_folder, output_pdf_path)