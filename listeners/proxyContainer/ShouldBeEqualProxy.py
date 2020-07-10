from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n

class ShouldBeEqualProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['first', 'second', 'msg=None', 'values=True', 'ignore_case=False'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, first, second, msg=None, values=True, ignore_case=False):
            if 'not' in func.__name__:
                compare = lambda x,y:True if x != y else False
            else:
                compare = lambda x,y:True if x == y else False
            ShouldBeEqualProxy.show_warning(self, first, second)
            for first_translation in i18n.I18nListener.MAP.value(first):
                for second_translation in i18n.I18nListener.MAP.value(second):
                    if compare(first_translation,second_translation):
                        return func(self, first_translation, second_translation, msg, values, ignore_case)
            return func(self, first, second, msg, values, ignore_case)
        return proxy
    
    def deal_translate_message(self, value, message_title):
        translation = i18n.I18nListener.MAP.value(value)[0]
        if value != translation:
            message = ('%s argument evaluates to' + ' ' + '\'%s\'' + ' is translated to: ' + '\'%s\'') %(message_title, value, translation)  + '\n'
        else:
            message = ('%s argument evaluates to' + ' ' + '\'%s\'') %(message_title, value)  + '\n'
        return message

    def show_warning(self, first, second):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_first = Proxy().deal_warning_message_for_one_word(first, 'First')
        message_for_second = Proxy().deal_warning_message_for_one_word(second, 'Second')
        message = language + test_name + message_for_first + ' '*3 + '\n' +  message_for_second + '\n' + 'You should verify translation is correct!'
        if message_for_first != '' or message_for_second != '':
            logger.warn(message)
        else:
            message_for_first = ShouldBeEqualProxy.deal_translate_message(self, first, 'First')
            message_for_second = ShouldBeEqualProxy.deal_translate_message(self, second, 'Second')
            message = language +' ' + message_for_first + ' '*2 +  message_for_second
            logger.info(message)


