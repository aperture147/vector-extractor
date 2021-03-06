
from typing import Optional
from PyPDF2 import PdfFileWriter, PdfFileReader
from subprocess import Popen, DEVNULL
import shlex
import logging
import svg
from uuid import uuid4
from multiprocessing.pool import ThreadPool
import os
import shutil

class Extractor:
    INKSCAPE_PATH = "inkscape" # change this to your absolute inkscape path or link it to /usr/local/bin
    INKSCAPE_EXPORT_ACTIONS = "file-open:tmp/{current_ts}/{i}.ai;vacuum-defs;export-plain-svg;export-filename:result/{current_ts}/{i}.svg;export-do;file-close"
    RESULT_FILE_PATH = "result/{current_ts}/{i}.svg"

    def __init__(self, inkscape_path: Optional[str]) -> None:
        if inkscape_path:
            self.INKSCAPE_PATH = inkscape_path
        

    def extract(
        self,
        file_path: str,
        inkscape_log: bool = False,
        artboard_only: bool = False,
        cleanup: bool = True) -> str:

        inkscape_actions = []
        target_file_list = []
        extraction_id: str = str(uuid4())
        
        tmp_dir = f'tmp/{extraction_id}'
        result_dir = f'result/{extraction_id}'
        inkscape_log_dir = f'inkscape_log/{extraction_id}'
        os.mkdir(tmp_dir)
        os.mkdir(inkscape_log_dir)

        try:
            with open(file_path, "rb") as f:
                input_pdf = PdfFileReader(f)
                num_pages = input_pdf.numPages

                for i in range(num_pages):
                    logging.info(f'converting page {i} in file')
                    output = PdfFileWriter()
                    output.addPage(input_pdf.getPage(i))

                    # if it already exists, then it's time to clear the directory
                    
                    with open(f'{tmp_dir}/{i}.ai', 'wb') as temp_f:
                        output.write(temp_f)

                    inkscape_actions.append(self.INKSCAPE_EXPORT_ACTIONS.format(
                        current_ts=extraction_id,
                        i=i
                    ))
                    target_file_list.append(self.RESULT_FILE_PATH.format(
                        current_ts=extraction_id,
                        i=i
                    ))

            inkscape_actions_str = ";".join(inkscape_actions)
            if inkscape_log:
                with open(f"{inkscape_log_dir}/out.txt", "wb") as f_out, open(f"{inkscape_log_dir}/err.txt", "wb") as f_err: 
                    proc = Popen(shlex.split(f'{self.INKSCAPE_PATH} --actions="{inkscape_actions_str}"'), stdout=f_out, stderr=f_err)
            else:
                proc = Popen(shlex.split(f'{self.INKSCAPE_PATH} --actions="{inkscape_actions_str}"'), stdout=DEVNULL, stderr=DEVNULL)
            proc.wait()
            if not artboard_only:
                with ThreadPool(os.cpu_count()) as pool:
                    pool.starmap(svg.extract_elements, [(file_path,) for file_path in target_file_list])

                if cleanup:
                    for file_path in target_file_list:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    if os.path.exists(tmp_dir):
                        shutil.rmtree(tmp_dir)
            return extraction_id
        except Exception as e:
            if cleanup:
                if os.path.exists(tmp_dir):
                    shutil.rmtree(tmp_dir)
                if os.path.exists(result_dir):
                    shutil.rmtree(result_dir)
            raise e
