from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import itertools
import I18nListener as i18n

class ListsShouldBeEqualProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['list1', 'list2', 'msg=None', 'values=True', 'names=None'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, list1, list2, msg=None, values=True, names=None):
            if not list1 or not list2:
                return func(self, list1, list2, msg, values, names)
            ListsShouldBeEqualProxy.show_warning(self, list1, list2)
            list1_translation = i18n.I18nListener.MAP.values(list1)
            list2_translation = i18n.I18nListener.MAP.values(list2)
            list1_all_combination = list(itertools.product(*list1_translation))
            list2_all_combination = list(itertools.product(*list2_translation))
            for list1_sub in list1_all_combination:
                for list2_sub in list2_all_combination:
                    if isinstance(list1_sub[0], dict) and isinstance(list2_sub[0], dict):
                        if(list1_sub == list2_sub):
                            return func(self, list1_sub, list2_sub, msg, values, names)
                    elif(set(list1_sub) == set(list2_sub) and len(list1_sub) == len(list2_sub)):
                        return func(self, list(list1_sub), list(list2_sub), msg, values, names)
            return func(self, list1, list2, msg, values, names)
        return proxy
    
    def show_warning(self, list1, list2):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_list1 = Proxy().deal_warning_message_for_list(list1, 'LIST1')
        message_for_list2 = Proxy().deal_warning_message_for_list(list2, 'LIST2')
        message = language + test_name + message_for_list1 + ' '*3 + '\n' +  message_for_list2 + '\n'  + 'You should verify translation is correct!'
        if message_for_list1 != '' or message_for_list1 != '':
            logger.warn(message)