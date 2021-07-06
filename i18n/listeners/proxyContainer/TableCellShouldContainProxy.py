from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui
from SeleniumLibrary.keywords.tableelement import TableElementKeywords

class TableCellShouldContainProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', 'row', 'column', 'expected', 'loglevel=\'TRACE\''])] = self

    def i18n_Proxy(self, func):
        def proxy(self, locator, row, column, expected, loglevel='TRACE'):
            full_args = [locator, row, column, expected]

            expected_trans = i18n.I18nListener.MAP.value(expected, full_args)
            locator_trans = i18n.I18nListener.MAP.locator(BuiltIn().replace_variables(locator), full_args)
            multiple_translation_words = i18n.I18nListener.MAP.get_multiple_translation_words()
            word_trans = i18n.I18nListener.MAP.values(multiple_translation_words, full_args)

            xpath = ''
            my_expected = ''
            if len(expected_trans)>1 or len(locator_trans)>1:
                TableCellShouldContainProxy.show_warning(self, multiple_translation_words, expected, full_args)

                for i, lt in enumerate(locator_trans):
                    is_pass = False
                    is_actual = BuiltIn().run_keyword_and_return_status('Get WebElement', lt)
                    if is_actual:
                        xpath += lt.replace('xpath:','')
                        content = TableElementKeywords.get_table_cell(self, lt, row, column, loglevel)
                        for et in expected_trans:
                            if et in content:
                                my_expected += et
                                is_pass = True
                                break

                    if is_pass:
                        i18n.I18nListener.Is_Multi_Trans = True
                        
                        for i, wt in enumerate(word_trans):
                            if len(wt)>1 and str(full_args)+multiple_translation_words[i] not in ui.UI.unique_log:
                                multi_trans_word = [multiple_translation_words[i]]                            
                                ui.UI.origin_xpaths_or_arguments.append(full_args)
                                ui.UI.add_trans_info(self, multi_trans_word, wt, full_args, func.__name__)
                        if len(expected_trans) > 1 and str(full_args)+expected not in ui.UI.unique_log:
                            multiple_translation_word = [expected]     
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            ui.UI.add_trans_info(self, multiple_translation_word, expected_trans, full_args, func.__name__)
                        break
            else:
                xpath = locator_trans[0].replace('xpath:','')
                my_expected = expected_trans[0]

            return func(self, xpath, row, column, my_expected, loglevel)
        return proxy

    def show_warning(self, multiple_translation_words, expected, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_multi_trans_words = Proxy().deal_warning_message_for_list(multiple_translation_words, full_args, 'MULTI_TRANS_WORDS')
        message_for_expected = Proxy().deal_warning_message_for_one_word(expected, full_args, 'EXPECTED')
        if message_for_multi_trans_words or message_for_expected:
            message = language + test_name + message_for_multi_trans_words + '\n' +\
                      message_for_expected + '\n' + 'You should verify translation is correct!'
            logger.warn(message)