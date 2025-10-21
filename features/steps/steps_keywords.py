from behave import given, when, then
import time
from allure_commons.types import AttachmentType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from helper.pages.page_whatsapp import PageWhatsapp
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


@given('ingreso a WhatsApp Web y abro el chat con "{contacto}"')
def step_ingreso_whatsapp(context, contacto):
    """Abre WhatsApp Web y selecciona el chat indicado."""
    page = PageWhatsapp(context.browser)
    context.browser.get("https://web.whatsapp.com")

    # Espera que cargue el buscador del chat
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located(page.chat_search_box)
    )
    search_box = context.browser.find_element(*page.chat_search_box)
    search_box.click()
    search_box.clear()
    search_box.send_keys(contacto)

    # Espera y selecciona el chat
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located(page.chat_result(contacto))
    )
    context.browser.find_element(*page.chat_result(contacto)).click()

    # Espera a que cargue la caja de texto del chat
    WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located(page.chat_input_box)
    )
    print("✅ Chat abierto correctamente")


@when('envío el mensaje "{mensaje_reseteo}" para reiniciar el bot')
def step_envio_reseteo(context, mensaje_reseteo):
    """Envía el mensaje de reseteo y espera respuesta del bot."""
    page = PageWhatsapp(context.browser)
    box = WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located(page.chat_input_box)
    )
    box.click()
    box.send_keys(mensaje_reseteo)
    box.send_keys(Keys.ENTER)
    print(f"📨 Enviado: {mensaje_reseteo}")

    # Esperar nueva respuesta del bot
    prev_msg = page.get_last_bot_text()
    WebDriverWait(context.browser, 60, poll_frequency=1).until(
        lambda d: (msg := page.get_last_bot_text()) and msg != prev_msg
    )
    context.last_bot_reply = page.get_last_bot_text()
    print(f"🤖 Bot respondió: {context.last_bot_reply}")


@when('envío la palabra clave "{keyword}"')
def step_envio_keyword(context, keyword):
    """Envía una palabra clave y espera la respuesta del bot."""
    page = PageWhatsapp(context.browser)
    prev_msg = page.get_last_bot_text()

    box = WebDriverWait(context.browser, 40).until(
        EC.presence_of_element_located(page.chat_input_box)
    )
    box.click()
    box.send_keys(keyword)
    box.send_keys(Keys.ENTER)
    print(f"📨 Enviado: {keyword}")

    WebDriverWait(context.browser, 60, poll_frequency=1).until(
        lambda d: (msg := page.get_last_bot_text()) and msg != prev_msg
    )
    context.keyword_reply = page.get_last_bot_text()
    print(f"🤖 Bot respondió: {context.keyword_reply}")



@then('valido la respuesta del chat bot')
def step_valido_respuesta(context):
    page = PageWhatsapp(context.browser)
    driver = context.browser

    print("⏳ Esperando el ÚLTIMO bloque del bot con la pregunta '¿Aceptas los términos y condiciones?'...")

    # Guarda el texto previo del bot
    texto_anterior = page.get_last_bot_text()

    # Forzamos scroll al fondo (WhatsApp Web usa virtualización)
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    try:
        # Esperar hasta que aparezca un nuevo bloque que contenga la pregunta exacta
        WebDriverWait(driver, 60, poll_frequency=1).until(
            lambda d: (
                (mensajes := d.find_elements(By.XPATH, "//div[contains(@class,'message-in')]"))
                and "¿aceptas los términos y condiciones" in mensajes[-1].text.lower()
                and mensajes[-1].text.strip() != texto_anterior
            )
        )

        # Tomar el último bloque detectado
        ultimo_mensaje = driver.find_elements(By.XPATH, "//div[contains(@class,'message-in')]")[-1]
        texto_ultimo = ultimo_mensaje.text.strip()
        print(f"🟢 Último bloque detectado correctamente:\n{texto_ultimo}")

        # 🕒 Esperar 3 segundos antes de cerrar el escenario (permite ver el mensaje en pantalla)
        time.sleep(3)
        print("⏸️ Espera de 3 segundos completada. Cerrando escenario...")

    except TimeoutException:
        # Esperar también 3 segundos en caso de fallo, para debug visual
        time.sleep(3)
        raise AssertionError("❌ No apareció el bloque con '¿Aceptas los términos y condiciones?' dentro del tiempo esperado (60 s).")
