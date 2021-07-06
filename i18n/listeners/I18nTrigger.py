import SeleniumLibrary
import re
import os
import inspect
import json
import sys
from glob import glob
import SeleniumLibrary
from selenium import webdriver
from robot.libraries.Collections import Collections
from SeleniumLibrary.base import keyword
from robot.libraries.BuiltIn import BuiltIn

class I18nTrigger:

    def __init__(self):
        self.arg_format = {}
        self.new_proxy_instance()
        self.set_proxy_func_to_library_class_func(Collections)
        self.set_proxy_func_to_library_class_func(webdriver.Chrome)
        self.set_proxy_func_to_library_class_func(BuiltIn)
        self.set_proxy_func_to_SeleniumLibrary()

    def get_module_name(self, path):
        file = re.findall('[_A-Za-z]+.py', path)
        file_name = re.findall('[_A-Za-z]+', file[0])
        module_name = file_name[0]
        return module_name

    def get_class_name(self, text):
        m = re.search('class[ A-Za-z]+', text)
        class_define =  m.group(0)
        m = re.findall('[a-zA-Z]+', class_define)
        class_name = m[1] # Fisrst is 'Class' Second is Class name
        return class_name

    def new_proxy_instance(self):
        module_names = []
        class_names = []
        for f in glob('%s\proxyContainer\*.py' % (os.path.dirname(os.path.abspath(__file__)))):
            with open(f, 'r', encoding='UTF-8') as sub_proxy:
                text = sub_proxy.read()
                module_name =  self.get_module_name(sub_proxy.name)
                if text and module_name != '__init__'and module_name != 'Proxy':
                    module_names.append(module_name)
                    class_names.append(self.get_class_name(text))

        zipped = zip ( module_names , class_names )
        for arg in zipped:
            inport_text = 'from proxyContainer import %s' %(arg[0])
            exec(inport_text)
            instance_text = '%s.%s(self.arg_format)' %(arg[0], arg[1])
            eval(instance_text)

    #get proxy
    def get_func_proxy(self, func):
        args_declaration = self.get_argument_declaration(func)
        if repr(args_declaration) in list(self.arg_format.keys()):
            return self.arg_format[repr(args_declaration)].i18n_Proxy(func)
        return func

    def get_argument_declaration(self, func):
        args = inspect.getfullargspec(func).args[1:]
        defaults = inspect.getfullargspec(func).defaults
        varargs = inspect.getfullargspec(func).varargs
        keywords = inspect.getargspec(func).keywords
        if defaults:
            defaults = ['=' + repr(default) for default in defaults]
            defaults = [''] * (len(args) - len(defaults)) + defaults
            args = list(arg[0] + arg[1] for arg in zip(args, defaults))
        if varargs:
            args.append(varargs)
        if keywords:
            args.append(keywords)
        return args

    def set_proxy_func_to_library_class_func(self, library):
        for str_method in dir(library):
            func = getattr(library, str_method)
            if repr(type(func)) == "<class 'function'>":
                setattr(library, str_method, self.get_func_proxy(func))

    # provide a surrogate of selenium keywords and functions so that they can test i18n
    ## SeleniumLibrary
    def set_proxy_func_to_SeleniumLibrary(self):
        import SeleniumLibrary
        keywords = [keyword.replace(' ', '_').lower() for keyword in SeleniumLibrary.SeleniumLibrary().keywords]
        for str_keywords_class in dir(SeleniumLibrary):
            keywords_class = getattr(locals().get(SeleniumLibrary.__name__), str_keywords_class)
            for str_method in dir(keywords_class):
                if str_method.replace(' ', '_').lower() in keywords:
                    func = getattr(keywords_class, str_method)
                    if repr(type(func)) == "<class 'function'>":
                        setattr(keywords_class, str_method, keyword(self.get_func_proxy(func)))

I18nTrigger() #import I18nTrigger that it will run this line.