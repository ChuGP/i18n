from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
from SeleniumLibrary.keywords import AlertKeywords
import I18nListener as i18n
import ManyTranslations as ui

class AlertShouldBePresentProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['text=\'\'', 'action=\'ACCEPT\'', 'timeout=None'])] = self
    def i18n_Proxy(self, func):
        def proxy(self, text='', action='ACCEPT', timeout=None):
            full_args = [text] 

            text_trans = i18n.I18nListener.MAP.value(text, full_args)

            if len(text_trans)>1:
                AlertShouldBePresentProxy.show_warning(self, text, full_args)

                pass_tt = ''
                is_pass = False
                if 'present' in func.__name__ :
                    message = AlertKeywords.handle_alert(action, timeout)
                    for tt in text_trans:
                        if tt == message:
                            is_pass = True
                            pass_tt = tt
                            break
                if is_pass:
                    i18n.I18nListener.Is_Multi_Trans = True

                    if len(text_trans)>1 and str(full_args)+text not in ui.UI.unique_log:
                        multiple_translation_word = [text]     
                        ui.UI.origin_xpaths_or_arguments.append(full_args)
                        ui.UI.add_trans_info(self, multiple_translation_word, text_trans, full_args, func.__name__)
                    return func(self, pass_tt, action, timeout)

            return func(self, text_trans[0], action, timeout)
        return proxy 

    def show_warning(self, text):
        language = 'i18n in %s:\n' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_text = Proxy().deal_warning_message_for_one_word(text, 'Text')
        if message_for_text != '':
            message = language + test_name + message_for_text + ' '*3 + '\n' + 'You should verify translation is correct!'
            logger.warn(message)

