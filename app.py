from PyPDF2 import PdfFileWriter, PdfFileReader
from subprocess import Popen, DEVNULL
from time import time
import shlex
import logging

INKSCAPE_PATH = "inkscape" # change this to your absolute inkscape path or link it to /usr/local/bin

inkscape_actions = []
current_ts = time()

with open("test.ai", "rb") as f:
    input_pdf = PdfFileReader(f)
    num_pages = input_pdf.numPages

    for i in range(num_pages):
        logging.info(f'converting page {i} in file')
        output = PdfFileWriter()
        output.addPage(input_pdf.getPage(i))
        with open(f'tmp/{current_ts}-{i}.ai', 'wb') as temp_f:
            output.write(temp_f)
        inkscape_actions.append(f"file-open:tmp/{current_ts}-{i}.ai;vacuum-defs;export-plain-svg;export-area-drawing;export-filename:result/{current_ts}-{i}.svg;export-do;file-close")

inkscape_actions_str = ";".join(inkscape_actions)

proc = Popen(shlex.split(f'inkscape --actions="{inkscape_actions_str}" --pdf-poppler'), stdout=DEVNULL)
proc.wait()