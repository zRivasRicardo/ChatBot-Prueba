import os
import pluggy
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from helper.plugins.AllurePlugin import AllurePlugin
from helper.plugins.DBPlugin import BDPlugin
from helper.plugins.PluginSpec import PluginSpec
from helper.plugins.RerunPlugin import RerunPlugin
from helper.plugins.qalityplusPlugin import QAlityPlusPlugin

load_dotenv()

pm = pluggy.PluginManager("hooks")
pm.add_hookspecs(PluginSpec)

pm.register(RerunPlugin())
pm.register(AllurePlugin())
pm.register(BDPlugin())
pm.register(QAlityPlusPlugin())


def before_all(context):
    print("> EJECUCIÓN LOCAL ACTIVADA")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # ✅ Crea un perfil de Chrome propio para automatización (sin bloqueo)
    # Usa una copia del perfil real (solo la primera vez debes loguearte a WhatsApp)
# ✅ Crea un perfil de Chrome propio para automatización (sin bloqueo)
# Usa una copia del perfil real (solo la primera vez debes loguearte a WhatsApp)
    user_dir = os.path.expanduser("~")
    profile_path = os.path.join(user_dir, "Desktop", "chrome_whatsapp_persist")
    os.makedirs(profile_path, exist_ok=True)
    chrome_options.add_argument(f"--user-data-dir={profile_path}")

    # 🚫 No pongas "--profile-directory", eso bloquea DevToolsActivePort
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--remote-debugging-port=9222")


    try:
        service = Service(ChromeDriverManager().install())
        context.browser = webdriver.Chrome(service=service, options=chrome_options)
        context.browser.implicitly_wait(10)
        pm.hook.before_all(context=context)
        print("✅ Chrome iniciado con perfil persistente de WhatsApp.")
    except Exception as e:
        print(f"❌ Error iniciando Chrome: {e}")
        raise


def after_all(context):
    try:
        context.browser.quit()
    except Exception:
        pass
    pm.hook.after_all(context=context)


def before_tag(context, tag):
    pm.hook.before_tag(context=context, tag=tag)


def after_tag(context, tag):
    pm.hook.after_tag(context=context, tag=tag)


def before_feature(context, feature):
    pm.hook.before_feature(context=context, feature=feature)


def after_feature(context, feature):
    pm.hook.after_feature(context=context, feature=feature)


def before_scenario(context, scenario):
    pm.hook.before_scenario(context=context, scenario=scenario)


def after_scenario(context, scenario):
    pm.hook.after_scenario(context=context, scenario=scenario)


def before_step(context, step):
    pm.hook.before_step(context=context, step=step)


def after_step(context, step):
    pm.hook.after_step(context=context, step=step)
