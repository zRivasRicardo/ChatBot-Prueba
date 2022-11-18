from multiprocessing import Process
import time
import os
import argparse
from os import listdir
import subprocess

from dotenv import load_dotenv

from helper.plugins.AllurePlugin import execute_allure_combine


def execution_regression():
    os.system('python -m behave -f allure_behave.formatter:AllureFormatter -o reporte ./features/')
    
def execution_tag(tag_name):
    os.system('python -m behave -f allure_behave.formatter:AllureFormatter -o reporte --tags='+tag_name)

def execution_parallel():
    # Iterable con las rutas de los scripts
    scripts_paths = listdir("./executions/")
    print("La lista", scripts_paths)
    # Creamos cada proceso
    list_processes = [subprocess.Popen(["python", "./executions/"+script]) for script in scripts_paths]

    # Esperamos a que todos los subprocesos terminen
    for the_process in list_processes:
        the_process.wait()
    print("TERMINO DE TODOS LOS PROCESOS")
    load_dotenv(dotenv_path='.env')
    print("EXECUTION PARALLEL : ", os.getenv("EXECUTION_PARALLEL"))
    if os.getenv("EXECUTION_PARALLEL") == "true":
        execute_allure_combine()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--type_execution", help="type execution to functional test")
    args = parser.parse_args()
    type_execution = args.type_execution

    if type_execution == "total_regression":
        list_tag = ["selenium", "service", "appium", "artificial_vision"]
        list_tag_execution = []
        for i in list_tag:
            list_tag_execution.append(Process(target=execution_tag, args=(i,)))

        for i in list_tag_execution:
            i.start()
            time.sleep(1)

    else:
        if type_execution == "parallel":
            execution_parallel()
        else:
            execution_tag(type_execution)
     
    #if type_execution == "regression":
    #    for i in regresion:
    #        i.join()

    #if type_execution == "tag":
    #    for i in list_tag_execution:
            
    #        i.join()
