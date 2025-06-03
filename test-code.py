from PyPDF2 import pdf_to_text

input_path = '../Petersen2021.pdf'

output_path = './PyPDF2 Petersen2021.txt'

pdf_to_text(input_path, output_path)