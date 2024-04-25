import time
import keyboard
import customtkinter
from groq import Groq
import os
import pyperclip
from infi.systray import SysTrayIcon
import sys
import signal
client = None
add_prompt_temp = []
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
models=["llama3-8b-8192","llama3-70b-8192","llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"]
stop = False
def quit(systray):
    os.kill(os.getpid(), signal.SIGTERM)
    os.kill(os.getppid(), signal.SIGTERM)
systray = SysTrayIcon("icon.ico", "Example tray icon",on_quit=quit)
systray.start()
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
language::english
model::llama3-70b-8192""")
    tmp.close()
api_key_encripted = open("apikey","r").read()
decripted_api_key = False
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
        action[temp_lst[0]] = temp_lst[1].replace("{language}",language).replace("\xa0","\n")+" : \n"
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
    global settings,decripted_api_key
    app.destroy()
    app = None
    print("Generate")
    print(settings["model"])
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"{action[actual_choice]}{pyperclip.paste()}",
        }
    ],
    model=settings["model"],
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
def add_prompt_event():
    global app
    global actual_choice
    global action
    global languages
    global settings, settings_checkbox
    app.destroy()
    app = None
    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("400x400")
    app.resizable(False,False)
    app.title("Groq Assistant")
    ###Seting var
    label = customtkinter.CTkLabel(app,text="Prompt")
    label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)
    write = customtkinter.CTkTextbox(app,width=400,height=100)
    write.place(relx=0, rely=0.3, anchor=customtkinter.W)
    label2 = customtkinter.CTkLabel(app,text="Name")
    label2.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
    write2 = customtkinter.CTkTextbox(app,width=400,height=20)
    write2.place(relx=0, rely=0.55, anchor=customtkinter.W)
    ADD = customtkinter.CTkButton(app, text="Add", command=add_prompt,width=400,height=40)
    ADD.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)
    global add_prompt_temp
    add_prompt_temp = [write,write2]
    app.mainloop()
def add_prompt():
    global add_prompt_temp,action,actual_choice,app
    name = add_prompt_temp[1].get("0.0","end")[0:-1].replace("\n"," ").replace("::",": :")
    prompt = add_prompt_temp[0].get("0.0","end")[0:-1].replace("\n"," ").replace("::",": :")
    print(f"adding prompt '{name}' '{prompt}'")
    tmp = open("action","a")
    tmp.write(f"\n{name}::{prompt}")
    tmp.close()
    action_txt=open("action").read()
    for i in range(len(action_txt.split("\n"))):
        if action_txt.split("\n")[i] != "":
            temp = action_txt.split("\n")[i]
            temp_lst = temp.split("::")
            action[temp_lst[0]] = temp_lst[1].replace("{language}",language).replace("\xa0","\n")+" : \n"
    print(action)
    actual_choice = list(action.keys())[0]
    app.destroy()

def settings_event():
    global app
    global actual_choice
    global action
    global languages
    global settings, settings_checkbox
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
    clipboard.place(relx=0.05, rely=0.18, anchor=customtkinter.W)
    optionmenu_lang = customtkinter.CTkOptionMenu(app, values=languages)
    optionmenu_lang.set(settings["language"])
    optionmenu_lang.place(relx=0.05, rely=0.26, anchor=customtkinter.W)

    optionmenu_model = customtkinter.CTkOptionMenu(app, values=models)
    optionmenu_model.set(settings["model"])
    optionmenu_model.place(relx=0.05, rely=0.34, anchor=customtkinter.W)
    add_prompt = customtkinter.CTkButton(app, text="Add prompt", command=add_prompt_event,width=150,height=50)
    add_prompt.place(relx=0.05, rely=0.80, anchor=customtkinter.W)

    app.mainloop()
    settings["language"] = optionmenu_lang.get()
    settings["model"] = optionmenu_model.get()
    save_settings(settings_checkbox)
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
    if not decripted_api_key:
        def continue_password():
            global api_key_encripted
            from cryptography.fernet import Fernet
            import base64
            import os
            import hashlib
            print(textbox.get("0.0","end").replace("\n",""))
            # Generate a key from the password
            password_key = hashlib.sha256(textbox.get("0.0","end").replace("\n","").encode()).digest()
            key = base64.urlsafe_b64encode(password_key)

            # Create a Fernet instance with the key
            f = Fernet(key)

            # Read the encrypted API key from the file

            try:
                global decripted_api_key,client,app
                # Decrypt the API key
                client = Groq(api_key=f.decrypt(api_key_encripted).decode())
                decripted_api_key = True
                app.destroy()
            except Exception as e:
                print("Nope", str(e))
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
        app = customtkinter.CTk()  # create CTk window like you do with the Tk window
        app.geometry("150x100")
        app.resizable(False,False)
        app.title("Groq Assistant")
        text = customtkinter.CTkLabel(app,text="enter you password")
        text.place(relx=0.15, rely=0.3, anchor=customtkinter.W)
        textbox = customtkinter.CTkTextbox(master=app, width=150,height=40, corner_radius=0)
        textbox.place(relx=0, rely=0.7, anchor=customtkinter.W)
        button = customtkinter.CTkButton(app,150,20,text="continue",command=continue_password)
        button.place(relx=0, rely=0.9, anchor=customtkinter.W)
        app.mainloop()
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