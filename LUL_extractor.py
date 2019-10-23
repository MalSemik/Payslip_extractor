import re
import subprocess

from PyPDF2 import PdfFileReader, PdfFileWriter


def select_file():
    pass
    # return pdf_path


def transform_pdf_to_txt():
    pass
    # return txt_path


def read_names_from_txt(names_txt):
    with open(names_txt, encoding="utf8") as names_file:
        names = names_file.read().split("\n")
        return names


PDF_PATH = r"C:\Users\PLMASEM\PycharmProjects\LUL\pdftotxt\LUL_NonDirigenti_201907_LU08021452411.pdf"
TXT_PATH = PDF_PATH.replace(".pdf",".txt")
NAMES_TXT = r"C:\Users\PLMASEM\PycharmProjects\LUL\test.txt"
print(TXT_PATH)

def get_pattern_of_name(name: str):
    return re.compile(name.replace(" ", r"\s+"))


def extract_numbers_of_pages_with_name(name, pages):
    numbers_of_pages_with_name = []
    for page_number in range(len(pages)):
        result = re.search(get_pattern_of_name(name), pages[page_number])
        if result:
            numbers_of_pages_with_name.append(page_number)  # indeksowanie od zera
    return numbers_of_pages_with_name


def extract_pages_from_converted_txt(txt_path):
    with open(txt_path, encoding="utf8") as txt_file:
        content_of_txt = txt_file.read()
        pages = content_of_txt.split("")

    return pages


def convert_pdf_to_txt(pdf_path):
    subprocess.run(f'pdftotext.exe "{pdf_path}"', shell=True)


def main():
    convert_pdf_to_txt(PDF_PATH)
    pages = extract_pages_from_converted_txt(PDF_PATH.replace(".pdf",".txt"))
    names = read_names_from_txt(NAMES_TXT)
    for name in names:
        numbers_of_pages_with_name = extract_numbers_of_pages_with_name(name, pages)

        reader = PdfFileReader(open(PDF_PATH, 'rb'))
        writer = PdfFileWriter()
        for page_number_with_name in numbers_of_pages_with_name:
            writer.addPage(reader.getPage(page_number_with_name))
        if len(numbers_of_pages_with_name) > 0:
            with open(name + ".pdf", "wb") as out_file:
                writer.write(out_file)


main()
