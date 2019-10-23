import PySimpleGUI as sg
import re
import subprocess

from PyPDF2 import PdfFileReader, PdfFileWriter


def read_names_from_txt(names_txt):
    with open(names_txt, encoding="utf8") as names_file:
        names = names_file.read().split("\n")
        return names


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

        if pages[-1] == "":
            pages.pop()

    return pages


def convert_pdf_to_txt(pdf_path):
    subprocess.run(f'pdftotext.exe "{pdf_path}"', shell=True)


def check_if_selected_file(key):
    if values[key] != '':
        path = values[key]
        return path
    else:
        sg.Popup(f'You need to select {key} file!')

color = 'Dark'
sg.change_look_and_feel(color)

menu_def = [['&Color', ['&Dark', '&Purple', '&Blue', '&GreenTan']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

layout = [[sg.Menu(menu_def, tearoff=True)],
          [sg.Text('Choose the file you want to convert:', size=(50, 1))],
          [sg.Input(),sg.FileBrowse(button_text='Choose pdf file', key='pdf')],
          [sg.Frame(layout=[[sg.Radio('LUL     ', 'CHECK', key="LUL", default=False, size=(10, 1)),
                             sg.Radio('Payslip', 'CHECK', key="PAYSLIP", default=True)]],
                    title='Options', title_color='green', relief=sg.RELIEF_SUNKEN, tooltip='Select one option')],
          [sg.Text('Write surnames and names or select a file with names:')],
          [sg.Text('E.g. ROSSI MARCO')],
          [sg.Multiline(size=(35, 10), key='INPUT')],
          [sg.Input(), sg.FileBrowse(button_text='Choose txt file', key='txt')],
          [sg.Text('')],
          [sg.OK(), sg.Cancel()]]

color = 'Dark'
sg.change_look_and_feel(color)
# Create the Window
window = sg.Window('LUL extractor', layout, resizable=True)
# Event Loop to process "events"
while True:
    try:

        # sg.PopupAnimated(r"C:\Users\PLMASEM\PycharmProjects\LUL\pdftotxt\ring_gray_segments.gif", 'Converting files',time_between_frames=0.01)
        event, values = window.Read()
        print(event, values)
        if event == 'OK':
            pdf_path = check_if_selected_file('pdf')
            if pdf_path == None:
                continue
            convert_pdf_to_txt(pdf_path)
            pages = extract_pages_from_converted_txt(pdf_path.replace(".pdf", ".txt"))

            if values['INPUT'] == '\n':
                names_txt = check_if_selected_file('txt')
                if names_txt == None:
                    continue
                names = read_names_from_txt(names_txt)
            else:
                names = values['INPUT'].upper().split('\n')
                names = [name for name in names if name != '']
                print(names)

            not_found = []
            for name in names:
                numbers_of_pages_with_name = extract_numbers_of_pages_with_name(name, pages)
                if values['LUL'] == True:
                    numbers_of_pages_with_name = numbers_of_pages_with_name[::2]
                reader = PdfFileReader(open(pdf_path, 'rb'))
                writer = PdfFileWriter()
                for page_number_with_name in numbers_of_pages_with_name:
                    writer.addPage(reader.getPage(page_number_with_name))
                if len(numbers_of_pages_with_name) > 0:
                    with open(name + ".pdf", "wb") as out_file:
                        writer.write(out_file)
                else:
                    not_found.append(name)

            if len(not_found) > 0:
                string = "\n".join(not_found)
                sg.Popup(f'The following names were not found:\n{string}')
        if event in (None, 'Cancel'):
            break

    except Exception as e:
        sg.Popup(f'Something went wrong\n {e}')

window.Close()
