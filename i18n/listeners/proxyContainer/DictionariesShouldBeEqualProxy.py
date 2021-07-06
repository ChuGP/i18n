from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui
from robot.libraries.Collections import _Dictionary

class DictionariesShouldBeEqualProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['dict1', 'dict2', 'msg=None', 'values=True'])] = self
        
    def i18n_Proxy(self, func):
        def proxy(self, dict1, dict2, msg=None, values=True):
            full_args = [str(dict1), str(dict2)]

            dict1_keys_trans = i18n.I18nListener.MAP.values(list(dict1.keys()), full_args)
            dict1_values_trans = i18n.I18nListener.MAP.values(list(dict1.values()), full_args)
            dict2_keys_trans = i18n.I18nListener.MAP.values(list(dict2.keys()), full_args)
            dict2_values_trans = i18n.I18nListener.MAP.values(list(dict2.values()), full_args)
            whole_trans = []
            whole_trans.append(dict1_keys_trans)
            whole_trans.append(dict1_values_trans)
            whole_trans.append(dict2_keys_trans)
            whole_trans.append(dict2_values_trans)
            dict_have_multi_trans = False
            for i in range(4):
                for dt in whole_trans[i]: 
                    if len(dt)>1:
                        dict_have_multi_trans = True 
                        break

            new_dict1 = {}
            new_dict2 = {}
            new_dict2=dict(zip(list(dict2.keys()), dict2_values_trans))

            if dict_have_multi_trans:
                DictionariesShouldBeEqualProxy.show_warning(self, dict1, dict2, full_args)
                if 'contain_sub' in func.__name__:
                    keys = self.get_dictionary_keys(dict2)
                    contain_key = True  
                    for k in keys:
                        if k not in dict1:
                            contain_key = False
                            break
                    if contain_key and not list(_Dictionary._yield_dict_diffs(self, keys, dict1, dict2)):
                        diffs = False
                    else:
                        diffs = True
                elif 'equal' in func.__name__:
                    try:
                        keys = _Dictionary._keys_should_be_equal(self, dict1, dict2, msg, values)
                        diffs = list(_Dictionary._yield_dict_diffs(self, keys, dict1, dict2))
                        for k in keys:
                            if dict1[k] in dict2_values_trans[0]:
                                diffs = False
                    except:
                        for dict1_key in dict1.keys():
                            for dict2_key in new_dict2.keys():
                                if [dict1_key] in dict2_keys_trans and dict1[dict1_key] in new_dict2[dict2_key][0]:
                                    new_dict1[dict2_key] = new_dict2[dict2_key]
                                    diffs = False 
                                else:
                                    diffs = True
                                    break
                if not diffs:
                    i18n.I18nListener.Is_Multi_Trans = True

                    for i, dt in enumerate(dict1_keys_trans):
                        if len(dt)>1 and str(full_args)+list(dict1.keys())[i] not in ui.UI.unique_log:
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            multi_trans_word = [list(dict1.keys())[i]]                                
                            ui.UI.add_trans_info(self, multi_trans_word, dt, full_args, func.__name__)
                    for i, dt in enumerate(dict1_values_trans):
                        if len(dt)>1 and str(full_args)+list(dict1.values())[i] not in ui.UI.unique_log:
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            multi_trans_word = [list(dict1.values())[i]]                                
                            ui.UI.add_trans_info(self, multi_trans_word, dt, full_args, func.__name__)                    
                    for i, dt in enumerate(dict2_keys_trans):
                        if len(dt)>1 and str(full_args)+list(dict2.keys())[i] not in ui.UI.unique_log:
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            multi_trans_word = [list(dict2.keys())[i]]                                
                            ui.UI.add_trans_info(self, multi_trans_word, dt, full_args, func.__name__)                    
                    for i, dt in enumerate(dict2_values_trans):
                        if len(dt)>1 and str(full_args)+list(dict2.values())[i] not in ui.UI.unique_log:
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            multi_trans_word = [list(dict2.values())[i]]                                
                            ui.UI.add_trans_info(self, multi_trans_word, dt, full_args, func.__name__)  
            dict1 = dict(zip(list(dict1.keys()), dict1_values_trans)) 
            dict2 = dict(zip(list(dict2.keys()), dict2_values_trans))
            
            for dict1_key in dict1.keys():
                for dict2_key in dict2.keys():
                    if [dict1_key] in dict2_keys_trans and dict1[dict1_key]== dict2[dict2_key]:
                        dict1.pop(dict1_key, None)
                        dict1[dict2_key] = dict2[dict2_key]
                        return func(self, dict1, dict2)
                    elif dict1_key== dict2_key and dict1[dict1_key][0] in dict2[dict2_key]:
                        dict1[dict1_key] = dict2[dict2_key] 
            if new_dict1:
                return func(self, new_dict1, new_dict2, msg, values)     
                
            else:           
                return func(self, dict1, dict2, msg, values)                              
        return proxy

    def show_warning(self, dict1, dict2, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_dict1_key = Proxy().deal_warning_message_for_list(dict1.keys(), full_args, 'Dict1KEY')
        message_for_dict1_value = Proxy().deal_warning_message_for_list(dict1.values(), full_args, 'Dict1VALUE')
        message_for_dict2_key = Proxy().deal_warning_message_for_list(dict2.keys(), full_args, 'Dict2KEY')
        message_for_dict2_value = Proxy().deal_warning_message_for_list(dict2.values(), full_args, 'Dict2VALUE')
        message = language + test_name + message_for_dict1_key + '\n' + message_for_dict1_value + '\n' \
        + message_for_dict2_key + '\n' + message_for_dict2_value + '\n' + 'You should verify translation is correct!'
        if message_for_dict1_key or message_for_dict1_value or message_for_dict2_key or message_for_dict2_value:
            logger.warn(message)