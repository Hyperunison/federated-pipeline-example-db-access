from typing import List, Dict
import os

def get_input_files(ucdm: List[Dict[str, str]], parameters: Dict[str, str]) -> Dict[str, str]:
    folder_path = os.path.dirname(os.path.abspath(__file__))

    return {
        "data/dsn.txt": parameters['dsn'],
        "main.nf": file_get_contents(folder_path + '/main.nf')
    }


def get_output_file_masks(parameters) -> Dict[str, str]:
    return {
        ".nextflow.log": "/basic/.nextflow.log",
        "result.txt": "result.txt",
        "report.html": "/basic/report.html",
    }


def get_nextflow_cmd(input_files: Dict[str, str], parameters, run_name, weblog_url):
    return "nextflow run main.nf -name {} -with-report report.html -with-weblog {} -with-trace -ansi-log".format(
        run_name,
        weblog_url,
    )


def file_get_contents(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()