from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.remote.webelement import WebElement
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import sys
import ManyTranslations as ui

class FindElementsProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['by=\'id\'', 'value=None'])] = self

    def i18n_Proxy(self, func):
        def proxy(self, by='id', value=None):
            if isinstance(value, WebElement):
                return func(self, by, value)
            
            full_args = [value]

            BuiltIn().import_library('SeleniumLibrary')
            locator = i18n.I18nListener.MAP.locator(BuiltIn().replace_variables(value), full_args) 
            multiple_translation_words = i18n.I18nListener.MAP.get_multiple_translation_words() 

            is_actual = False
            xpath = ''
            if len(locator) > 1:
                FindElementsProxy.show_warning(self, value, multiple_translation_words, full_args)

                for i, translation_locator in enumerate(locator):
                    xpath += '|' + translation_locator.replace('xpath:', '') if i != 0 else translation_locator.replace('xpath:', '')
                    is_actual = BuiltIn().run_keyword_and_return_status('Get WebElement', translation_locator) 
                    if is_actual:
                        break
                    
                if is_actual:
                    i18n.I18nListener.Is_Multi_Trans = True
                    
                    if str(full_args)+multiple_translation_words[0] not in ui.UI.unique_log:
                        word_translation = i18n.I18nListener.MAP.values(multiple_translation_words, full_args)
                        ui.UI.origin_xpaths_or_arguments.append(full_args)
                        ui.UI.add_trans_info(self, multiple_translation_words, word_translation, full_args, func.__name__)
                        
                    actual_locator_message = "System use the locator:'%s' to run!\n" %translation_locator
                    logger.info(actual_locator_message)
                        
            else:
                xpath = locator[0]
            return func(self, by, BuiltIn().replace_variables(xpath))
        return proxy

    def show_warning(self, locator, multiple_translation_words, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = BuiltIn().get_variable_value("${TEST NAME}")
        message_for_words = Proxy().deal_warning_message_for_list(multiple_translation_words, full_args,  'MULTI_TRANS_WORDS')
        message = language + 'Test Name: ' + test_name + '\n' + 'locator: ' + locator +'\n'+ \
              message_for_words + '\n' + 'You should verify translation is correct!'
        if message_for_words:
            logger.warn(message)