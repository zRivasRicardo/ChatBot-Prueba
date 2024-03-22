import re
from datetime import datetime

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
from selenium.webdriver.chrome.service import Service


def camel_to_snake(text):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()


def execution_selenium(context):
    if os.getenv('EXECUTION_TYPE') == "localhost":
        context.browser = config_driver_local(context)
    elif os.getenv('EXECUTION_TYPE') == "hub":
        context.browser = config_driver_selenium_hub(context)
    elif os.getenv('EXECUTION_TYPE') == "selenoid":
        context.browser = config_driver_selenoid(context)
    elif os.getenv('EXECUTION_TYPE') == "saucelabs":
        context.browser = config_driver_saucelab(context)
    else:
        assert False, "Selenium config is not correct, you should check file readme.md"
    context.browser.delete_all_cookies()
    context.browser.implicitly_wait(20)
    context.browser.maximize_window()
    context.browser.set_page_load_timeout(time_to_wait=200)

    context.window_control = WindowControl(context.browser)
    context.elements = Elements(context.browser)
    context.js_script = JsScript(context.browser)
    context.mouse_action = MouseActions(context.browser)
    context.keyboard_action = KeyboardActions(context.browser)


def config_driver_local(context, ):
    name_os = system()
    try:
        rute_driver = str(pathlib.Path().absolute()) + "/helper/selenium_class/web_driver/" + os.getenv('BROWSER') + "/" + name_os+"/"
        rute_driver = rute_driver.replace("\\", "/")
        if os.getenv('BROWSER') == "chrome":
            rute_driver += "chromedriver"
            if name_os == 'Windows':
                rute_driver += ".exe"
            prefs = {"profile.default_content_setting_values.notifications": 2}
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_experimental_option("prefs", prefs)
            context.browser = webdriver.Chrome(service=Service(executable_path=rute_driver), options=chrome_options)
        elif os.getenv('BROWSER') == "firefox":
            rute_driver += "geckodriver"
            if name_os == 'Windows':
                rute_driver += ".exe"
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.binary_location = r'/Applications/Firefox.app/Contents/MacOS/firefox'
            context.browser = webdriver.Firefox(service=Service(executable_path=rute_driver), options=firefox_options)
        elif os.getenv('BROWSER') == "opera":
            rute_driver += "operadriver"
            if name_os == "Windows":
                rute_driver += ".exe"
            opera_options = webdriver.ChromeOptions
            #opera_options.add_experimental_option( 'w3c', True)
            opera_options.binary_location = r'/Applications/Opera.app/Contents/MacOS/Opera'
            context.browser = webdriver.Chrome(service=Service(executable_path=rute_driver), options=opera_options)
        elif os.getenv('BROWSER') == "edge":
            rute_driver = rute_driver + "msedgedriver"
            if name_os == "Windows":
                rute_driver += ".exe"
            context.browser = webdriver.Edge(service=Service(executable_path=rute_driver))
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
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=" + os.getenv('WIDTH_RESOLUTION') + "," + os.getenv('HEIGHT_RESOLUTION'))
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
                'sauce:options': {}
            }
            context.browser = webdriver.Remote("https://" + os.getenv('USER_SAUCELAB') + ":" + os.getenv('TOKEN_SAUCELAB') + "@" + os.getenv('HOST_SAUCELAB') + ":443/wd/hub", capabilities)
        return context.browser
    except Exception as exc:
        print("Exception", exc)
        assert False, "Connection saucelab is not correct, you should check saucelab connection"


def config_driver_selenoid(context):
    try:
        if os.getenv('SELENIUM_HUB_IP') is not None and os.getenv('BROWSER') is not None and os.getenv('BROWSER_VERSION_SELENIUM') is not None and os.getenv('PROYECTO') is not None:
            if os.getenv('BROWSER') == "chrome" or os.getenv('BROWSER') == "opera":
                option = webdriver.ChromeOptions()
            elif os.getenv('BROWSER') == "firefox":
                option = webdriver.FirefoxOptions()
            else:
                assert False, "No existe un driver en selenoid para el navegador"+os.getenv('BROWSER')

            option.set_capability("browserVersion", os.getenv("BROWSER_VERSION_SELENIUM"))
            option.set_capability("browserName", os.getenv("BROWSER"))

            selenoid_options = {
                "enableVideo": False,
                "enableVNC": True,
                "w3c": True
                #"enableLog": False,
                #"name": os.getenv("PROYECTO"),
                #"videoName": os.getenv("PROYECTO")+"_video_auto" + datetime.now().strftime('%H-%M-%S') + ".mp4",
                #"sessionTimeout": "24h"
            }
            option.set_capability("selenoid:options", selenoid_options)
            context.browser = webdriver.Remote(command_executor="http://"+os.getenv("SELENIUM_HUB_IP")+":4444/wd/hub", options=option)
            context.browser.maximize_window()
            return context.browser
        else:
            assert False, "Environment selenoid config is not correct, you should check envireonment in file .env"
    except Exception as exc:
        print("Exception Selenoid config ->", exc)
        assert False, "Connection selenoid config is not correct, you should check selenoid connection"


class SeleniumPlugin:
    """A hook implementation namespace."""

    @PluginSpec.hookimpl
    def before_all(self, context):
        load_dotenv(dotenv_path='.env')
        print("> SO :", system())
        print("> EXECUTION_TYPE :", os.getenv('EXECUTION_TYPE'))
        print("> SELENIUM_HUB_IP : ", os.getenv('SELENIUM_HUB_IP'))
        print("> BROWSER : ", os.getenv('BROWSER'))
        print("> RELOADBROWSER : ", os.getenv('RELOADBROWSER'))
        print("> EXECUTION_PARALLEL : ", os.getenv('EXECUTION_PARALLEL'))
        if os.getenv('RELOADBROWSER') == "false":
            execution_selenium(context)

    @PluginSpec.hookimpl
    def after_all(self, context):
        if os.getenv('RELOADBROWSER') == "false":
            print("> CIERRO DRIVER EN AFTER ALL")
            context.browser.quit()

    @PluginSpec.hookimpl
    def before_scenario(self, context, scenario):
        print("> EJECUTANDO ESCENARIO CON EL TAG : ", scenario.name)
        if os.getenv('RELOADBROWSER') == "true":
            execution_selenium(context)

    @PluginSpec.hookimpl
    def after_scenario(self, context, scenario):
        print("> FINALIZANDO ESCENARIO CON TAG : ", scenario.name, "con estado", scenario.status)
        if os.getenv('RELOADBROWSER') == "true":
            context.browser.quit()

