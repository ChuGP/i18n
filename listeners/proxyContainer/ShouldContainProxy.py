from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class ShouldContainProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['container', 'item', 'msg=None', 'values=True', 'ignore_case=False'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, container, item, msg=None, values=True, ignore_case=False):
            ShouldContainProxy.show_warning(self, container, item)
            for translation_container in i18n.I18nListener.MAP.values(container):
                for translation_item in i18n.I18nListener.MAP.value(item):
                    if translation_item in translation_container:
                        return func(self, translation_container, translation_item, msg, values, ignore_case)
            return func(self, container, item, msg, values, ignore_case)
        return proxy
    
    def show_warning(self, container, item):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_container = Proxy().deal_warning_message_for_list(container, 'container')
        message_for_item = Proxy().deal_warning_message_for_one_word(item, 'Expected Contain')
        if message_for_container != '' or message_for_item != '':
            message = language + test_name + message_for_container + ' '*3 + '\n' +  message_for_item + '\n' + 'You should verify translation is correct!'
            logger.warn(message)