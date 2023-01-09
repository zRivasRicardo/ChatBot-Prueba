import allure
from allure_commons.types import AttachmentType
import os
import shutil
from platform import system
import pathlib
from helper.plugins import PluginSpec


def attachment_browser_scenario_in_allure(context):
    allure.attach(context.browser.name, name="Browser", attachment_type=AttachmentType.TEXT)

def attachment_screenshot_step_in_allure(context):
    allure.attach(context.browser.get_screenshot_as_png(),name="screenshot", attachment_type=AttachmentType.PNG)

def update_personal_report_allure(context):
    resolution = context.browser.get_window_size()
    file = open(str(pathlib.Path().absolute()) + "\\report\\widgets\\environment.properties", "w+")
    if os.getenv('EXECUTION_TYPE') == 'hub':
        file = open(str(pathlib.Path().absolute()) + "/report/widgets/environment.properties", "w+")
    file.write("Browser :" + context.browser.name.capitalize() + os.linesep)    
    file.write("Browser.Version : Latest" + os.linesep)
    file.write("Resolución" + os.linesep)
    file.write("Ancho :" + str(resolution['width']) + os.linesep)
    file.write("Alto :" + str(resolution['height']) + os.linesep)
    file.write("Ambiente : QA Hakalab" + os.linesep)
    file.close()

def execute_allure_combine():
    if os.getenv('EXECUTE_ALLURE') == "true":
        name_os = system()
        file_name_allure = 'allure'
        if name_os == 'Windows':
            file_name_allure += '.bat'

        path_allure = os.path.join(os.getcwd(), 'helper', 'vendor', 'allure-2.13.6', 'bin', file_name_allure)

        if name_os == "Darwin" or name_os == "Linux":
            # make bin executable
            mode = os.stat(path_allure).st_mode
            mode |= (mode & 0o444) >> 2
            os.chmod(path_allure, mode)

        os.system(path_allure + ' generate reporte -o report -c')
        if os.getenv('SAVE_REPORT_ALLURE') == "false":
            folder = str(pathlib.Path().absolute()) + '/reporte'
            shutil.rmtree(folder, ignore_errors=True)
        shutil.copy(os.path.join(os.getcwd(), 'helper', 'vendor', 'report-assets', 'index.html'),
                    os.path.join(os.getcwd(), 'report', 'index.html'))
        shutil.copy(os.path.join(os.getcwd(), 'helper', 'vendor', 'report-assets', 'app.js'),
                    os.path.join(os.getcwd(), 'report', 'app.js'))
        shutil.copy(os.path.join(os.getcwd(), 'helper', 'vendor', 'report-assets', 'styles.css'),
                    os.path.join(os.getcwd(), 'report', 'styles.css'))
        shutil.copy(
            os.path.join(os.getcwd(), 'helper', 'vendor', 'report-assets', 'executors.json'),
            os.path.join(os.getcwd(), 'report', 'widgets', 'executors.json'))

        os.system(f"python3 ./helper/combine.py .{os.sep}report")
        if os.getenv("CLEAN_EXTRAS_REPORT_ALLURE") == "true":
            os.remove(os.path.join(os.getcwd(), 'report', 'index.html'))
            os.remove(os.path.join(os.getcwd(), 'report', 'app.js'))
            os.remove(os.path.join(os.getcwd(), 'report', 'styles.css'))
            os.remove(os.path.join(os.getcwd(), 'report', 'sinon-9.2.4.js'))
            os.remove(os.path.join(os.getcwd(), 'report', 'server.js'))
            os.remove(os.path.join(os.getcwd(), 'report', 'favicon.ico'))
            shutil.rmtree(os.path.join(os.getcwd(), 'report', 'widgets'), ignore_errors=True)
            shutil.rmtree(os.path.join(os.getcwd(), 'report', 'export'), ignore_errors=True)
            shutil.rmtree(os.path.join(os.getcwd(), 'report', 'data'), ignore_errors=True)
            shutil.rmtree(os.path.join(os.getcwd(), 'report', 'history'), ignore_errors=True)
            shutil.rmtree(os.path.join(os.getcwd(), 'report', 'plugins'), ignore_errors=True)

class AllurePlugin:
    """A hook implementation namespace."""
    @PluginSpec.hookimpl
    def after_step(self, context):
        attachment_screenshot_step_in_allure(context)

    @PluginSpec.hookimpl
    def after_all(self, context):
        if os.getenv("EXECUTION_PARALLEL") == "false":
            update_personal_report_allure(context)
            execute_allure_combine()
