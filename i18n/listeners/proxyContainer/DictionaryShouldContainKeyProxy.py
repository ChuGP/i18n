from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui

class DictionaryShouldContainKeyProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['dictionary', 'key', 'msg=None'])] = self

    def i18n_Proxy(self, func):
        def proxy(self, dictionary, key, msg=None):
            full_args = [str(dictionary), key]

            dict_keys_trans = i18n.I18nListener.MAP.values(list(dictionary.keys()), full_args)
            dict_have_multi_trans  = False
            for dt in dict_keys_trans:
                if len(dt) >1:
                    dict_have_multi_trans  = True
                    break
            key_trans = i18n.I18nListener.MAP.value(key, full_args)

            if len(key_trans)>1 or dict_have_multi_trans:
                DictionaryShouldContainKeyProxy.show_warning(self, dictionary, key, full_args)

                is_pass = False
                if 'not' in func.__name__:
                    if key not in dictionary.keys():
                        is_pass = True
                else:
                    if key in dictionary.keys():
                        is_pass = True
                if is_pass:
                    
                    i18n.I18nListener.Is_Multi_Trans = True
                    
                    for i, dt in enumerate(dict_keys_trans):
                        if len(dt)>1 and str(full_args)+list(dictionary.keys())[i] not in ui.UI.unique_log: 
                            multi_trans_word = [list(dictionary.keys())[i]]                                
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            ui.UI.add_trans_info(self, multi_trans_word, dt, full_args, func.__name__)
                    if len(key_trans) > 1 and str(full_args)+key not in ui.UI.unique_log:
                        multiple_translation_word = [key]     
                        ui.UI.origin_xpaths_or_arguments.append(full_args)
                        ui.UI.add_trans_info(self, multiple_translation_word, key_trans, full_args, func.__name__)
            return func(self, dictionary, key, msg)
        return proxy

    def show_warning(self, dictionary,key, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_dict_key = Proxy().deal_warning_message_for_list(dictionary.keys(),full_args, 'DICT_KEY')
        message_for_key = Proxy().deal_warning_message_for_one_word(key, full_args,  'KEY')
        if message_for_dict_key or message_for_key:
            message = language + test_name + message_for_dict_key + '\n' + message_for_key + '\n'\
                        'You should verify translation is correct!'
            logger.warn(message)