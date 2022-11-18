from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

class Elements:
    """
        This class validates the elements items
    """
    def __init__(self, browser):
        """
        *Constructor of class*

        - `@param browser: The internet browser driver used`
        """
        self.__browser = browser

    def __str__(self):
        """
        *If you print the variable of the instantiated class it returns the string of this method*

        - `@return: The important variables of the class`
        """
        return "elements"
    

    def _find_element(self, url_element, type="xpath"):
        """
        *Find elements in web*

        - `@param url_element: string of url element`
        - `@param type: method to use to find element`
        - `@return: element found`
        """
        element = None
        try:
            if type == "xpath":
                element = self.__browser.find_element_by_xpath(url_element)
            elif type == "id":
                element = self.__browser.find_element_by_id(url_element)
            elif type == "name":
                element = self.__browser.find_element_by_name(url_element)
            elif type == "link_text":
                element = self.__browser.find_element_by_link_text(url_element)
            elif type == "partial_link_text":
                element = self.__browser.find_element_by_partial_link_text(url_element)
            elif type == "tag_name":
                element = self.__browser.find_element_by_tag_name(url_element)
            elif type == "class_name":
                element = self.__browser.find_element_by_class_name(url_element)
            elif type == "css_selector":
                element = self.__browser.find_element_by_css_selector(url_element)
            else:
                assert False, "Type parameters not found"

            assert element != None, "No element found"

            return element

        except:
            assert False, "No element found, you should verify parameters in function"

        
    
    def _sub_find_element(self, url_element, element, type="xpath"):
        """
        *Find elements in web*

        - `@param url_element: string of url element`
        - `@param element: element to find element`
        - `@param type: method to use to find element`
        - `@return: element found`
        """
        try:
            if type == "xpath":
                element = element.find_element_by_xpath(url_element)
            elif type == "id":
                element = element.find_element_by_id(url_element)
            elif type == "name":
                element = element.find_element_by_name(url_element)
            elif type == "link_text":
                element = element.find_element_by_link_text(url_element)
            elif type == "partial_link_text":
                element = element.find_element_by_partial_link_text(url_element)
            elif type == "tag_name":
                element = element.find_element_by_tag_name(url_element)
            elif type == "class_name":
                element = element.find_element_by_class_name(url_element)
            elif type == "css_selector":
                element = element.find_element_by_css_selector(url_element)
            else:
                assert False, "Type parameters not found"

            assert element != None, "No element found"

            return element

        except:
            assert False, "No element found, you should verify parameters in function"

        
    
    def _find_elements(self, url_element, type="xpath"):
        """ 
        *Find elements in web*

        - `@param url_element: string of url elements`
        - `@param type: method to use to find elements`
        - `@return: list elements found`
        """
        elements = None
        try:
            if type == "xpath":
                elements = self.__browser.find_elements_by_xpath(url_element)
            elif type == "id":
                elements = self.__browser.find_elements_by_id(url_element)
            elif type == "name":
                elements = self.__browser.find_elements_by_name(url_element)
            elif type == "link_text":
                elements = self.__browser.find_elements_by_link_text(url_element)
            elif type == "partial_link_text":
                elements = self.__browser.find_elements_by_partial_link_text(url_element)
            elif type == "tag_name":
                elements = self.__browser.find_elements_by_tag_name(url_element)
            elif type == "class_name":
                elements = self.__browser.find_elements_by_class_name(url_element)
            elif type == "css_selector":
                elements = self.__browser.find_elements_by_css_selector(url_element)
            else:
                assert False, "Type parameters not found"

            assert elements != None, "No elements found"

            return elements
        except:
            assert False, "No element found, you should verify parameters in function"

    def _sub_find_elements(self, url_element, element, type="xpath"):
        """ 
        *Find elements in web*

        - `@param url_element: string of url elements`
        - `@param element to find element`
        - `@param type: method to use to find elements`
        - `@return: list elements found`
        """
        try:
            if type == "xpath":
                elements = element.find_elements_by_xpath(url_element)
            elif type == "id":
                elements = element.find_elements_by_id(url_element)
            elif type == "name":
                elements = element.find_elements_by_name(url_element)
            elif type == "link_text":
                elements = element.find_elements_by_link_text(url_element)
            elif type == "partial_link_text":
                elements = element.find_elements_by_partial_link_text(url_element)
            elif type == "tag_name":
                elements = element.find_elements_by_tag_name(url_element)
            elif type == "class_name":
                elements = element.find_elements_by_class_name(url_element)
            elif type == "css_selector":
                elements = element.find_elements_by_css_selector(url_element)
            else:
                assert False, "Type parameters not found"

            assert elements != None, "No elements found"

            return elements
        except:
            assert False, "No element found, you should verify parameters in function"

    def _click_element(self, element):
        """
        *click in element in web*

        - `@param element: element to do click`
        """
        assert element != None, "Element is not found"
        try:
            element.click()
        except:
            assert False, "Click element is not working, you should check elements parameter"

    def _send_text_in_element(self, text, element):
        """
        *Write a string in the element*

        - `@param text: String to write`
        - `@param element: Element to write a string`
        """
        assert type(text) == str, "Text must be a string"
        try:
            element.send_keys(text)
        except:
            assert False, "send text in element failed, you should check parameters"

    def _get_text_in_element(self, element):
        """
        *Get text in element container*

        - `@param element: element to search text`
        """
        assert element != None, "Element not found"
        return element.text

    def _get_attribute_in_element(self, element, value):
        """
        *Get attribute of element container*

        - `@param element: element to get attribute`
        - `@param value: Value of attribute in element to search`
        - `@return: value of attribute to search`
        """
        assert (value != "" or value != None or type(value)!=str), "value is None or is empty string"
        assert element != None, "Element not found"

        return element.get_attribute(value)
    
    def _get_location_element(self, element):
        """
        *Get location of element in browser*

        - `@param element: element to get location`
        """
        assert element != None, "Element not found"

        return element.location

    def _get_size_element(self, element):
        """
        *Get size of element in browser*

        - `@param element: element to get size`
        """
        assert element != None, "Element not found"

        return element.size

    def _element_is_selected(self, element):
        """
        *Verify if element is selected*

        - `@param element: element to check is selected`
        - `@return: True or False if elements is selected`
        """
        assert element != None, "Element not found"

        return element.is_selected()

    def _element_is_displayed(self, element):
        """
        *Verify if element is displayed*

        - `@param element: element to check is displayed`
        - `@return: True or False if elements is displayed`
        """
        assert element != None, "Element not found"

        return element.is_displayed()

    def _element_is_enabled(self, element):
        """
        *Verify if element is enabled*

        - `@param element: element to check is enabled`
        - `@return: True or False if elements is enabled`
        """
        assert element != None, "Element not found"

        return element.is_enabled()

    def _clear_text_in_element(self, element):
        """
        *clear text in field*

        - `@param element: element to clear text`
        """

        assert element != None, "Element not found"
        element.clear()
    
    def _screenshot_element(self, element, str_name_image_screenshot):
        """
        *Take a screenshot of element*

        - `@param element: element to take a screenshot`
        - `@param str_name_image_screenshot: String to save screenshot of element`
        """

        assert element != None, "Element not found"
        assert (str_name_image_screenshot != "" or str_name_image_screenshot != None), "Error: str_name_image_screenshot is not correct"
        element.screenshot(str_name_image_screenshot+".png")


    def _find_tag_name_in_element(self, element):
        """
        *find tag name of element container*

        - `@param element: element to find tag name`
        - `@return: tag name of element`
        """
        assert element != None, "Element not found"
        
        return element.tag_name

    def _find_parent_element(self, element, type="xpath"):
        """
        *find parent of element*

        - `@param element: element to find his parent`
        - `@return: parent of elemento in format element selenium`
        """
        try:
            parent = None

            if type == "xpath":
                parent = element.find_element_by_xpath("..")
            elif type == "id":
                parent = element.find_element_by_id("..")
            elif type == "name":
                parent = element.find_element_by_name("..")
            elif type == "link_text":
                parent = element.find_element_by_link_text("..")
            elif type == "partial_link_text":
                parent = element.find_element_by_partial_link_text("..")
            elif type == "tag_name":
                parent = element.find_element_by_tag_name("..")
            elif type == "class_name":
                parent = element.find_element_by_class_name("..")
            elif type == "css_selector":
                parent = element.find_element_by_css_selector("..")
            else:
                assert False, "Type parameters not found"

            assert parent != None, "No element parent found"

            return parent
        except:
            assert False, "Element not have parent"


    def _wait_implicitly(self, time):
        """
        *Wait implicitly a time (in seconds) to load in page*

        - `@param time: Seconds to wait load page`
        """
        assert type(time) == int, "Value of time is not integer"

        self.__browser.implicitly_wait(time)

    ########################### review classes
    def create_select_option(self, value, id):
        """
        *crea un select y va seleccionando de acuerdo al valor que llega de afuera del metodo*
        """
        select_element = self.browser.find_element_by_id(id)
        select_options = Select(select_element)
        select_options.select_by_value(value)


    def select_date(self):
        """
        *Crea un select para los meses y otro para los años y selecciona de acuerdo a los valores que pasamos entre los parentesis,*
        *no recibe parametros desde afuera, los parametros los pasamos directo dentro del metodo*
        """
        div = self.browser.find_element_by_id("rangeDatePicker")
        select_month = Select(div.find_element_by_css_selector("select[title='Select month']"))
        select_year = Select(div.find_element_by_css_selector("select[title='Select year']"))
        select_month.select_by_visible_text("May")
        select_year.select_by_value("2010")

    def show_correct_date(self):
        """
        *Valida que el mes y el año seleccionado sean los que esperamos, no recibe parametros desde afuera, se los pasamos*
        *directo dentro del metodo*
        """
        div = self.browser.find_element_by_id("rangeDatePicker")
        select_month = Select(div.find_element_by_css_selector("select[title='Select month']"))
        select_year = Select(div.find_element_by_css_selector("select[title='Select year']"))
        month = self.browser.find_elements_by_xpath("//div[contains(@class, 'ngb-dp-month-name')]")
        if select_month.first_selected_option.get_attribute(
                'text') == "May" and select_year.first_selected_option.get_attribute('text') == "2010":
            if month[0].text == "May 2010" and month[1].text == "Jun 2010":
                assert True

    def _implicity_wait(self,time, element_by = By):
        try:
            element = WebDriverWait(self.__browser, time).until(expected_conditions.presence_of_element_located(element_by))
        except Exception as ex:
            print(ex)
            assert element != None, "Elemento no encontrado en el dom : "+element
        return element