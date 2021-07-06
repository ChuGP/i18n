from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui

class TitleShouldBeProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['title', 'message=None'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, title, message=None):
            full_args = [title]

            title_trans = i18n.I18nListener.MAP.value(title, full_args)

            if len(title_trans)>1:
                TitleShouldBeProxy.show_warning(self, title, full_args)

                is_pass = False
                actual = self.get_title()
                for tt in title_trans:
                    if tt == actual:
                        is_pass = True
                        break
                if is_pass:
                    i18n.I18nListener.Is_Multi_Trans = True

                    if len(title_trans) > 1 and str(full_args)+title not in ui.UI.unique_log:
                        multiple_translation_word = [title]     
                        ui.UI.origin_xpaths_or_arguments.append(full_args)
                        ui.UI.add_trans_info(self, multiple_translation_word, title_trans, full_args, func.__name__)

            actual = self.get_title()
            for tt in title_trans:
                if tt == actual:
                    title_trans = tt
            
            return func(self, title_trans, message)
        return proxy

    def show_warning(self, title, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_title = Proxy().deal_warning_message_for_one_word(title, full_args, 'TITLE')
        if message_for_title :
            message = language + test_name + message_for_title + '\n' + 'You should verify translation is correct!'
            logger.warn(message)