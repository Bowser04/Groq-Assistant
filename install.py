
#from pyshortcuts import make_shortcut

#make_shortcut('assistant.py', name='Windows Groq Assistant', icon='icon.ico')
import os
from win32com.client import Dispatch
import pathlib

path = os.path.join(str(pathlib.Path().resolve()), "Windows Groq Assistant.lnk")
target = str(pathlib.Path().resolve())+r"\venv\Scripts\python.exe assistant.py"
wDir = str(pathlib.Path().resolve())
icon = str(pathlib.Path().resolve())+r"\icon.ico"

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.IconLocation = icon
shortcut.save()