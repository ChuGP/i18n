from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import I18nListener as i18n
import json
import re
import os
from glob import glob

class I18nMap:

    def __init__(self, translation_file,locale='en-US'):
        self.locale = locale #language
        self.translation_file = translation_file
        self.translation_mapping_routes = self.read_translation_mapping_routes()
        self.multiple_translation_words = []
        self.no_need_trans_attirbutes = ["@id", "@class"]

    def read_translation_mapping_routes(self):
        json_path = glob('./mappingRoutes.json')[0]
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def is_exist_multiple_translation_words(self, text, full_args):
        if len(self.value(text, full_args)) > 1 and text not in self.multiple_translation_words:
            self.multiple_translation_words.append(text) 
    
    '''
        new_locate_rule -> key should be the regular expression rule
                           I will use findall to find the word that is needed to translate .
                           so value should be the your match word group position.
    '''
    def locator(self, xpath, full_args, new_locate_rule={}): 
        def combine_locate_rule(rule_at, rule_bracket, locate_rule):  
            default_rule = {
                    '(('+ rule_bracket + ')\((text\(\))?\) ?= ?(\'|\")(([0-9a-zA-Z.?&()]| ?)+)(\'|\"))': 4, 
                    '(('+ rule_bracket + ')\((text\(\))?\)\ ?, ?(\'|\")(([0-9a-zA-Z.?&()]| ?)+)(\'|\"))': 4,
                    '(('+ rule_at + ') ?= ?(\'|\")(([0-9a-zA-Z.?&()]| ?)+)(\'|\"))' : 3,
                    '(('+ rule_at + ') ?, ?(\'|\")(([0-9a-zA-Z.?&()]| ?)+)(\'|\"))' : 3
                }
            if len(new_locate_rule):
                temp = dict(default_rule.items() + new_locate_rule.items())
                locate_rule = temp
            else:
                locate_rule = default_rule
            return locate_rule

        def find_all_match_word(xpath, locate_rule):  
            all_match_words = {}
            for rule in locate_rule.keys():
                matches = re.findall(rule, xpath)
                all_match_words[rule] = matches
            return all_match_words
        
        self.multiple_translation_words = []    
        if not isinstance(xpath, str):
            return [xpath]
        translated_xpath = [xpath]

        rule_for_filter = {
            "(@[a-z-]*)":"@",
            "([a-z-]*\(\))":"()"
        }
        rule_for_insert_at = ""
        rule_for_insert_bracket = ""
        all_match_attributes = find_all_match_word(xpath, rule_for_filter)
        for rule, matches in all_match_attributes.items():
            for match in matches:
                c = 0
                if match not in self.no_need_trans_attirbutes:
                    if rule_for_filter[rule] == "@":
                        rule_for_insert_at += "|" + match if c!=0 else match
                        c+=1
                    elif rule_for_filter[rule] == "()":
                        match = match.strip("()")
                        rule_for_insert_bracket += "|" + match if c!=0 else match
                        c+=1

        locate_rule = combine_locate_rule(rule_for_insert_at, rule_for_insert_bracket, new_locate_rule) 
        
        all_match_words = find_all_match_word(xpath, locate_rule)
        for rule, matches in all_match_words.items():
            for match in matches:
                match_group = locate_rule[rule]
                quot_group = match_group - 1 
                self.is_exist_multiple_translation_words(match[match_group], full_args)
                translated_xpath = self.translate(full_args, match=match[match_group], quot=match[quot_group], 
                xpaths=translated_xpath) # group 0 as self, group 4 as match, group 3 as quot 
        if xpath != list(translated_xpath)[0] :
            self.log_translation_info(xpath, translated_xpath)
        return translated_xpath
    
    def log_translation_info(self, xpath, translated_xpath):
        def is_need_to_show_warning():
            for multiple_translation_word in self.multiple_translation_words:
                if multiple_translation_word in i18n.I18nListener.Not_SHOW_WARNING_WORDS:
                    return False
            return True   
        
        def deal_translated_xpath_info(translated_xpath):
            translated_xpath_info = ''
            for i,temp_xpath in enumerate(translated_xpath):
                temp = str(i+1) + '. ' + temp_xpath + '\n   '
                translated_xpath_info = translated_xpath_info + temp
            message = 'Detail Information\ni18n in %s :\nOriginal Locator:\n   1. %s\nTranslated Locator:\n   %s' % (self.locale, xpath, translated_xpath_info)
            return message
        
        warning_or_not = is_need_to_show_warning()
        message = deal_translated_xpath_info(translated_xpath)
        if warning_or_not == False:
            words = ', '.join(self.multiple_translation_words)
            message = message + '\nYou had resolved the multiple translations of the word: \'%s\'' %(words)
        logger.info(message)

    def get_multiple_translation_words(self):
        return self.multiple_translation_words

    # Our target is "XXX" if without quot that it will translate the wrong target.
    def translate(self,full_args, match, quot, xpaths):
        origin = quot + match + quot
        translate_list = []
        for translation in self.value(match, full_args):
            value = quot + translation + quot
            for xpath in xpaths:
                translate_list.append(xpath.replace(origin, value))
        return list(set(translate_list))

    #For list should be equal, set should be equal...
    def values(self, values, full_args):
        return [self.value(v, full_args) for v in values]

    def value(self, value, full_args):
        try:
            result = self.get_possible_translation(value, full_args)
        except (KeyError):
            return [value]
        return list(set(result))

    def get_possible_translation(self, value, full_args):
        result = []
        for i in range(len(i18n.I18nListener.SETTING_KEYS)):
            if i18n.I18nListener.SETTING_KEYS[i] == value and i18n.I18nListener.SETTING_ARGS[i] == full_args:
                result.append(i18n.I18nListener.SETTING_TRANS[i])
                break
        if result:    
            return result
        else:
            try:
                for mapping_route in self.translation_mapping_routes[value]:
                    result.append(eval("self.translation_file%s" % mapping_route))
            except (KeyError):
                raise KeyError
            return result