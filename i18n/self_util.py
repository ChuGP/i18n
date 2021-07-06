from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from selenium import webdriver

class self_util():
    @keyword(name='Scroll To The End')
    def scroll_to_the_end(self):
        selenium = BuiltIn().get_library_instance('SeleniumLibrary')
        selenium.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

