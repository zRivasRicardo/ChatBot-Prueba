from multiprocessing import Process
import shutil
import pathlib
import time
import os
from dotenv import load_dotenv
from platform import system


def execution_cycle(tag_name):
    os.system('python3 -m behave -f allure_behave.formatter:AllureFormatter -o reporte --tags=' + tag_name)


if __name__ == '__main__':

    load_dotenv(dotenv_path='.env')
    name_os = system()
    if os.getenv('SAVE_REPORT_ALLURE') == "false":
        if name_os == 'Windows':
            folder = str(pathlib.Path().absolute()) + '\\reporte'
        elif name_os == 'Linux' or name_os == 'Darwin':
            folder = str(pathlib.Path().absolute()) + '/reporte'
        shutil.rmtree(folder, ignore_errors=True)
    # Add tags to list_ tag for execute
    list_tag = ["@HU-23"]
    os.environ['CANTIDAD'] = 'Multiple'
    list_tag_execution = []
    for i in list_tag:
        list_tag_execution.append(Process(target=execution_cycle, args=(i,)))

    for i in list_tag_execution:
        i.start()
        time.sleep(1)
