from selenium.webdriver.common.by import By

class PageWhatsapp:
    def __init__(self, browser):
        self.browser = browser

        # 🟢 Campo de búsqueda y de chat
        self.chat_search_box = (By.XPATH, "//div[@contenteditable='true' and @data-tab='3']")
        self.chat_input_box = (By.XPATH, "//div[@contenteditable='true' and @data-tab='10']")

        # 🟢 Último mensaje recibido del bot
        self.last_bot_message = (
            By.XPATH,
            "//div[@class='_akbu x6ikm8r x10wlt62']"
        )

        # 🟢 Mensaje final esperado de cierre
        self.msg_visible_final = (
            By.XPATH,
            "//span[text()[contains(.,'Si quieres volver a escribirnos, solo mándanos un “hola”.')]]"
        )

        # 🟢 Botón “Sí” del ÚLTIMO bloque del bot que contenga “términos y condiciones”
        self.last_btn_si = (
            By.XPATH,
            "("
            "//div[contains(@class,'message-in')]"
            "[.//span[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜ', "
            "'abcdefghijklmnopqrstuvwxyzáéíóúü'), 'términos y condiciones')]]"
            "//div[@role='button']//span[normalize-space()='Sí' or normalize-space()='Si']"
            ")[last()]"
        )
        # 🟢 Mensaje entrante posterior al último mensaje del usuario
        # Solo toma el primer 'message-in' que venga después del último 'message-out'
        self.next_incoming_message_after_user = (
            By.XPATH,
            "(//div[contains(@class,'message-in')])[last()]"
        )


        # 🟢 Texto esperado dentro del nuevo bloque recibido
        self.accept_terms_text = (
            By.XPATH,
            ".//strong[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
            "'¿aceptas los términos y condiciones?')]"
        )

        
    def chat_result(self, contacto):
        """Devuelve el localizador dinámico del chat según el nombre del contacto."""
        return (By.XPATH, f"//span[@title='{contacto}']")

    def get_last_bot_text(self):
        """Devuelve el texto del último mensaje recibido del bot."""
        try:
            elementos = self.browser.find_elements(*self.last_bot_message)
            if elementos:
                texto = elementos[-1].text.strip()
                print(f"📨 Último mensaje detectado del bot: {texto}")
                return texto
            else:
                print("⚠️ No se encontraron mensajes del bot todavía.")
                return ""
        except Exception as e:
            print(f"❌ Error obteniendo el último mensaje del bot: {e}")
            return ""
