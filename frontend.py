import tkinter
import requests
import yaml
import json
#from tkinter import Tk, Entry, Button, INSERT

with open("config_frontend.yml","r") as configYaml:
    # opens config file and stores the information to a variable
    config = yaml.load(configYaml, Loader=yaml.SafeLoader)

window = tkinter.Tk()
window.title("Wikipedia-Bot")
entry = tkinter.Entry(window)
entry.pack()
entry.insert(tkinter.INSERT, 'Hello,world!')

def print_content():
    payload = {'searchVal':entry.get()}
    req = requests.post(":".join(["http://"+config['HOSTNAME'],config['PORT']+"/definition/"]), data=payload)
    print(req.text)

button = tkinter.Button(window, text='Print content', command=print_content)

button.pack()

tkinter.mainloop()