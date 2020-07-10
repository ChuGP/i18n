from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class ElementTextShouldBeProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', 'expected', 'message=None', 'ignore_case=False'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, locator, expected, message=None, ignore_case=False):
            possible_translations = i18n.I18nListener.MAP.value(expected)
            actual_text = ''
            if len(possible_translations) > 1:
                ElementTextShouldBeProxy.show_warning(self, expected, 'Expected')
                BuiltIn().import_library('SeleniumLibrary')
                actual_text = BuiltIn().run_keyword('Get Text', locator)
            else:
                actual_text = possible_translations[0] #only one translation
            actual_text_message = "'%s'is currently resolved as'%s'\n" %(expected, actual_text)
            logger.info(actual_text_message)
            return func(self, BuiltIn().replace_variables(locator), actual_text, message, ignore_case) if actual_text in possible_translations else func(self, BuiltIn().replace_variables(locator), expected, message, ignore_case)
        return proxy
    
    def show_warning(self, expected, name):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_expected = Proxy().deal_warning_message_for_one_word(expected, 'Expected')
        if message_for_expected != '':
            if expected not in i18n.I18nListener.Not_SHOW_WARNING_WORDS:   
                message = language + test_name + message_for_expected + ' '*3 + '\n' + 'You should verify translation is correct!'
                logger.warn(message)
            else:
                message = 'Detail Information\n' + language + message_for_expected + ' '*3  + '\nYou had resolved the multiple translations of the word: \'%s\'' %(expected)
                logger.info(message)