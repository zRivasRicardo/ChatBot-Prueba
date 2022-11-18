

class WindowControl:
    """
        Change windowBrowser, alerts or frames
    """
    def __init__(self, browser):
        """
        *Constructor class*
        """
        self._browser = browser

    def __str__(self):
        """
        *Return importart variables of class*

        - `@return: importart variabnles`
        """
        return "important variables"

    def _go_to_url(self, url):
        """ 
        *The method to ingress to url*

        - `@param url: string url to go to view`
        """
        assert type(url) == str, "url must be a string variable"
        assert url != "", "url is empty"

        self._browser.get(url)
        
        assert self._browser.current_url != "data:,", "The url is empty"
    
    def _get_current_url(self):
        """ 
        *Get current url in web*

        - `@return: url that current browser index`
        """
        url = self._browser.current_url
        return url

    def _change_window_browser(self, num_window):
        """
        *Change windows in selenium*

        - `@param num_window: is the number of window opened. must be to a integer value`
        """

        assert type(num_window) == int, "num_window must be integer"
        assert num_window >= 0, "num_windows must be between 0 to infinite"

        self._browser.switch_to.window(self._browser.window_handles[num_window])

    def _get_list_window_handles(self):
        """
        *get list of all window in driver*

        - `@return: list of ID of window handles of browser`
        """
        return self._browser.window_handles
    
    def _get_current_window_handle(self):
        """
        *get current window that is show in driver*

        - `@return: Id of current window`
        """
        return self._browser.current_window_handle

    def _get_title_current_window(self):
        """
        *get title of current window*

        - `@return: title of current window`
        """
        return self._browser.title

    def _maximize_window(self):
        """
        *Maximize window that use driver*
        """

        self._browser.maximize_window()
        

    def _refresh_window(self):
        """
        *Refresh window that use driver*
        """

        self._browser.refresh()

    def _take_screenshot_window(self, str_name_image):
        """
        *Take a screenshot to current window*

        - `@param str_name_image: name that you want named to image`
        """
        assert type(str_name_image) == str, "str_name_image parameter must be a string variable"

        self._browser.save_screenshot(str_name_image+".png")
    
    def _get_cookies(self):
        """
        *get cookies in pages*

        - `@return: the list of cookies`
        """
        return self._browser.get_cookies()

    def _change_resolution(self, x=1920, y=1080, num_window=0):
        """
        *change resolution of explorer*

        - `@param x: resolution of x`
        - `@param y: resolution of y`
        - `@param num_window: value integer between 0 and infinite`
        """
        assert type(x) == int, "x parameters must be a integer"
        assert type(y) == int, "y parameters must be a integer"
        assert type(num_window) == int, "num_window must be integer"
        assert num_window >= 0, "num_windows must be between 0 to infinite"

        self._browser.set_window_size(x, y, self._browser.window_handles[num_window])

    def _get_text_alert(self):
        """
        *Get text in string var to alert*

        - `@return: String var that have text alert`
        """

        alert_obj = self._browser.switch_to.alert

        return alert_obj.text

    def _get_window_size(self):
        """
        *Get widows size*

        - `@return: values of width and height of resolution`
        """

        return self._browser.get_window_size()

    def _accept_alert(self):
        """
        *Select accept in options to alert*
        """
        alert_obj = self._browser.switch_to.alert

        alert_obj.accept()
    
    def _dismiss_alert(self):
        """
        *Select dismiss in options to alert*
        """
        alert_obj = self._browser.switch_to.alert

        alert_obj.dismiss()

    def _send_text_alert(self, text_send):
        """
        *Send text to alert*
        
        - `@param text_send: string to write in alert`
        """
        assert type(text_send) == str, "text_send parameter must be a string variable"

        alert_obj = self._browser.switch_to.alert

        alert_obj.send_keys(text_send)
