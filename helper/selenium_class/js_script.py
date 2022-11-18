
class JsScript:
    """
    Esta clase tiene el propósito de ejecutar acciones desde el lenguaje Javascript
    """
    def __init__(self, browser):
        """
        *Constructor de la clase js*
        """
        self.__browser = browser

    def __str__(self):
        """
        *retorna un string si es llamada la instancia de esta clase*
        """
        return "jsScript class"
    
    def _execute_script(self, str_script, *args):
        """
        *Ejecuta un script libre en lenguaje javascript*

        - `@param str_script: es el str con el script que se desea realizar`
        - `@param *args: Establece una cantidad de parametros indefinidos que son guardados en una lista llamada args`
        """
        

        self.__browser.execute_script(str_script)

    def _execute_script_alert(self, message_alert):
        """
        *Ejecuta un script para mostrar una alerta en el navegador*

        - `@param message_alert: es el mensaje que se mostrará en la alerta`
        """
        assert type(message_alert) == str, "message_alert should be to string type"

        self.__browser.execute_script("alert('"+message_alert+"');")
    
    def _execute_script_scrollHeight(self, height=0, type="full_down"):
        """
        *Ejecuta un scroll mouse en la dirección que se requiera*

        - `@param height: Es solo requerido con el type="down", establece la cantidad de pixeles que irá hacia abajo con el scroll`
        - `@param type: Es para establecer el tipo de scroll, completo hacia final de página, al inicio o con el height especificado`

        """
        height = int(height)

        if type == "full_up":
            self.__browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
        
        elif type == "full_down":
            self.__browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        elif type == "down":
            self.__browser.execute_script("window.scrollTo(0, window.scrollY +"+str(height)+");")

        else:
            assert False, "type variable is not recognize in parameters"

    def _open_new_window(self):
        """
        *Abre una nueva ventana en navegador*

        """

        self.__browser.execute_script("window.open()")

    def _click_element(self, element):
        """
        *hace click en el elemento entregado por los parametros*

        - `@param element: Es el elemento detectado con selenium en la página web`
        """
        assert element != None, "Element not found"
        self.__browser.execute_script("arguments[0].click();", element)

    def _getfile(self):
        """
            *Falta revisarla, es una clase que hicieron los que entregaron en el arquetipo, y no se ha eliminado* 
            *por si es necesaria en el futuro*

        """
        
        file = self.__browser.execute_script(
            '''
            let tag = document.querySelector('downloads-manager').shadowRoot;
            let div = tag.querySelector('downloads-item').shadowRoot;
            let file = div.getElementById('file-link');
            return file;
            '''
        )

        return file



    