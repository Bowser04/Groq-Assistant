
#from pyshortcuts import make_shortcut
import winshell
#make_shortcut('assistant.py', name='Windows Groq Assistant', icon='icon.ico')
import os
import shutil
from win32com.client import Dispatch
import pathlib
objShell = Dispatch("WScript.Shell")
allUserProgramsMenu = objShell.SpecialFolders("AllUsersPrograms")
userMenu = objShell.SpecialFolders("StartMenu")
path = os.path.join(str(pathlib.Path().resolve()), "Windows Groq Assistant.lnk")
target = str(pathlib.Path().resolve())+'\\venv\\Scripts\\pythonw.exe'
argument = "assistant.py"
wDir = str(pathlib.Path().resolve())
icon = str(pathlib.Path().resolve())+r"\icon.ico"

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = wDir
shortcut.IconLocation = icon
shortcut.arguments = argument
shortcut.save()

if not input("add to startup ? ([y]/n): ") == "n":
    startup = winshell.startup()
    shutil.copy("Windows Groq Assistant.lnk", startup)
    print("Windows Groq Assistant as benn added to startup")
if not input("add to start menu ? ([y]/n): ") == "n":
    startup = winshell.startup()
    shutil.copy("Windows Groq Assistant.lnk", userMenu)
    print("Windows Groq Assistant as benn added to start menu")