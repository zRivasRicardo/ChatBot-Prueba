from selenium.webdriver.common.action_chains import ActionChains

class MouseActions:
    """
        This class validates the mouse actions elements
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
        return "class mouse action"

    def _execute_actions(self):
        """
        *Performs all stored actions*
        """

        self.__action.perform()

    def _click_left_action(self, on_element=None):
        """
        *Left click on element*

        - `@param on_element: The element to click. if element is None, click on current mouse position`
        """

        self.__action.click(on_element)

    def _click_and_hold_left_action(self, on_element=None):
        """
        *Holds down the left mouse button on an element*

        - `@param on_element: Element to mouse down. if None, click on current mouse position`
        """

        self.__action.click_and_hold(on_element)

    def _context_click_right_action(self, on_element=None):
        """
        *Performs a context-click(right click) on an element*

        - `@param on_element: The element to context click. If None, clicks on current mouse position`
        """

        self.__action.context_click(on_element)

    def _double_click_left_action(self, on_element=None):
        """
        *Double click an element*

        - `@param on_element: The element to double click. If None, clicks on current mouse position`
        """

        self.__action.double_click(on_element)

    def _drag_and_drop(self, source, target):
        """
        *Holds down the left mouse button on the source element, then move to target element and releases the mouse button*

        - `@param source: The element to mouse down`
        - `@param target: The element to mouse up`
        """
        assert source != None, "Element source not found"
        assert target != None, "Element target not found"

        self.__action.drag_and_drop(source, target)

    def _drag_and_drop_by_offset(self, source, xoffset, yoffset):
        """
        *Holds down left mouse button on the source element, then moves to the target offset and releases the mouse button*

        - `@param source: The element to mouse down`
        - `@param xoffset: X offset to move to`
        - `@param yoffset: Y offset to move to`
        """
        assert source != None, "Element source not found"
        assert type(xoffset) == int, "xoffset should be to int variable"
        assert type(yoffset) == int, "yoffset should be to int variable"

        self.__action.drag_and_drop_by_offset(source, xoffset, yoffset)
    
    def _move_by_offset(self, xoffset, yoffset):
        """
        *Moving the mouse to an offset from current mouse position*

        - `@param xoffset: X offset to move to, as a posible or negative integer`
        - `@param yoffset: Y offset to move to, as a posible or negative integer`
        """
        assert type(xoffset) == int, "xoffset should be to int variable"
        assert type(yoffset) == int, "yoffset should be to int variable"

        self.__action.move_by_offset(xoffset, yoffset)

    def _move_to_element(self, to_element):
        """
        *Moving the mouse to the middle of and element*

        - `@param to_element: The web element to move to`
        """
        assert to_element != None, "Element not found"

        self.__action.move_to_element(to_element)

    def _move_to_element_with_offset(self, to_element, xoffset, yoffset):
        """
        *Move the mouse by and offset of the specified element. Offset are relative to the top-left corner of element*

        - `@param to_element: The web element to move to`
        - `@param xoffset: X offset to move to`
        - `@param yoffset: Y offset to move to`
        """
        assert type(xoffset) == int, "xoffset should be to int variable"
        assert type(yoffset) == int, "yoffset should be to int variable"
        assert to_element != None, "Element not found"

        self.__action.move_to_element_with_offset(to_element, xoffset, yoffset)

    def _pause_actions(self, time):
        """
        *Pause all inputs for the specified duration in seconds*

        - `@param time: Time in seconds to pause`
        """

        assert type(time) == int, "Variable time must be a integer"
        
        self.__action.pause(time)

    def _release_held_mouse(self, on_element=None):
        """
        *Releasing a held mouse button on an element*
        
        - `@param on_element: The element to mouse up. If None`
        """

        self.__action.release(on_element)

    def _reset_actions(self):
        """
        *Clears actions that are already stored locally and on the remote end*
        """

        self.__action.reset_actions()