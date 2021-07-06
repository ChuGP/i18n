from .Proxy import Proxy
from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
from robot.api import logger
import I18nListener as i18n
import ManyTranslations as ui
from SeleniumLibrary.keywords.selectelement import SelectElementKeywords

class SelectFromListByLabelProxy(Proxy):
    def __init__(self, arg_format):
        arg_format[repr(['locator', 'labels'])] = self
    
    def i18n_Proxy(self, func):
        def proxy(self, locator, *labels):
            if not labels:
                return func(self, locator, labels)
            full_args = [locator, str(labels)]

            BuiltIn().import_library('SeleniumLibrary')
            locator_trans = i18n.I18nListener.MAP.locator(BuiltIn().replace_variables(locator), full_args)
            multiple_translation_words = i18n.I18nListener.MAP.get_multiple_translation_words()
            words_trans = i18n.I18nListener.MAP.values(multiple_translation_words, full_args)

            labels_trans = i18n.I18nListener.MAP.values(labels, full_args)
            labels_have_multi_trans = False
            for lt in labels_trans:
                if len(lt) >1:
                    labels_have_multi_trans = True
                    break

            xpath = ""
            if len(locator_trans)>1 or labels_have_multi_trans:
                SelectFromListByLabelProxy.show_warning(self, multiple_translation_words, labels, full_args) #show warning
                
                for i, lt in enumerate(locator_trans):
                    xpath += '|' + lt.replace('xpath', '') if i!=0 else lt.replace('xpath', '')

                all_options = SelectElementKeywords._get_options(self, locator)
                all_labels = SelectElementKeywords._get_labels(self, all_options)
                is_pass = False
                for lt in labels_trans:
                    for single_tran in lt:
                        if single_tran in all_labels:
                            is_pass = True
                            break

                if is_pass:
                    i18n.I18nListener.Is_Multi_Trans = True
                    
                    for i, word_trans in enumerate(words_trans):
                        if len(word_trans)>1 and str(full_args)+multiple_translation_words[i] not in ui.UI.unique_log:
                            multi_trans_word = [multiple_translation_words[i]] 
                            ui.UI.origin_xpaths_or_arguments.append(full_args)                               
                            ui.UI.add_trans_info(self, multi_trans_word, word_trans, full_args, func.__name__)
                    for i, lt in enumerate(labels_trans):
                        if len(lt) > 1 and str(full_args)+labels[i] not in ui.UI.unique_log:
                            multi_trans_word = [labels[i]]     
                            ui.UI.origin_xpaths_or_arguments.append(full_args)
                            ui.UI.add_trans_info(self, multi_trans_word, lt, full_args, func.__name__)
            else:
                xpath = locator_trans[0]
            
            all_options = SelectElementKeywords._get_options(self, locator)
            all_labels = SelectElementKeywords._get_labels(self, all_options)
            for i, lt in enumerate(labels_trans): 
                    for single_tran in lt:
                        if single_tran in all_labels:
                            labels_trans[i] = single_tran
                            break

            return func(self, BuiltIn().replace_variables(xpath), *tuple(labels_trans))
        return proxy

    def show_warning(self, multi_trans_words, labels, full_args):
        language = 'i18n in %s:\n ' %i18n.I18nListener.LOCALE
        test_name = ('Test Name: %s') %BuiltIn().get_variable_value("${TEST NAME}") + '=> Exist multiple translations of the word' + '\n'
        message_for_words = Proxy().deal_warning_message_for_list(multi_trans_words,full_args, 'MULTI_TRANS_WORDS')
        message_for_labels = Proxy().deal_warning_message_for_list(labels, full_args, 'LABELS')
        if message_for_words or message_for_labels:
            message = language + test_name + message_for_words + '\n' + \
                message_for_labels + '\n' +'You should verify translation is correct!'
            logger.warn(message)