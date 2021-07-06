from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from selenium import webdriver
import SeleniumLibrary
import inspect
import json

def parse_library(library):
    function_names = {}
    for str_method in dir(library):
        func = getattr(library, str_method)
        if repr(type(func)) == "<class 'function'>":
            function_names[func.__name__] = get_argument_declaration(func)
    generate_json_file('%s.json' % library.__name__, {library.__name__:function_names})

def parse_seleniumLibrary():
    function_names = {}
    for keyword in SeleniumLibrary.SeleniumLibrary().keywords: # Use ".keywords" Can get all keywords
        function_names[keyword] = get_argument_declaration(keyword)
    generate_json_file("SeleniumLibrary.json", {"SeleniumLibrary: ":function_names})

def parse_seleniumLibrary():
    function_names = {}
    keywords = [keyword.replace(' ', '_').lower() for keyword in SeleniumLibrary.SeleniumLibrary().keywords]
    for str_keywords_class in dir(SeleniumLibrary):
        keywords_class = getattr(SeleniumLibrary, str_keywords_class)
        for str_method in dir(keywords_class):
            if str_method.replace(' ', '_').lower() in keywords:
                func = getattr(keywords_class, str_method)
                if repr(type(func)) == "<class 'function'>":
                    function_names[func.__name__] = get_argument_declaration(func)
    generate_json_file("SeleniumLibrary.json", {"SeleniumLibrary: ":function_names})

def generate_json_file(output_file_name, source):
    with open("./result/"+output_file_name, 'w') as file:
        json.dump(source, file, indent=4) #python->json

def get_argument_declaration(func):
    args = inspect.getargspec(func).args[1:]  # [0] is self
    defaults = inspect.getargspec(func).defaults
    varargs = inspect.getargspec(func).varargs
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

if __name__ == "__main__":
    parse_seleniumLibrary() 
    parse_library(Collections)
    parse_library(BuiltIn)
    parse_library(webdriver.Chrome)