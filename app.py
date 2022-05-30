from PyPDF2 import PdfFileWriter, PdfFileReader
from subprocess import Popen
from time import time
import shlex
import logging

INKSCAPE_PATH = "inkscape" # change this to your absolute inkscape path or link it to /usr/local/bin
INKSCAPE_EXPORT_ACTIONS = "file-open:tmp/{current_ts}-{i}.ai;vacuum-defs;export-plain-svg;export-area-drawing;export-filename:result/{current_ts}-{i}.svg;export-do;file-close"

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

        inkscape_actions.append(INKSCAPE_EXPORT_ACTIONS.format(
            current_ts=current_ts,
            i=i
        ))

inkscape_actions_str = ";".join(inkscape_actions)
with open(f"log/{current_ts}.out.txt", "wb") as f_out, open(f"log/{current_ts}.err.txt", "wb") as f_err: 
    proc = Popen(shlex.split(f'{INKSCAPE_PATH} --actions="{inkscape_actions_str}"'), stdout=f_out, stderr=f_err)
    proc.wait()