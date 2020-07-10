from robot.libraries.BuiltIn import BuiltIn
import sys
from robot.libraries.Screenshot import Screenshot
import I18nListener as i18n
from robot.api import logger

class Proxy():
    def __init__(self):
        '''
            You should set your argument format as key, value is yourself.
            For example:
                arg_format[repr(['by=\'id\'', 'value=None'])] = self

            'arg_format' will pass into your constructor.
            "['by=\'id\'', 'value=None']" is your argument format.
        '''
        pass
    
    def i18n_Proxy(self, func):
        '''           
            Package keyword Proxy mapping logic by yourself.
        '''
        raise('You should implement it!')
    
    def show_warning(self):
        '''           
            Define keyword Proxy warning message by yourself.
        '''
        raise('You should implement it!')
    
    def deal_warning_message_for_one_word(self, word, message_title):
        # should be equal 搬來的
        # from I18nListener import I18nListener
        message = ' '*3
        counter = 1
        should_return = False
        possible_translations = i18n.I18nListener.MAP.value(word)
        if len(possible_translations) > 1: 
            should_return = True
            message_value = str(counter) + '. ' + 'Multiple translations of the word: \'%s\'' %word + '\n' + ' '*6
            message_for_list = ('\'%s\'' + ' can translate to: ' + '[ ' + ', '.join(possible_translations) +' ]') %word + '\n'
            message = message + message_value + message_for_list
            counter = counter + 1 
        # list1_to_sring =  '[' + ', '.join(argu) + ']'
        if should_return:
            message =  ('   %s Word:' + ' ' + '\'' + word+ '\'' + '\n' + ' '*3 + message) % message_title
        else:
            message = ''
        return message
    
    def deal_warning_message_for_list(self, deal_list, message_title):
        message = ' '*3
        counter = 1
        should_return = False
        for temp in deal_list:
            possible_translations = i18n.I18nListener.MAP.value(temp)
            if len(possible_translations) > 1: 
                should_return = True
                message_value = str(counter) + '. ' + 'Multiple translation of the word: \'%s\'' %''.join(temp) + '\n' + ' '*6
                message_for_list = ('\'%s\'' + ' can translate to: ' + '[ ' + ', '.join(possible_translations)+ ' ]') %temp
                message = message + message_value + message_for_list
                counter = counter + 1 
        list1_to_sring =  '[' + ', '.join(deal_list) + ']'
        if should_return:
            message = ('   In %s' + ' '*2 + list1_to_sring + '\n' + ' '*3 + message) % message_title
        else:
            message = ''
        return message