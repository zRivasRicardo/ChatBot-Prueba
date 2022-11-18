from selenium.webdriver.common.by import By

class PageModel:
    def __init__(self, browser):
        self.browser = browser

    by_search_box = (By.XPATH, "//h1[text()='¡Bienvenidos a HakaTools!']")
    card_element = (By.XPATH, "//h2[text()='Formularios']")
    txt_first_name = (By.ID, "first_name")
    txt_email = (By.ID, "email")
    txt_direccion = (By.ID, "currentAddress")
    txt_direccion_permanente = (By.ID, "permanentAddress")
    btn_enviar = (By.ID, "submitBasicForm")
    txt_result_form = (By.ID, "resultBasicForm")
