from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui

class DictionaryShouldContainValueProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['dictionary', 'value', 'msg=None'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, dictionary, value, msg=None):
            full_args = [str(dictionary), value]

            dict_values_trans = i18n.I18nListener.MAP.values(list(dictionary.values()), full_args)
            dict_have_multi_trans  = False
            for dt in dict_values_trans:
                if len(dt) >1:
                    dict_have_multi_trans  = True
            value_trans = i18n.I18nListener.MAP.value(value, full_args)

            if len(value_trans)>1 or dict_have_multi_trans:
                DictionaryShouldContainValueProxy.show_warning(self, dictionary, value, full_args)
                is_pass = False
                if 'not' in func.__name__:
                    if value not in dictionary.values():
                        is_pass = True
                else:
                    if value in dictionary.values():
                        is_pass = True
                if is_pass:
                    i18n.I18nListener.Is_Multi_Trans = True
                    
                    for i, dt in enumerate(dict_values_trans):
                        if len(dt)>1 and str(full_args)+list(dictionary.values())[i] not in ui.UI.unique_log:
                            multi_trans_word = [list(dictionary.values())[i]]                                
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            ui.UI.add_trans_info(self, multi_trans_word, dt, full_args, func.__name__)
                    if len(value_trans) > 1 and str(full_args)+value not in ui.UI.unique_log:
                        multiple_translation_word = [value]     
                        ui.UI.origin_xpaths_or_arguments.append(full_args)
                        ui.UI.add_trans_info(self, multiple_translation_word, value_trans, full_args, func.__name__)
                        
            dictionary = dict(zip(list(dictionary.keys()), dict_values_trans))
            return func(self, dictionary, value_trans, msg)
        return proxy

    def show_warning(self, dictionary, value, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_dict_value = Proxy().deal_warning_message_for_list(dictionary.values(),full_args, 'DICT_VALUE')
        message_for_value = Proxy().deal_warning_message_for_one_word(value, full_args,  'VALUE')
        if message_for_dict_value or message_for_value:
            message = language + test_name + message_for_dict_value + '\n' + message_for_value + '\n'\
                        'You should verify translation is correct!'
            logger.warn(message)