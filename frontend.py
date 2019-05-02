# -*- coding: utf-8 -*-
import tkinter
import requests
import yaml
import json

#from tkinter import Tk, Entry, Button, INSERT

with open("config_frontend.yml","r") as configYaml:
    # opens config file and stores the information to a variable
    config = yaml.load(configYaml, Loader=yaml.SafeLoader)

def updateText(text):
    textField.delete("1.0", "end")
    textField.insert(tkinter.END, text)

def print_content():
    payload = {'searchVal':entry.get()}
    req = requests.post(":".join(["http://"+config['HOSTNAME'],config['PORT']+"/definition/"]), data=payload)
    updateText(req.json())


window = tkinter.Tk()

window.title("Wikipedia-Bot")

entry = tkinter.Entry(window)
entry.insert(tkinter.INSERT, 'Hello,world!')
button = tkinter.Button(window, text='Print content', command=print_content)
textField = tkinter.Text(window, height=40, width=60)

# place widgets
textField.pack()
entry.pack()
button.pack()

tkinter.mainloop()