from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class KeyboardActions:
    """
        This class validates the keyboard actions elements
    """
    def __init__(self, browser):
        """
        *Constructor of class*

        - `@param browser: The internet browser driver used`
        """
        
        self.__browser = browser
        self.__action = ActionChains(self.__browser)
    
    def __str__(self):
        """
        *If you print the variable of the instantiated class it returns the string of this method*

        - `@return: The important variables of the class`
        """

        return "class keyboard actions"

    def _key_down(self, value, element=None):
        """
        *Send a key press only , without releasing it. Should only be used with modifier keys (Control, Alt and Shift)*

        - `@param value: The modifier key to send. Values are defined in keys class`
        - `@param element: The element to send keys. If None, sends a keys to current focused element`
        """

        res = self._get_special_keys(value)

        self.__action.key_down(res, element)

    def _key_up(self, value, element=None):
        """
        *Release a modifier key*

        - `@param value: The modifier key to send. Values are defined in keys class`
        - `@param element: The element to send keys. If None, sends a keys to current focused element`
        """

        res = self._get_special_keys(value)

        self.__action.key_up(res, element)

    def _send_keys(self, keys_to_send):
        """
        *Sends keys to current focused element*

        - `@param keys_to_send: The string to send`
        """

        assert type(keys_to_send) == str, "The keys must be a string"

        self.__action.send_keys(keys_to_send)
    
    def _send_keys_to_element(self, element, keys_to_send):
        """
        *Sends keys to an element*

        - `@param element: The element to send keys`
        - `@param keys_to_send: The keys to send. Modifier keys constants can be found in the keys class`
        """

        assert type(keys_to_send) == str, "The keys must be a string"
        assert element != None, "Element not found"

        self.__action.send_keys_to_element(element, keys_to_send)

    def _execute_actions(self):
        """
        *Performs all stored actions*
        """

        self.__action.perform()

    def _move_to_right(self, element, times):
        """
        *move to right keyboard*
        """

        for i in range(times):
            element.send_keys(Keys.RIGHT)