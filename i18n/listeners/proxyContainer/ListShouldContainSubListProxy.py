from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui
from robot.utils import unic

class ListShouldContainSubListProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['list1', 'list2', 'msg=None', 'values=True'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, list1, list2, msg=None, values=True):
            full_args = [str(list1), str(list2)]

            list1_trans = i18n.I18nListener.MAP.values(list1, full_args)
            list2_trans = i18n.I18nListener.MAP.values(list2, full_args)

            list1_have_multi_trans  = False
            for lt in list1_trans:
                if len(lt) >1:
                    list1_have_multi_trans  = True
                    break
            list2_have_multi_trans  = False
            for lt in list2_trans:
                if len(lt) >1:
                    list2_have_multi_trans  = True
                    break

            if list1_have_multi_trans or list2_have_multi_trans:
                ListShouldContainSubListProxy.show_warning(self, list1, list2, full_args)

                diffs = ', '.join(unic(item) for item in list2 if item not in list1)
                if not diffs:
                    i18n.I18nListener.Is_Multi_Trans = True
                    
                    for i, lt in enumerate(list1_trans):
                        if len(lt)>1 and str(full_args)+list1[i] not in ui.UI.unique_log:
                            multi_trans_word = [list1[i]]                            
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            ui.UI.add_trans_info(self, multi_trans_word, lt, full_args, func.__name__)
                    for i, lt in enumerate(list2_trans):
                        if len(lt)>1 and str(full_args)+list2[i] not in ui.UI.unique_log:
                            multi_trans_word = [list2[i]]                            
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            ui.UI.add_trans_info(self, multi_trans_word, lt, full_args, func.__name__)
            return func(self, list1_trans, list2_trans, msg, values)
        return proxy

    def show_warning(self, list1, list2, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_list1 = Proxy().deal_warning_message_for_list(list1, full_args, 'LIST1')
        message_for_list2 = Proxy().deal_warning_message_for_list(list2, full_args,  'LIST2')
        if message_for_list1 or message_for_list2:
            message = language + test_name + message_for_list1 + '\n' + message_for_list2 + '\n'\
                        'You should verify translation is correct!'
            logger.warn(message)