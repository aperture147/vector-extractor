
from PyPDF2 import PdfFileWriter, PdfFileReader
from subprocess import Popen, DEVNULL
import shlex
import logging
import svg
from uuid import uuid4
from multiprocessing.pool import ThreadPool
import os
import shutil

INKSCAPE_PATH = "inkscape" # change this to your absolute inkscape path or link it to /usr/local/bin
INKSCAPE_EXPORT_ACTIONS = "file-open:tmp/{current_ts}/{i}.ai;vacuum-defs;export-plain-svg;export-filename:result/{current_ts}/{i}.svg;export-do;file-close"
RESULT_FILE_PATH = "result/{current_ts}/{i}.svg"

def extract(
    file_path: str,
    inkscape_log: bool = False,
    artboard_only: bool = False,
    cleanup: bool = True) -> str:
    inkscape_actions = []
    target_file_list = []
    extraction_id = str(uuid4())
    os.mkdir(f'tmp/{extraction_id}')
    try:
        with open(file_path, "rb") as f:
            input_pdf = PdfFileReader(f)
            num_pages = input_pdf.numPages

            for i in range(num_pages):
                logging.info(f'converting page {i} in file')
                output = PdfFileWriter()
                output.addPage(input_pdf.getPage(i))

                # if it already exists, then it's time to clear the directory
                
                with open(f'tmp/{extraction_id}/{i}.ai', 'wb') as temp_f:
                    output.write(temp_f)

                inkscape_actions.append(INKSCAPE_EXPORT_ACTIONS.format(
                    current_ts=extraction_id,
                    i=i
                ))
                target_file_list.append(RESULT_FILE_PATH.format(
                    current_ts=extraction_id,
                    i=i
                ))

        inkscape_actions_str = ";".join(inkscape_actions)
        if inkscape_log:
            with open(f"inkscape_log/{extraction_id}.out.txt", "wb") as f_out, open(f"inkscape_log/{extraction_id}.err.txt", "wb") as f_err: 
                proc = Popen(shlex.split(f'{INKSCAPE_PATH} --actions="{inkscape_actions_str}"'), stdout=f_out, stderr=f_err)
        else:
            proc = Popen(shlex.split(f'{INKSCAPE_PATH} --actions="{inkscape_actions_str}"'), stdout=DEVNULL, stderr=DEVNULL)
        proc.wait()
        if not artboard_only:
            with ThreadPool(os.cpu_count()) as pool:
                pool.starmap(svg.extract_elements, [(file_path,) for file_path in target_file_list])

            if cleanup:
                for file_path in target_file_list:
                    os.remove(file_path)
                shutil.rmtree(f'tmp/{extraction_id}')
        return extraction_id
    except Exception as e:
        if cleanup:
            shutil.rmtree(f'tmp/{extraction_id}')
            shutil.rmtree(f'result/{extraction_id}')
        raise e
