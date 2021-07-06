from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui
from robot.utils import is_string, is_list_like

class ShouldContainProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['container', 'item', 'msg=None', 'values=True', 'ignore_case=False'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, container, item, msg=None, values=True, ignore_case=False):
            full_args = [str(container), item]

            container_trans = i18n.I18nListener.MAP.values(container, full_args)
            item_trans = i18n.I18nListener.MAP.value(item, full_args)

            container_have_multi_trans = False
            if is_list_like(container):
                for lt in container_trans:
                    if len(lt) >1:
                        container_have_multi_trans  = True
                        break 
            elif is_string(container):
                if len(container_trans)>1:
                    container_have_multi_trans = True

            if container_have_multi_trans or len(item_trans)>1:
                ShouldContainProxy.show_warning(self, container, item, full_args)
                
                is_pass = False
                if 'not' in func.__name__ :
                    if is_string(container):
                        container = container.lower()
                        if item not in container and (index not in container for index in item_trans):
                            is_pass=True
                    elif is_list_like(container):
                        if item not in container and (index not in container for index in item_trans):
                            is_pass = True
                else:
                    if is_string(container):
                        container = container.lower()
                        if item in container or (index in container for index in item_trans):
                            is_pass = True
                    elif is_list_like(container):
                        if item in container or (index in container for index in item_trans):
                            is_pass = True

                if is_pass:
                    i18n.I18nListener.Is_Multi_Trans = True

                    if is_list_like(container):
                        for i, lt in enumerate(container_trans):
                            if len(lt)>1 and str(full_args)+container[i] not in ui.UI.unique_log:
                                multi_trans_word = [container[i]]                            
                                ui.UI.origin_xpaths_or_arguments.append(full_args)
                                ui.UI.add_trans_info(self, multi_trans_word, lt, full_args, func.__name__)
                    elif is_string(container):
                        if len(container_trans)>1 and str(full_args)+container not in ui.UI.unique_log:
                            multiple_translation_word = [container]     
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            ui.UI.add_trans_info(self, multiple_translation_word, container_trans, full_args, func.__name__)
                    if len(item_trans)>1 and str(full_args)+item not in ui.UI.unique_log:
                        multiple_translation_word = [item]     
                        ui.UI.origin_xpaths_or_arguments.append(full_args)
                        ui.UI.add_trans_info(self, multiple_translation_word, item_trans, full_args, func.__name__)

            if 'not' not in func.__name__ :
                if is_list_like(item_trans):
                    for it in item_trans:
                        if [it] in container_trans:
                            item_trans = [it]
                            break
                        
            return func(self, container_trans, item_trans, msg)
        return proxy                        
    
    def show_warning(self, container, item, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_container = Proxy().deal_warning_message_for_list(container, full_args, 'CONTAINER')
        message_for_item = Proxy().deal_warning_message_for_one_word(item, full_args, 'Expected Contain')
        if message_for_container or message_for_item :
            message = language + test_name + message_for_container + '\n' +  message_for_item + '\n' + 'You should verify translation is correct!'
            logger.warn(message)