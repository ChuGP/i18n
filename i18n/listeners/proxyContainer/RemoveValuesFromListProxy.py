from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui

class RemoveValuesFromListProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['list_', 'values'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, list_, *values):
            full_args = [str(list_), str(values)]            

            list_trans = i18n.I18nListener.MAP.values(list_, full_args)
            list_have_multi_trans  = False
            for lt in list_trans:
                if len(lt) >1:
                    list_have_multi_trans  = True

            values_trans = i18n.I18nListener.MAP.values(values, full_args)
            values_have_multi_trans = False
            for lt in values_trans:
                if len(lt) >1:
                    values_have_multi_trans = True
                    break
            
            if list_have_multi_trans or values_have_multi_trans:
                RemoveValuesFromListProxy.show_warning(self, list_, values, full_args)

                i18n.I18nListener.Is_Multi_Trans = True
                
                for i, lt in enumerate(list_trans):
                    if len(lt)>1 and str(full_args)+list_[i] not in ui.UI.unique_log:
                        multi_trans_word = [list_[i]]                                
                        ui.UI.origin_xpaths_or_arguments.append(full_args)
                        ui.UI.add_trans_info(self, multi_trans_word, lt, full_args, func.__name__)
                for i, lt in enumerate(values_trans):
                        if len(lt) > 1 and str(full_args)+values[i] not in ui.UI.unique_log:
                            multi_trans_word = [values[i]]     
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            ui.UI.add_trans_info(self, multi_trans_word, lt, full_args, func.__name__)
                        
            for i,lt in enumerate(list_trans):
                list_[i] = lt[0] 
                           
            for i,vt in enumerate(values_trans):
                for j in range(len(vt)):
                    if vt[j] in list_:
                        values_trans[i] = vt[j]
                        break;
            
            return func(self, list_, *tuple(values_trans))
        return proxy

    def show_warning(self, list_, values, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_list = Proxy().deal_warning_message_for_list(list_, full_args, 'LIST')
        message_for_values = Proxy().deal_warning_message_for_list(values, full_args, 'VALUES')
        if message_for_list or message_for_values:
            message = language + test_name + message_for_list + '\n' + \
            message_for_values + '\n' + 'You should verify translation is correct!'
            logger.warn(message)