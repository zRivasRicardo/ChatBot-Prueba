import re
import allure
from allure_commons.types import AttachmentType
from dotenv import load_dotenv
from helper.plugins import PluginSpec
import os
from platform import system
import pathlib
from helper.selenium_class.elements import Elements
from helper.selenium_class.js_script import JsScript
from helper.selenium_class.keyboard_actions import KeyboardActions
from helper.selenium_class.mouse_actions import MouseActions
from helper.selenium_class.window_control import WindowControl
from selenium import webdriver


def camel_to_snake(text):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()

# def prepare_pages(context):
#     current_directory = os.getcwd()
#     pages_directory = [os.path.join(current_directory, 'helper/pages/mantenedor/')]
#
#     for loader, module_name, is_pkg in pkgutil.walk_packages(pages_directory):
#         module = importlib.import_module('helper.pages.mantenedor.' + module_name)
#         class_ = getattr(module, module_name)
#         instance = class_(context.browser)
#         setattr(context, camel_to_snake(module_name), instance)


def execution_selenium(context):
    if os.getenv('EXECUTION_TYPE') == "localhost":
        print("Tipo de ejecucion : ",os.getenv('EXECUTION_TYPE'))
        context.browser = config_driver_local(context)
        context.browser.delete_all_cookies()
        context.browser.implicitly_wait(20)
        context.browser.set_window_size(1300, 900)
        context.browser.maximize_window()
        context.browser.set_page_load_timeout(time_to_wait=200)
    elif os.getenv('EXECUTION_TYPE') == "hub":
        context.browser = config_driver_selenium_hub(context)
    elif os.getenv('EXECUTION_TYPE') == "saucelabs":
        context.browser = config_driver_saucelab(context)

    # global classes control selenium
    context.window_control = WindowControl(context.browser)
    context.elements = Elements(context.browser)
    context.js_script = JsScript(context.browser)
    context.mouse_action = MouseActions(context.browser)
    context.keyboard_action = KeyboardActions(context.browser)


def config_driver_local(context,):
    name_os = system()
    print("INICIO SET DRIVER EN SO", name_os)
    try:
        if os.getenv('BROWSER') == "chrome":
            rute_driver = str(pathlib.Path().absolute()) + "/helper/selenium_class/web_driver/" + os.getenv('BROWSER') + "/" + name_os + "/chromedriver"
            if name_os == 'Windows':
                rute_driver += ".exe"
            prefs = {"profile.default_content_setting_values.notifications": 2}
            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument("--headless")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_experimental_option("prefs", prefs)
            print(rute_driver)
            context.browser = webdriver.Chrome(executable_path=rute_driver, chrome_options=chrome_options)
        elif os.getenv('BROWSER') == "firefox":
            rute_driver = str(pathlib.Path().absolute()) + "/helper/selenium_class/web_driver/" + os.getenv('BROWSER') + "/" + name_os + "/geckodriver"
            if name_os == 'Windows':
                rute_driver += ".exe"
            rute_driver = rute_driver.replace("\\", "/")
            context.browser = webdriver.Firefox(executable_path=rute_driver)
        elif os.getenv('BROWSER') == "opera":
            rute_driver = str(pathlib.Path().absolute()) + "/helper/selenium_class/web_driver/" + os.getenv('BROWSER') + "/" + name_os + "/operadriver"
            if name_os == "Windows":
                rute_driver += ".exe"
            rute_driver = rute_driver.replace("\\", "/")
            context.browser = webdriver.Opera(executable_path=rute_driver)
        elif os.getenv('BROWSER') == "edge":
            rute_driver = str(pathlib.Path().absolute()) + "/helper/selenium_class/web_driver/" + os.getenv('BROWSER') + "/" + name_os + "/msedgedriver"
            if name_os == "Windows":
                rute_driver += ".exe"
            rute_driver = rute_driver.replace("\\", "/")
            context.browser = webdriver.Edge(executable_path=rute_driver)
        elif os.getenv('BROWSER') == "safari":
            try:
                if name_os == "Windows" or name_os == "Linux":
                    assert False, "Safari is not support in windows or Linux"
                else:
                    context.browser = webdriver.Safari()
            except Exception as exc:
                print("Exception", exc)
                assert False, "not found Safari in your operative system. Remember must be to activate webdriver in MAC "
        return context.browser
    except Exception as exc:
        print("Exception", exc)
        assert False, "Connection webdriver is not correct, you should check connection rute"


def config_driver_selenium_hub(context):
    global options
    # TODO implementar ejecucion en pipeline para el resto de navegadores
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=" + os.getenv('WIDTH_RESOLUTION') + "," + os.getenv('HEIGHT_RESOLUTION'))
        options = chrome_options
        context.browser = webdriver.Remote(command_executor='http://' + os.getenv("SELENIUM_HUB_IP") + ':4444/wd/hub', desired_capabilities=options.to_capabilities())
        return context.browser
    except Exception as exc:
        print("Exception Selenium Hub config", exc)
        assert False, "Connection selenium hub config is not correct, you should check selenium Hub connection"


def config_driver_saucelab(context):
    try:
        if os.getenv('USER_SAUCELAB') is not None and os.getenv('TOKEN_SAUCELAB') is not None and os.getenv('HOST_SAUCELAB') is not None:
            capabilities = {
                'browserName': os.getenv('BROWSER'),
                'browserVersion': os.getenv('BROWSER_VERSION_SELENIUM'),
                'platformName': os.getenv('PLATFORM_NAME_SELENIUM'),
                'sauce:options': {
                }
            }
            context.browser = webdriver.Remote(
                "https://"+os.getenv('USER_SAUCELAB')+":"+os.getenv('TOKEN_SAUCELAB')+"@"+os.getenv('HOST_SAUCELAB')+":443/wd/hub", capabilities)
        return context.browser
    except Exception as exc:
        print("Exception", exc)
        assert False, "Connection saucelab is not correct, you should check saucelab connection"


class SeleniumPlugin:
    """A hook implementation namespace."""

    @PluginSpec.hookimpl
    def before_all(self, context):
        if os.getenv('BROWSER') is None:
            load_dotenv(dotenv_path='.env')
        print("Ejecucion en navegador: ", os.getenv('BROWSER'))
            # assert os.getenv('BROWSER') is not None, "You must to define environment variables"
        print("con RELOADBROWSER en : ", os.getenv('RELOADBROWSER'))
        if os.getenv('RELOADBROWSER') == "false":
            execution_selenium(context)

    @PluginSpec.hookimpl
    def after_all(self, context):
        if os.getenv('RELOADBROWSER') == "false":
            print("cierro driver en after all")
            context.browser.quit()

    @PluginSpec.hookimpl
    def before_scenario(self, context, scenario):
        print("Ejecutando escenario con tag : ", scenario.name)
        if os.getenv('RELOADBROWSER') == "true" and os.getenv('EXECUTION_TYPE') == "localhost":
            execution_selenium(context)

    @PluginSpec.hookimpl
    def after_scenario(self, context, scenario):
        print("Finalizando escenario : ", scenario.name, "con estado", scenario.status)
        if os.getenv('RELOADBROWSER') == "true" and os.getenv('EXECUTION_TYPE') == "localhost":
            context.browser.quit()

