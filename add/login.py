from tkinter import *
import time

class Сoordinate():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y       

LOGIN = Tk()

login_running = True
login_window = Сoordinate(200, 250)
zone = 5
icon_location = r"images\ship.ico"
login_name_1 = "Гравець №1"
login_name_2 = "Гравець №2"


def login_close():
    global login_running
    login_running = False
    LOGIN.destroy()
 
LOGIN.iconbitmap(icon_location)   
LOGIN.protocol("WM_DELETE_WINDOW", login_close)     # функція на вихід з гри
LOGIN.title("Sea Battle | LOGIN")                   # назва гри
LOGIN.resizable(0, 0)                              # параметер на зміну розміру вікна
LOGIN.wm_attributes("-topmost", 1)

background = Canvas(LOGIN, width=login_window.x, height=login_window.y, bd=0, highlightthickness=0)
background.pack()

label_player_1 = Label(LOGIN, text=login_name_1, font=("Helvetica", 12))
label_player_1.place(relx=.5, rely=.1, anchor="c")

name_player_1 = Entry(textvariable=login_name_1)
name_player_1.place(relx=.5, rely=.2, anchor="c")

label_player_2 = Label(LOGIN, text=login_name_2, font=("Helvetica", 12))
label_player_2.place(relx=.5, rely=.3, anchor="c")

name_player_2 = Entry(textvariable=login_name_2)
name_player_2.place(relx=.5, rely=.4, anchor="c")

label_player_3 = Label(LOGIN, text="Розмір зони", font=("Helvetica", 12))
label_player_3.place(relx=.5, rely=.5, anchor="c")

zone_input = Entry(textvariable=zone)
zone_input.place(relx=.5, rely=.6, anchor="c")

label_player_4 = Label(LOGIN, text="(від 4 до 18)", font=("Helvetica", 8))
label_player_4.place(relx=.5, rely=.7, anchor="c")

def show_message():
    global login_running
    global login_name_1
    global login_name_2
    global zone

   
    if name_player_1.get() != "":
        login_name_1 = name_player_1.get()
    if name_player_2.get() != "":
        login_name_2 = name_player_2.get()
    
    try:
        zone = int(zone_input.get())
        if zone < 4 or zone > 18:
            zone = 5
            raise ValueError("ERROR")
    except ValueError:
        label_player_4.configure(fg="red", text="недопустимі параметри")
        return 0
    
    login_running = False
    LOGIN.destroy()

message_button = Button(text="ПІДТВЕРДИТИ", command=show_message)
message_button.place(relx=.5, rely=.9, anchor="c")

while login_running:
    if login_running:
        LOGIN.update_idletasks()
        LOGIN.update()
