from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui

class RemoveFromDictionaryProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['dictionary', 'keys'])] = self

    def i18n_Proxy(self, func):
        def proxy(self, dictionary, *keys):
            full_args = [str(dictionary), str(keys)]

            dict_keys_trans = i18n.I18nListener.MAP.values(list(dictionary.keys()), full_args)
            dict_have_multi_trans  = False
            for dt in dict_keys_trans:
                if len(dt) >1:
                    dict_have_multi_trans  = True

            keys_trans = i18n.I18nListener.MAP.values(keys, full_args)
            keys_have_multi_trans = False
            for lt in keys_trans:
                if len(lt) >1:
                    keys_have_multi_trans = True
                    break
            
            if keys_have_multi_trans or dict_have_multi_trans:
                RemoveFromDictionaryProxy.show_warning(self, dictionary, keys, full_args)

                i18n.I18nListener.Is_Multi_Trans = True
                
                for i, dt in enumerate(dict_keys_trans):
                    if len(dt)>1 and str(full_args)+list(dictionary.keys())[i] not in ui.UI.unique_log:
                        multi_trans_word = [list(dictionary.keys())[i]]                                
                        ui.UI.origin_xpaths_or_arguments.append(full_args)
                        ui.UI.add_trans_info(self, multi_trans_word, dt, full_args, func.__name__)
                for i, lt in enumerate(keys_trans):
                        if len(lt) > 1 and str(full_args)+keys[i] not in ui.UI.unique_log:
                            multi_trans_word = [keys[i]]     
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            ui.UI.add_trans_info(self, multi_trans_word, lt, full_args, func.__name__)
            
            return func(self, dictionary, *keys)
        return proxy

    def show_warning(self, dictionary, keys, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_dict_keys = Proxy().deal_warning_message_for_list(dictionary.keys(), full_args, 'DICT_KEYS')
        message_for_keys = Proxy().deal_warning_message_for_list(keys, full_args, 'KEYS')
        if message_for_keys != '':
            message = language + test_name + message_for_dict_keys + '\n' + \
            message_for_keys + '\n' + 'You should verify translation is correct!'
            logger.warn(message)