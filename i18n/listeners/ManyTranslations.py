from tkinter import *
import random
import time
import threading
from PIL import Image, ImageTk
from robot.api import logger
import tkinter.font as tkFont
import os


class UI:
    keyword_name = []
    translations_key = []
    translations_value = []
    origin_xpaths_or_arguments = []
    unique_log= []

    def __init__(self):
        self.run()

    def add_trans_info(self, multi_trans_word, translations, full_args, func_name):
        if not type(translations[0]) == list:
            translations = [translations]
        
        UI.translations_key.append(multi_trans_word[0])
        UI.translations_value.append(translations[0])
        UI.unique_log.append(str(full_args) + multi_trans_word[0])
        UI.add_keyword_name(self,func_name)

    def add_keyword_name(self, func_name):
        robot_func_name = ""
        for n, i in enumerate(func_name.split('_')):
            robot_func_name = i.capitalize() if n==0 else robot_func_name+ " " + i.capitalize()
        UI.keyword_name.append(robot_func_name)

    def get_transdic_keys_and_values(self):
        if UI.translations_key and UI.translations_value:
            for key in UI.translations_key:
                self.label_texts.append(key)
            for value in UI.translations_value:
                self.radio_texts.append(value)

    def output_setting_file(self):
        with open("./setting.txt", "a") as out_file:
            contents = ""
            for i in range(len(self.label_texts)):
                now_selected = self.radio_vars[i].get()               

                format_args=""
                for j in UI.origin_xpaths_or_arguments[i]:
                    format_args += j + "#"
                format_args = format_args[:-1]

                contents += UI.keyword_name[i] + "~" + format_args + "~" + self.label_texts[i] + "~" + self.radio_texts[i][now_selected] + "\n"
            logger.warn(contents)
            out_file.write(contents)

            for i in range(len(self.labels)):
                self.labels[i].grid_forget()
                self.labels_word[i].grid_forget()
                for j in range(len(self.radios[i])):
                    self.radios[i][j].grid_forget()
            self.btn_submit.grid_forget()
    
    def undo_trans(self):
        with open("./setting.txt", "a+") as modi_file:
            if os.stat("./setting.txt").st_size != 0:
                modi_file.seek(0)
                content_rmv = []
                for i in range(len(self.checkbtn_vars)):
                    if self.checkbtn_vars[i].get() == 1:
                        content_rmv.append(self.line_record[i]+'\n')

                new_data = ""
                for line in modi_file.readlines():
                    if line not in content_rmv:
                        new_data += line
                modi_file.seek(0)
                modi_file.truncate()
                modi_file.write(new_data)       
            self.record_ui.destroy()

    def draw_trans_options(self):
        self.labels = []   #label 1

        self.labels_word = [] #label 2
        self.label_texts = []

        self.radios = []
        self.radio_vars = []
        self.radio_texts = []
        self.get_transdic_keys_and_values()
        for i in range(len(self.label_texts)):
            self.radio_vars.append(IntVar())
            self.radios.append([])

            args = " "
            for k in range(len(UI.origin_xpaths_or_arguments[i])):
                args = args + UI.origin_xpaths_or_arguments[i][k] if k==0 else args + " , " + UI.origin_xpaths_or_arguments[i][k]

            self.labels.append(Label(self.win, text="關鍵字:%s, 參數部分是:%s  " % 
            (UI.keyword_name[i] , args), font=self.fontStyle))
            self.labels[i].grid( column=0,row=i, sticky=W+N+S, padx=10, pady=3)

            self.labels_word.append(Label(self.win, text="%s可以被翻譯成: " % 
            (self.label_texts[i]), font=self.fontStyle, fg = "red"))
            self.labels_word[i].grid( column=1,row=i, sticky=W+N+S, padx=10, pady=3)

            for j in range(len(self.radio_texts[i])):
                default_value = j
                self.radios[i].append(Radiobutton(self.win, variable=self.radio_vars[i], text=self.radio_texts[i][j], font=self.fontStyle, value=default_value))
                self.radios[i][j].grid(columnspan=1, column=2+j, row=i, sticky=W+N+S, pady=3)

    def open_record(self):
        self.record_ui = Toplevel(self.win)
        self.record_ui.title("使用者翻譯紀錄")
        self.record_ui.geometry('+250+250')

        with open("./setting.txt", 'a+') as file:
            if os.stat("./setting.txt").st_size != 0:
                file.seek(0)

                self.checkbtns = []
                self.checkbtn_vars = []
                self.checkbtn_texts = []
                self.line_record = []
                for line in file.readlines():
                    self.line_record.append(line.strip('\n')) 
                    line_split = line.strip('\n').split('~')
                    present_str = "關鍵字:%s, 參數部分:%s . 待翻譯詞:%s, 翻譯:%s" %(line_split[0],line_split[1].replace('#',', '), line_split[2], line_split[3])
                    self.checkbtn_texts.append(present_str)
                
                for i in range(len(self.checkbtn_texts)):
                    self.checkbtn_vars.append(IntVar())
                    self.checkbtns.append(Checkbutton(self.record_ui, variable=self.checkbtn_vars[i], text=self.checkbtn_texts[i], font=self.fontStyle, \
                                                        bg='light green'))
                    self.checkbtns[i].grid(column=0, row=i, sticky=W+N+S, padx=10, pady=3)
            
            text_undo = StringVar()
            btn_undo = Button(self.record_ui, textvariable=text_undo, command= self.undo_trans, font=self.fontStyle, bg="#ff8a15", fg="white", height=1, width=8)
            text_undo.set("Undo")
            btn_undo.grid(row=10, column=0, sticky=S+E, padx=10, pady=5, columnspan=3)

    def run(self):
        self.win = Tk()    
        self.win.title("一詞多譯")
        self.win.geometry('+200+300')        
        self.fontStyle = tkFont.Font(family ="Helvetica", size=14)
        self.draw_trans_options()
        
        self.instructions = Label(self.win, text="Choose the translation(s) you want!!", font=self.fontStyle)
        self.instructions.grid(row=10, sticky=S+W, padx=10, pady=5)

        self.text_record = StringVar()
        self.btn_record = Button(self.win, textvariable=self.text_record, command= self.open_record, font=self.fontStyle, bg="#8c4646", fg="white", height=2, width=15)
        self.text_record.set("TransRecord")
        self.btn_record.grid(row=10, column=1, sticky=S+E, padx=10, pady=5)

        self.text_submit = StringVar()
        self.btn_submit = Button(self.win, textvariable=self.text_submit, command= lambda:self.output_setting_file(), font=self.fontStyle, bg="#20bebe", fg="white", height=2, width=15)
        self.text_submit.set("Submit")
        self.btn_submit.grid(row=10, column=2, sticky=S+E, padx=10, pady=5, columnspan=10)

        self.win.mainloop()


  
if __name__=='__main__':
    self.run()