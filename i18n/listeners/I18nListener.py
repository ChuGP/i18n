import SeleniumLibrary
import inspect
import os
import json
import sys
import itertools
import time
import re
from glob import glob
from selenium import webdriver
from I18nMap import I18nMap
from MappingRoutesGenerator import MappingRoutesGenerator
from SeleniumLibrary.base import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.api import logger
from robot.libraries.Screenshot import Screenshot
from selenium.webdriver.remote.webelement import WebElement
from I18nTrigger import I18nTrigger #This line will initiate Ii18nTrigger

class I18nListener:
 
    ROBOT_LISTENER_API_VERSION = 2
    MAP = None
    TRANSLATION_FILE = json.loads("{}")
    LOCALE = None
    Not_SHOW_WARNING_WORDS = []
    Is_Multi_Trans=False
    SETTING_KEYS = {}
    SETTING_TRANS = {}
    SETTING_ARGS = {}

    def __init__(self, locale='en-US', language_file_path='.',not_show_warning_words='None'):
        self.is_admin_language_set=False
        self.is_ui_open=False
        self.locale = locale
        self.attrs = {}
        self.locale_dict = {'en-US':'United Kingdom - English', 
                            'ja':'日本 - 日本語', 
                            'ko':'대한민국 - 한국어', 
                            'zh-CN':'中国 - 简体中文', 
                            'zh-TW':'台灣 - 繁體中文',  
                            'de-CH':'Schweiz - Deutsch'}

        #decide language file's path. It's '.' by default. 
        if language_file_path == 'i18njson':
            language_file_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

        MappingRoutesGenerator().generate(language_file_path)
        for f in glob('%s/languageFiles/%s/*%s.json' % (language_file_path, locale, locale)):
            with open(f, 'r', encoding='UTF-8') as i18n_file: 
                i18n_dict = json.load(i18n_file)
            self.combine_i18n_dict(source_dict=i18n_dict, target_dict=I18nListener.TRANSLATION_FILE)
        I18nListener.MAP = I18nMap(I18nListener.TRANSLATION_FILE, locale)
        I18nListener.LOCALE = locale # for get language Ex zh-TW, zh-CN
        I18nListener.Not_SHOW_WARNING_WORDS = self.parse_not_show_warning_words(not_show_warning_words)

    '''
        append all key, value of source_dict to target_dict
        source_dict is the dict of json file like 'common-zh-TW.json'...
    '''
    def combine_i18n_dict(self, source_dict, target_dict):
        for key, value in source_dict.items():
            target_dict[key] = value
    
    def start_suite(self, name, attrs):
        if not self.is_admin_language_set: #set the admin language in the first suite start
            self.is_admin_language_set=True
            BuiltIn().set_global_variable('${language}',self.locale_dict[self.locale])
        with open("./setting.txt", 'a+') as file:
            if os.stat("./setting.txt").st_size != 0:
                file.seek(0)
                for i, line in enumerate(file.readlines()):
                    split_key_value = []
                    split_key_value=line.strip("\n").split('~')
                    read_args = split_key_value[1].split('#')
                    I18nListener.SETTING_KEYS[i] = split_key_value[2]
                    I18nListener.SETTING_TRANS[i] = split_key_value[3]
                    I18nListener.SETTING_ARGS[i] = read_args

    def parse_not_show_warning_words(self, words_string):
        if words_string == "Not_show_warning.txt":
            Not_show_warning_txt = glob('%s/Not_show_warning.txt' % (os.path.dirname(os.path.abspath(__file__))))[0]
            with open(Not_show_warning_txt, 'r', encoding='utf-8') as f:
                words_string = f.read()
        words = words_string.split('+')
        return words

    def end_suite(self, name, attrs):
        if not self.is_ui_open and I18nListener.Is_Multi_Trans:
            self.is_ui_open=True
            import ManyTranslations
            ManyTranslations.UI()