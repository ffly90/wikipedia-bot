#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter
import requests
import yaml
import json

def updateText(text, textField):
    textField.delete("1.0", "end")
    textField.insert(tkinter.END, text)

def print_content(short, entry, config, textField):
    payload = {'searchVal': entry.get(), 'short': short}
    req = requests.post(":".join(["http://"+config['HOSTNAME'],config['PORT']+"/definition/"]), data=payload)
    updateText(req.json(), textField)

def main(configFilePath=".config/config_frontend.yml"):
    with open(configFilePath, "r") as configYaml:
        # opens config file and stores the information to a variable
        config = yaml.load(configYaml, Loader=yaml.SafeLoader)
    
    window = tkinter.Tk()

    window.title("Wikipedia-Bot")

    entry = tkinter.Entry(window)
    entry.insert(tkinter.INSERT, 'Suchwort')
    textField = tkinter.Text(window, height=30, width=60, wrap='word')
    button1 = tkinter.Button(window, text='Short Definition', command= lambda: print_content(True, entry, config, textField))
    button2 = tkinter.Button(window, text='Long Definition', command= lambda: print_content(False, entry, config, textField))

    # place widgets
    textField.pack()
    entry.pack()
    button1.pack()
    button2.pack()

    tkinter.mainloop()

if __name__ == "__main__":
   exit(main())