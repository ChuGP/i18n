from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui
from robot.utils import unic

class ListShouldContainValueProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['list_', 'value', 'msg=None'])] = self

    def i18n_Proxy(self, func):
        def proxy(self, list_, value, msg=None):            
            full_args = [str(list_), value]
            
            list_trans = i18n.I18nListener.MAP.values(list_, full_args)
            value_trans = i18n.I18nListener.MAP.value(value, full_args)

            list_have_multi_trans = False
            for lt in list_trans:
                if len(lt) >1:
                    list_have_multi_trans  = True
                    break 

            if list_have_multi_trans or len(value_trans)>1:
                ListShouldContainValueProxy.show_warning(self, list_, value, full_args)

                is_pass = False
                if 'not' in func.__name__ :
                    if value not in list_:
                        is_pass = True
                else:
                    if value in list_:
                        is_pass = True
                if is_pass:
                    i18n.I18nListener.Is_Multi_Trans = True

                    for i, lt in enumerate(list_trans):
                        if len(lt)>1 and str(full_args)+list_[i] not in ui.UI.unique_log:
                            multi_trans_word = [list_[i]]                            
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            ui.UI.add_trans_info(self, multi_trans_word, lt, full_args, func.__name__)
                    if len(value_trans) > 1 and str(full_args)+value not in ui.UI.unique_log:
                        multiple_translation_word = [value]     
                        ui.UI.origin_xpaths_or_arguments.append(full_args)
                        ui.UI.add_trans_info(self, multiple_translation_word, value_trans, full_args, func.__name__)
            return func(self, list_trans, value_trans, msg)
        return proxy

    def show_warning(self, list_, value, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_list = Proxy().deal_warning_message_for_list(list_, full_args, 'LIST')
        message_for_value = Proxy().deal_warning_message_for_one_word(value, full_args, 'VALUE')
        if message_for_list or message_for_value:
            message = language + test_name + message_for_list + '\n' + message_for_value + '\n' + 'You should verify translation is correct!'
            logger.warn(message)