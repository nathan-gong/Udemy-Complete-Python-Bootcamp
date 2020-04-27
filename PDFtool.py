# Final Capstone Project
# Interactive PDF tool that allows users to edit and extract information
# from pdf files using the PyPDF2 and pdfminer packages

from PyPDF2 import PdfFileReader, PdfFileWriter
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO

def extract_information(pdf_path):
    '''
    INPUT: pdf
    OUTPUT: pdf file information
    '''
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """

    print(txt)
    return information

def rotate_pages(pdf_path):
    '''
    INPUT: pdf
    OUTPUT: rotated pdf
    '''
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(pdf_path)
    # Rotate page 90 degrees to the right
    page_1 = pdf_reader.getPage(0).rotateClockwise(90)
    pdf_writer.addPage(page_1)
    # Rotate page 90 degrees to the left
    page_2 = pdf_reader.getPage(1).rotateCounterClockwise(90)
    pdf_writer.addPage(page_2)
    # Add a page in normal orientation
    pdf_writer.addPage(pdf_reader.getPage(2))

    with open('rotate_pages.pdf', 'wb') as fh:
        pdf_writer.write(fh)

def merge_pdfs(paths, output):
    '''
    INPUT: pdfs
    OUTPUT: merged pdf
    '''
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

def split(path, name_of_split):
    '''
    INPUT: pdf
    OUTPUT: split pdfs
    '''
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output = f'{name_of_split}{page}.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

def create_watermark(input_pdf, output, watermark):
    '''
    INPUT: pdf
    OUTPUT: pdf with watermarked pages
    '''
    watermark_obj = PdfFileReader(watermark)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output, 'wb') as out:
        pdf_writer.write(out)

def add_encryption(input_pdf, output_pdf, password):
    '''
    INPUT: pdf
    OUTPUT: encrypted pdf
    '''
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(input_pdf)

    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))

    pdf_writer.encrypt(user_pwd=password, owner_pwd=None, 
                       use_128bit=True)

    with open(output_pdf, 'wb') as fh:
        pdf_writer.write(fh)

def pdf_to_text(path, output_text):
    '''
    INPUT: pdf
    OUTPUT: text file
    '''
    manager = PDFResourceManager()
    retstr = BytesIO()
    layout = LAParams(all_texts=True)
    device = TextConverter(manager, retstr, laparams=layout)
    filepath = open(path, 'rb')
    interpreter = PDFPageInterpreter(manager, device)

    for page in PDFPage.get_pages(filepath, check_extractable=True):
        interpreter.process_page(page)
        text = retstr.getvalue()
    
    filepath.close()
    device.close()
    retstr.close()

    f = open(output_text, "w+")
    f.write(text)
    f.close()

if __name__ == '__main__':

    print('Welcome to PDF Tool! What would you like to do?')
    print('1) Extract file information \n2) Rotate pages \n3) Merge files')
    print('4) Split files \n5) Add a watermark \n6) Encrypt file')
    print('7) Extract file text')

    user = 9

    while user not in range(1,8):
        user = int(input('Select a number: '))

        if user == 1:
            path = input('Enter pdf filename: ')
            extract_information(path)
        elif user == 2:
            path = input('Enter pdf filename: ')
            rotate_pages(path)
        elif user == 3:
            inpdf = list(input('Enter pdfs to be merged as a list: '))
            outpdf = input('Enter new pdf filename: ')
            merge_pdfs(inpdf, outpdf)
        elif user == 4:
            inpdf = input('Enter pdf to be split: ')
            output = input('Enter new pdf filename: ')
            split(inpdf, outpdf)
        elif user == 5:
            inpdf = input('Enter pdf filename: ')
            outpdf = input('Enter new pdf filename: ')
            wtmk = input('Enter watermark: ')
            create_watermark(inpdf, outpdf, wtmk)
        elif user == 6:
            inpdf = input('Enter pdf filename: ')
            outpdf = input('Enter new pdf filename: ')
            pswd = input('Enter password: ')
        elif user == 7:
            inpdf = input('Enter pdf filename: ')
            outtxt = input('Enter new text filename: ')
        else: 
            print('Please choose a number from the available options!')
