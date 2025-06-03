# code taken from rag-chatbot by Antara Ganapathy at https://github.com/AntaraGanapathy/rag-chatbot/tree/main

# firs run 'pip install PyPDF2==3.0.1'
import PyPDF2


def pdf_to_text(pdf_path, output_txt):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text = ''

        for page_num in range(0, 12):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
