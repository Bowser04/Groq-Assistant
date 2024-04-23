import time
import keyboard
import customtkinter
from groq import Groq
import os
import pyperclip
from infi.systray import SysTrayIcon
import sys
import signal
languages = [
    "Afrikaans",
    "Albanian",
    "Amharic",
    "Arabic",
    "Armenian",
    "Azerbaijani",
    "Basque",
    "Bengali",
    "Bengali (India)",
    "Bosnian",
    "Breton",
    "Bulgarian",
    "Catalan",
    "Chinese",
    "Cornish",
    "Croatian",
    "Czech",
    "Danish",
    "Dari",
    "Dutch",
    "English",
    "Estonian",
    "Farsi",
    "Finnish",
    "French",
    "Galician",
    "Georgian",
    "German",
    "Greek",
    "Gujarati",
    "Hausa",
    "Hebrew",
    "Hindi",
    "Hungarian",
    "Igbo",
    "Indonesian",
    "Irish",
    "Italian",
    "Japanese",
    "Kannada",
    "Kazakh",
    "Korean",
    "Kurdish",
    "Kyrgyz",
    "Latvian",
    "Lithuanian",
    "Luxembourgish",
    "Malay",
    "Maltese",
    "Marathi",
    "Mongolian",
    "Montenegrin",
    "Nepali",
    "Norwegian",
    "Occitan",
    "Oromo",
    "Pashto",
    "Polish",
    "Portuguese",
    "Portuguese (Brazil)",
    "Punjabi",
    "Romanian",
    "Russian",
    "Sanskrit",
    "Scottish Gaelic",
    "Serbian",
    "Sinhala",
    "Slovak",
    "Slovenian",
    "Somali",
    "Sorani",
    "Spanish",
    "Swahili",
    "Swedish",
    "Tajik",
    "Tamil",
    "Telugu",
    "Thai",
    "Tibetan",
    "Tigrinya",
    "Turkish",
    "Turkmen",
    "Ukrainian",
    "Urdu",
    "Uzbek",
    "Vietnamese",
    "Welsh",
    "Xhosa",
    "Yoruba",
    "Zulu",
]

stop = False
def quit(systray):
    os.kill(os.getpid(), signal.SIGTERM)
    os.kill(os.getppid(), signal.SIGTERM)
systray = SysTrayIcon("icon.ico", "Example tray icon",on_quit=quit)
systray.start()
if not os.path.exists("apikey"):
    open("apikey","w+").write(input("groq api key (https://console.groq.com/keys) : "))
if not os.path.exists("action"):
    tmp = open("action","+w")
    tmp.write("""resume::resume the folowing text in {language}
respond::respond to the folowing message in {language}
fix::fix the folowing error in {language}""")
    tmp.close()
if not os.path.exists("settings"):
    tmp = open("settings","+w")
    tmp.write("""write::off
clipboard::on
language::english""")
    tmp.close()
client = Groq(
    api_key=open("apikey","r").read(),
)
app = None
settings = {}
settings_checkbox = {}
settings_txt=open("settings").read()
for i in range(len(settings_txt.split("\n"))):
     if settings_txt.split("\n")[i] != "":
        temp = settings_txt.split("\n")[i]
        temp_lst = temp.split("::")
        settings[temp_lst[0]] = temp_lst[1]
language = settings["language"]
action = {}

action_txt=open("action").read()
for i in range(len(action_txt.split("\n"))):
     if action_txt.split("\n")[i] != "":
        temp = action_txt.split("\n")[i]
        temp_lst = temp.split("::")
        action[temp_lst[0]] = temp_lst[1].replace("{language}",language)+" : \n"
print(action)
actual_choice = list(action.keys())[0]
def optionmenu_callback(choice):
    global actual_choice
    print("optionmenu dropdown clicked:", choice)
    actual_choice = choice
def checkbox_settings_write():
    global var_write
    print(var_write.get())
