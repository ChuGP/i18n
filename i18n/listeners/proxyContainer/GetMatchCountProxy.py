from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui

class GetMatchCountProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['list', 'pattern', 'case_insensitive=False', 'whitespace_insensitive=False'])] = self

    def i18n_Proxy(self, func):
        def proxy(self, list, pattern, case_insensitive=False, whitespace_insensitive=False):
            if not list or not pattern:
                return func(self, list, pattern, case_insensitive, whitespace_insensitive)
            
            full_args = [str(list), pattern]

            list_trans = i18n.I18nListener.MAP.values(list, full_args)
            list_have_multi_trans = False
            for lt in list_trans:
                if len(lt) >1:
                    list_have_multi_trans = True
                    break
                
            if list_have_multi_trans: 
                if 'matches' in func.__name__:
                    GetMatchCountProxy.show_warning(self, list,full_args)
                i18n.I18nListener.Is_Multi_Trans = True
                
                for i, lt in enumerate(list_trans):
                    if len(lt)>1 and str(full_args)+list[i] not in ui.UI.unique_log:
                        multi_trans_word = [list[i]]                                
                        ui.UI.origin_xpaths_or_arguments.append(full_args)
                        ui.UI.add_trans_info(self, multi_trans_word, lt, full_args, func.__name__)
            
            return func(self, list, pattern, case_insensitive, whitespace_insensitive)
        return proxy

    def show_warning(self, list, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_list = Proxy().deal_warning_message_for_list(list, full_args, 'LIST')
        if message_for_list :
            message = language + test_name + message_for_list + '\n' + 'You should verify translation is correct!'
            logger.warn(message)