def save_settings(settings_checkbox):
    global settings,language,action,actual_choice
    os.remove("settings")
    settings_file = open("settings","+w")
    settings_txt = ""
    for el in settings_checkbox.items():
        settings[el[0]] = el[1].get()
    for el in settings.items():
        settings_txt+=el[0]+"::"+el[1]+"\n"
    language = settings["language"]
    settings_file.write(settings_txt)
    settings_file.close()
    action_txt=open("action").read()
    for i in range(len(action_txt.split("\n"))):
        if action_txt.split("\n")[i] != "":
            temp = action_txt.split("\n")[i]
            temp_lst = temp.split("::")
            action[temp_lst[0]] = temp_lst[1].replace("{language}",language)+" : \n"
    print(action)
    actual_choice = list(action.keys())[0]
def generate_event():
    global app
    global actual_choice
    global action
    global settings
    print("Generate")
    app.destroy()
    app = None
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"{action[actual_choice]}{pyperclip.paste()}",
        }
    ],
    model="llama3-70b-8192",
    )
    if settings["clipboard"] == "on":
        pyperclip.copy(chat_completion.choices[0].message.content)
    if settings["write"] == "on":
        time.sleep(0.5)
        keyboard.press_and_release("down")
        keyboard.press_and_release("enter")
        keyboard.write(chat_completion.choices[0].message.content)
    else:
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
        app = customtkinter.CTk()  # create CTk window like you do with the Tk window
        app.geometry("800x440")
        app.resizable(False,False)
        app.title("Groq Assistant")
        print(list(action.keys()))
        textbox = customtkinter.CTkTextbox(master=app, width=800,height=440, corner_radius=0)
        textbox.grid(row=0, column=0, sticky="nsew")
        textbox.insert("0.0", chat_completion.choices[0].message.content)
        textbox.configure(state="disabled")
        app.mainloop()
        app.destroy()
        wait_key()
        start_ui()
def settings_event():
    global app
    global actual_choice
    global action
    global languages
    global settings, settings_checkbox
    print("Generate")
    app.destroy()
    app = None
    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("800x440")
    app.resizable(False,False)
    app.title("Groq Assistant")
    ###Seting var
    settings_checkbox["write"] = customtkinter.StringVar(value=settings["write"])
    write = customtkinter.CTkCheckBox(app, text="automatic write response",
                                     variable=settings_checkbox["write"], onvalue="on", offvalue="off")
    write.place(relx=0.05, rely=0.1, anchor=customtkinter.W)
    settings_checkbox["clipboard"] = customtkinter.StringVar(value=settings["clipboard"])
    clipboard = customtkinter.CTkCheckBox(app, text="copy response to the clipboard",
                                     variable=settings_checkbox["clipboard"], onvalue="on", offvalue="off")
    clipboard.place(relx=0.05, rely=0.16, anchor=customtkinter.W)
    optionmenu = customtkinter.CTkOptionMenu(app, values=languages)
    optionmenu.set(settings["language"])
    optionmenu.place(relx=0.05, rely=0.22, anchor=customtkinter.W)
    app.mainloop()
    settings["language"] = optionmenu.get()
    save_settings(settings_checkbox)
    wait_key()
    start_ui()

import keyboard
import time
import sys

def wait_key():
    keyboard.wait("ctrl+alt+g")
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+c')

def start_ui():
    global actual_choice
    global action
    global app
    actual_choice = list(action.keys())[0]
    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("200x240")
    app.resizable(False,False)
    app.title("Groq Assistant")
    print(list(action.keys()))
    settings = customtkinter.CTkButton(app, text="Setings", command=settings_event,width=28,height=28)
    settings.place(relx=0.15, rely=0.08, anchor=customtkinter.CENTER)

    optionmenu = customtkinter.CTkOptionMenu(app, values=list(action.keys()),
                                            command=optionmenu_callback)
    optionmenu.set(list(action.keys())[0])
    optionmenu.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)
    button = customtkinter.CTkButton(app, text="Generate", command=generate_event)
    button.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)
    app.mainloop()
    wait_key()
    start_ui()

try:
    ###Start
    wait_key()
    start_ui()
except Exception as es:
    print(es)
    quit(0)