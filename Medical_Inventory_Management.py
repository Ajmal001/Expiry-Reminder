import tkinter as tk
import tkinter.ttk
from tkcalendar import Calendar, DateEntry
import os
import time
import smtplib
from datetime import datetime
from tkinter.font import Font
import configparser
import re
import os
import threading
from cryptography.fernet import Fernet


def Log_Out():
    master.destroy()
    Main_Account_Master()


def Admin_Out():
    admin_controls_master.destroy()
    Main_Account_Master()


def toMain_Account():
    visible.place_forget()
    Main_Account()


def toAdmin_Controls():
    visible.place_forget()
    Admin_Controls()


def toAdd_Inventory():
    visible.place_forget()
    Add_Inventory()


def toModify_Groups():
    visible.place_forget()
    Modify_Groups()


def toCheck_Inventory():
    visible.place_forget()
    Check_Inventory()


def toLogs():
    visible.place_forget()
    Logs()


Color = {"bg": "white", "hd": "white", "button": "grey"}


def Login():
    if os.path.exists(".users.db"):
        global login_screen
        global visible
        global username_verify
        global password_verify
        global username_login_Entry
        global password_login_Entry

        username_verify = tk.StringVar()
        password_verify = tk.StringVar()

        login_screen = tk.Frame(main_account_screen, bg = "white")

        tk.Label(login_screen, text="Please enter details below to Login", bg="white", font=("Calibri", 25), borderwidth=5, relief="solid").place(x=120,y=10,width=1126,height=60)
        tk.Button(login_screen, text="Back", width=10, height=1, command = toMain_Account).place(x=120, y=80)
        tk.Label(login_screen, text="Username:", bg="white", font=("Calibri", 20)).place(x=450, y=250, width=250, height=50)
        username_login_Entry = tk.Entry(login_screen, textvariable=username_verify, font=("Calibri", 20))
        username_login_Entry.place(x=650, y=250, width=250, height=50)
        tk.Label(login_screen, text="Password:", bg="white", font=("Calibri", 20)).place(x=450, y=350, width=250, height=50)
        password_login_Entry = tk.Entry(login_screen, textvariable=password_verify, show= '*', font=("Calibri", 20))
        password_login_Entry.place(x=650, y=350, width=250, height=50)
        tk.Button(login_screen, text="Login", width=10, height=1, command = login_verify).place(x=650, y=450, width=100, height=40)
        visible = login_screen
        login_screen.place(x=0, y=0, width=1366, height=768)
    else:
        popupmain("No users have been registerd yet.")


def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_Entry.delete(0, tk.END)
    password_login_Entry.delete(0, tk.END)

    if username1 != "" and password1 != "":
        file = open(".users.db", "r")
        conf = configparser.ConfigParser()
        path = ".admin.ini"
        conf.read(path)
        key = bytes(conf.get("DATA", "d1"), encoding='utf-8')
        cipher = Fernet(key)
        for line in file:
            username = bytes(line.split()[0], encoding='utf-8')
            username = cipher.decrypt(username)
            password = bytes(line.split()[1], encoding='utf-8')
            password = cipher.decrypt(password)
            if username.decode("utf-8") == username1 and password.decode("utf-8") == password1:
                main_account_master.destroy()
                with open(".inventory.lg", "a") as log:
                    username = b"Login: " + username + bytes(" ", "utf-8") + bytes(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "utf-8")
                    msg = cipher.encrypt(username)
                    log.write(msg.decode("utf-8"))
                    log.write("\n")
                Master(username1)
            else:
                popupmain("Username or Password Wrong.")
    else:
        popupmain("Please Enter Username and Password.")


def Admin_Login():

    global visible

    if os.path.exists(".admin.ini"):
        global admin_login_screen
        global username_verify
        global password_verify
        global username_login_Entry
        global password_login_Entry

        username_verify = tk.StringVar()
        password_verify = tk.StringVar()

        admin_login_screen = tk.Frame(main_account_screen, bg = "white")

        tk.Label(admin_login_screen, text="Please enter details below to Login as Admin", bg="white", font=("Calibri", 25), borderwidth=5, relief="solid").place(x=120,y=10,width=1126,height=60)
        tk.Button(admin_login_screen, text="Back", width=10, height=1, command = toMain_Account).place(x=120, y=80)
        tk.Label(admin_login_screen, text="Username:", bg="white", font=("Calibri", 20)).place(x=450, y=250, width=250, height=50)
        username_login_Entry = tk.Entry(admin_login_screen, textvariable=username_verify, font=("Calibri", 20))
        username_login_Entry.place(x=650, y=250, width=250, height=50)
        tk.Label(admin_login_screen, text="Password:", bg="white", font=("Calibri", 20)).place(x=450, y=350, width=250, height=50)
        password_login_Entry = tk.Entry(admin_login_screen, textvariable=password_verify, show= '*', font=("Calibri", 20))
        password_login_Entry.place(x=650, y=350, width=250, height=50)
        tk.Button(admin_login_screen, text="Login", width=10, height=1, command = login_admin_verify).place(x=650, y=450, width=100, height=40)
        visible = admin_login_screen
        admin_login_screen.place(x=0, y=0, width=1366, height=768)
    else:
        global admin_setup_screen
        global username
        global password
        global email

        username = tk.StringVar()
        password = tk.StringVar()
        email = tk.StringVar()

        admin_setup_screen = tk.Frame(main_account_screen, bg = "white")

        tk.Label(admin_setup_screen, text="Please enter details below to Setup Admin Account.", bg="white", font=("Calibri", 25), borderwidth=5, relief="solid").place(x=120,y=10,width=1126,height=60)
        tk.Button(admin_setup_screen, text="Back", width=10, height=1, command = toMain_Account).place(x=120, y=80)
        tk.Label(admin_setup_screen, text="Username:", bg="white", font=("Calibri", 15)).place(x=450, y=250, width=250, height=40)
        username_login_Entry = tk.Entry(admin_setup_screen, textvariable=username, font=("Calibri", 15))
        username_login_Entry.place(x=650, y=250, width=250, height=40)
        tk.Label(admin_setup_screen, text="Password:", bg="white", font=("Calibri", 15)).place(x=450, y=310, width=250, height=40)
        password_login_Entry = tk.Entry(admin_setup_screen, textvariable=password, show= '*', font=("Calibri", 15))
        password_login_Entry.place(x=650, y=310, width=250, height=40)
        tk.Label(admin_setup_screen, text="Mail-ID for Expiry", bg="white", font=("Calibri", 15)).place(x=450, y=370, width=250, height=40)
        tk.Label(admin_setup_screen, text="Notification:", bg="white", font=("Calibri", 15)).place(x=450, y=400, width=250, height=40)
        password_login_Entry = tk.Entry(admin_setup_screen, textvariable=email, font=("Calibri", 15))
        password_login_Entry.place(x=650, y=400, width=250, height=40)
        tk.Button(admin_setup_screen, text="Register", width=10, height=1, command = register_admin).place(x=650, y=470, width=100, height=40)
        visible = admin_setup_screen
        admin_setup_screen.place(x=0, y=0, width=1366, height=768)


def login_admin_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_Entry.delete(0, tk.END)
    password_login_Entry.delete(0, tk.END)

    if username1 != "" and password1 != "":
        conf = configparser.ConfigParser()
        path = ".admin.ini"
        conf.read(path)
        key = bytes(conf.get("DATA", "d1"), encoding='utf-8')
        cipher = Fernet(key)
        user = bytes(conf.get("DATA", "d2"), encoding='utf-8')
        passw = bytes(conf.get("DATA", "d3"), encoding='utf-8')
        if username1 == cipher.decrypt(user).decode("utf-8") and password1 == cipher.decrypt(passw).decode("utf-8"):
            main_account_master.destroy()
            Admin_Controls_Master()
        else:
            popupmain("Username or Password Wrong.")
    else:
        popupmain("Please Enter Username and Password.")


def register_admin():
    user = username.get()
    passw = password.get()
    mail = email.get()
    pattern = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"
    if user != "" and passw != "" and re.search(pattern, mail):
        with open(".admin.ini", "w") as file:
            initial = "[DATA]\nD1 = \nD2 = \nD3 = \nD4 = "
            file.write(initial)
        key = Fernet.generate_key()
        cipher = Fernet(key)
        config = configparser.ConfigParser()
        path = (".admin.ini")
        config.read(path)
        update_setting(path, config, "DATA", "D1", key.decode("utf-8"))
        update_setting(path, config, "DATA", "D2", cipher.encrypt(bytes(user, encoding='utf-8')).decode("utf-8"))
        update_setting(path, config, "DATA", "D3", cipher.encrypt(bytes(passw, encoding='utf-8')).decode("utf-8"))
        update_setting(path, config, "DATA", "D4", mail)
        popupmain("Admin succesfully registered.")
    else:
        popupmain("Please enter all fields.")


def Register():
    global register_screen
    global username
    global password
    global username_Entry
    global password_Entry
    global visible

    register_screen = tk.Frame(admin_controls_master, bg = "white")
    username = tk.StringVar()
    password = tk.StringVar()

    tk.Button(register_screen, text="Back", width=10, height=1, command = toAdmin_Controls).place(x=120, y=80)
    tk.Label(register_screen, text="Please enter details below to Register", bg="white", font=("Calibri", 25), borderwidth=5, relief="solid").place(x=120,y=10,width=1126,height=60)
    tk.Label(register_screen, text="Username:", bg="white", font=("Calibri", 20)).place(x=450, y=250, width=250, height=50)
    username_Entry = tk.Entry(register_screen, textvariable=username, font=("Calibri", 20))
    username_Entry.place(x=650, y=250, width=250, height=50)
    tk.Label(register_screen, text="Password:", bg="white", font=("Calibri", 20)).place(x=450, y=350, width=250, height=50)
    password_Entry = tk.Entry(register_screen, textvariable=password, show='*', font=("Calibri", 20))
    password_Entry.place(x=650, y=350, width=250, height=50)
    tk.Button(register_screen, text="Register", width=10, height=1, command = register_user).place(x=650, y=450, width=100, height=40)
    visible = register_screen
    register_screen.place(x=0, y=0, width=1366, height=768)


def register_user():

    username_info = username.get()
    password_info = password.get()
    if username_info != "" and password_info != "":
        file = open(".users.db", "r")
        conf = configparser.ConfigParser()
        path = ".admin.ini"
        conf.read(path)
        key = bytes(conf.get("DATA", "d1"), encoding='utf-8')
        cipher = Fernet(key)
        if cipher.encrypt(bytes(username_info, encoding='utf-8')).decode("utf-8") not in file:
            file = open(".users.db", "a")
            file.write(cipher.encrypt(bytes(username_info, encoding='utf-8')).decode("utf-8") + " ")
            file.write(cipher.encrypt(bytes(password_info, encoding='utf-8')).decode("utf-8") + "\n")
            file.close()
            username_Entry.delete(0, tk.END)
            password_Entry.delete(0, tk.END)
        else:
            popupmain("Username Already Taken.")
    else:
        popupmain("Please Enter Username and Password.")


def Modify_Groups():
    global modify_groups_screen
    global place_holder
    global visible
    global new_grp
    global new_type
    global groupsbox2

    new_grp = tk.StringVar()
    new_type = tk.StringVar()

    modify_groups_screen = tk.Frame(master, bg="white")

    tk.Label(modify_groups_screen, text="Modify Groups", bg="white", font=("Calibri", 25), borderwidth=5, relief="solid").place(x=120,y=10,width=1126,height=60)

    tk.Label(modify_groups_screen, text="Groups", bg="white", font=("Calibri", 25)).place(x=160,y=75,width=120,height=50)
    groupsbox2 = tk.Listbox(modify_groups_screen)
    groups = Get_Groups()
    for group in groups:
        groupsbox2.insert(tk.END, group)
    groupsbox2.bind("<Double-Button-1>", Draw_Types_Box)
    groupsbox2.place(x=40,y=120,width=400,height=550)

    tk.Label(modify_groups_screen, text="Types", bg="white", font=("Calibri", 25)).place(x=620,y=75,width=100,height=50)
    place_holder = tk.Label(modify_groups_screen, text="Please Choose a group first.", bg="white", borderwidth=5, relief="solid")
    place_holder.place(x=490,y=120,width=400,height=550)

    tk.Label(modify_groups_screen, text="Add New Group", bg="white").place(x=1065, y=180)
    tk.Entry(modify_groups_screen, textvariable=new_grp, width=30).place(x=1000, y=210)
    tk.Button(modify_groups_screen, text='Add Group', command=Add_Group).place(x=1075, y=240)

    tk.Label(modify_groups_screen, text="Add New Type to Selcted Group", bg="white").place(x=1025, y=300)
    tk.Entry(modify_groups_screen, textvariable=new_type, width=30).place(x=1000, y=330)
    tk.Button(modify_groups_screen, text='Add Type', command=Add_Type).place(x=1075, y=360)

    tk.Button(modify_groups_screen, text='Delete Selected Group', command=Delete_Group).place(x=1035, y=420)

    tk.Button(modify_groups_screen, text='Delete Type from Selcted Group', command=Delete_Type).place(x=1000, y=480)

    visible = modify_groups_screen
    modify_groups_screen.place(x=0, y=0, width=1366, height=768)


def update_setting(path, config, section, setting, value):
    #Update a setting
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)


def get_setting(config, section):
    #Returns a value
    value = config.get(section, "type")
    return value


def sel(event):
    global type
    widget = event.widget
    selection = widget.curselection()
    type = widget.get(selection[0]).strip()
    return type


def log_sel(event):
    global log
    global labels
    global log_frame

    widget = event.widget
    selection = widget.curselection()
    logs = open(".inventory.lg", "r")
    for i, line in enumerate(logs):
        if i == selection[0]:
            conf = configparser.ConfigParser()
            path = ".admin.ini"
            conf.read(path)
            key = bytes(conf.get("DATA", "d1"), encoding='utf-8')
            cipher = Fernet(key)
            line = cipher.decrypt(bytes(line, encoding='utf-8'))
            data = line.decode("utf-8")
    logs.close()
    log_frame = tk.Frame(logs_screen, bg="white")
    log_frame.place(x=900, y=100, width=400, height=600)

    if len(data.split()) == 4:
        log_frame = tk.Frame(logs_screen, bg="white")
        L1 = tk.Label(log_frame, text="Username :", bg="white", font=("Calibri", 13))
        L1.place(x=40, y=50)
        L2 = tk.Label(log_frame, text=data.split()[1], bg="white", font=("Calibri", 13))
        L2.place(x=210, y=50)
        L3 = tk.Label(log_frame, text="Logged in on :", bg="white", font=("Calibri", 13))
        L3.place(x=40, y=100)
        L4 = tk.Label(log_frame, text=data.split()[2], bg="white", font=("Calibri", 13))
        L4.place(x=210, y=100)
        L5 = tk.Label(log_frame, text=data.split()[3], bg="white", font=("Calibri", 13))
        L5.place(x=210, y=140)
        log_frame.place(x=900, y=100, width=400, height=600)
    elif len(data.split()) == 5:
        log_frame.place_forget()
        log_frame = tk.Frame(logs_screen, bg="white")
        L1 = tk.Label(log_frame, text="Product :", bg="white", font=("Calibri", 13))
        L1.place(x=40, y=50)
        L2 = tk.Label(log_frame, text=data.split()[1], bg="white", font=("Calibri", 13))
        L2.place(x=210, y=50)
        L3 = tk.Label(log_frame, text="Type :", bg="white", font=("Calibri", 13))
        L3.place(x=40, y=100)
        L4 = tk.Label(log_frame, text=data.split()[2], bg="white", font=("Calibri", 13))
        L4.place(x=210, y=100)
        L5 = tk.Label(log_frame, text="Deleted on :", bg="white", font=("Calibri", 13))
        L5.place(x=40, y=150)
        L6 = tk.Label(log_frame, text=data.split()[3], bg="white", font=("Calibri", 13))
        L6.place(x=210, y=150)
        L7 = tk.Label(log_frame, text=data.split()[4], bg="white", font=("Calibri", 13))
        L7.place(x=210, y=190)
        log_frame.place(x=900, y=100, width=400, height=600)
    elif len(data.split()) == 7:
        log_frame.place_forget()
        log_frame = tk.Frame(logs_screen, bg="white")
        L1 = tk.Label(log_frame, text="Product :", bg="white", font=("Calibri", 13))
        L1.place(x=40, y=50)
        L2 = tk.Label(log_frame, text=data.split()[1], bg="white", font=("Calibri", 13))
        L2.place(x=210, y=50)
        L3 = tk.Label(log_frame, text="Type :", bg="white", font=("Calibri", 13))
        L3.place(x=40, y=100)
        L4 = tk.Label(log_frame, text=data.split()[2], bg="white", font=("Calibri", 13))
        L4.place(x=210, y=100)
        L5 = tk.Label(log_frame, text="Inserted on :", bg="white", font=("Calibri", 13))
        L5.place(x=40, y=150)
        L6 = tk.Label(log_frame, text=data.split()[5], bg="white", font=("Calibri", 13))
        L6.place(x=210, y=150)
        L7 = tk.Label(log_frame, text=data.split()[6], bg="white", font=("Calibri", 13))
        L7.place(x=210, y=190)
        log_frame.place(x=900, y=100, width=400, height=600)
    else:
        log_frame.place_forget()
        log_frame = tk.Frame(logs_screen, bg="white")
        L1 = tk.Label(log_frame, text="Product :", bg="white", font=("Calibri", 13))
        L1.place(x=40, y=50)
        L2 = tk.Label(log_frame, text=data.split()[1], bg="white", font=("Calibri", 13))
        L2.place(x=210, y=50)
        L3 = tk.Label(log_frame, text="Type :", bg="white", font=("Calibri", 13))
        L3.place(x=40, y=100)
        L4 = tk.Label(log_frame, text=data.split()[2], bg="white", font=("Calibri", 13))
        L4.place(x=210, y=100)
        L5 = tk.Label(log_frame, text="Quantity used up :", bg="white", font=("Calibri", 13))
        L5.place(x=40, y=150)
        L6 = tk.Label(log_frame, text=int(data.split()[5])-int(data.split()[6]), bg="white", font=("Calibri", 13))
        L6.place(x=210, y=150)
        L7 = tk.Label(log_frame, text="Changed on :", bg="white", font=("Calibri", 13))
        L7.place(x=40, y=200)
        L8 = tk.Label(log_frame, text=data.split()[7], bg="white", font=("Calibri", 13))
        L8.place(x=210, y=200)
        L9 = tk.Label(log_frame, text=data.split()[8], bg="white", font=("Calibri", 13))
        L9.place(x=210, y=240)
        log_frame.place(x=900, y=100, width=400, height=600)


def reading_type(event):
    widget = event.widget
    selection = widget.curselection()
    name = widget.get(selection[0]).strip()
    file = open("inventory.db", "r")
    for line in file:
        if line.split()[0].replace("_", " ") == name:
            display_reading_type(line)


def display_reading_type(line):
    global text
    global qty
    global reading_type_frame

    text = line.split()
    reading_type_frame.place_forget()
    reading_type_frame = tk.Frame(modify_inventory_screen, bg="white")
    qty = tk.IntVar(reading_type_frame, text[5])
    tk.Label(reading_type_frame, text="Name:", bg="white").place(x = 0, y = 0)
    tk.Label(reading_type_frame, text=text[0].replace("_", " "), bg="white").place(x = 100, y = 0)
    tk.Label(reading_type_frame, text="Date of Expiry:", bg="white").place(x = 0, y = 30)
    tk.Label(reading_type_frame, text=text[3], bg="white").place(x = 100, y = 30)
    tk.Label(reading_type_frame, text="Quantity Left:", bg="white").place(x = 0, y = 60)
    tk.Entry(reading_type_frame, textvariable=qty).place(x = 100, y = 60)
    tk.Button(reading_type_frame, text="Update Quantity", command=Update_Qty).place(x=40, y=90)
    tk.Button(reading_type_frame, text="Delete from Inventory", command=Delete).place(x=195, y=90)
    reading_type_frame.place(x = 500, y = 550, width=500, height=500)


def Get_Types(group):
    config = configparser.ConfigParser()
    path = "Config.ini"
    config.read(path)
    types = get_setting(config, group).split(", ")
    return types


def Draw_Types_Box(event):
    global typesbox
    global current_selection
    widget = event.widget
    current_selection = widget.curselection()
    group = widget.get(current_selection[0]).strip()
    types = Get_Types(group)
    typesbox = tk.Listbox(visible)
    for type in types:
        typesbox.insert(tk.END, type)
    typesbox.bind("<Double-Button-1>", sel)
    typesbox.place(x=490,y=120,width=400,height=550)


def Draw_Types_Box_Same_Place(event):
    global typesbox
    global current_selection

    L1.place_forget()
    tk.Label(modify_inventory_screen, text="Types", bg="white", font=("Calibri", 25)).place(x=160,y=75,width=120,height=50)
    tk.Button(modify_inventory_screen, text="Back", command=Check_Inventory).place(x=40,y=100, width=50,height=20)
    widget = event.widget
    current_selection = widget.curselection()
    group = widget.get(current_selection[0]).strip()
    types = Get_Types(group)
    typesbox = tk.Listbox(visible)
    for type in types:
        typesbox.insert(tk.END, type)
    typesbox.bind("<Double-Button-1>", sel)
    typesbox.place(x=40,y=120,width=400,height=550)


def Get_Groups():
    global config
    global path
    config = configparser.ConfigParser()
    path = "Config.ini"
    config.read(path)
    groups = config.sections()
    return groups


def Add_Group():
    grp = (new_grp.get()).upper()
    groups = Get_Groups()
    if grp not in groups:
        grp = "\n[" + grp + "]\n"
        with open("Config.ini", "a") as confg:
            confg.write(grp)
            confg.write("type = \n")
        toModify_Groups()
        popupmsg("New Group Succesfully Created.")
    else:
        popupmsg("Group already exists.")


def Add_Type():
    type = (new_type.get()).upper()
    try:
        selection = (groupsbox2.curselection())[0]
        groups = Get_Groups()
        group = groups[selection]
        value = get_setting(config, group)
        if type not in value:
            if len(value) > 0:
                value += ", " + type
            else:
                value = type
            update_setting(path, config, group, "type", value)
            toModify_Groups()
            msg = "Type " + type + " added to " + group
            popupmsg(msg)
        else:
            popupmsg("Type already present.")
    except:
        popupmsg("Please select a group first.")


def Delete_Group():
    try:
        selection = (groupsbox2.curselection())[0]
        groups = Get_Groups()
        group = groups[selection]
        config.remove_section(group)
        with open("Config.ini", "w") as config_file:
            config.write(config_file)
        toModify_Groups()
        msg = "Succesfully deleted " + group + " group."
        popupmsg(msg)
    except:
        popupmsg("Please select a group first.")


def Delete_Type():
    selection = (typesbox.curselection())[0]
    groups = Get_Groups()
    group = groups[current_selection[0]]
    types = Get_Types(group)
    type = types[selection]
    types.remove(type)
    value = ", ".join(types)
    update_setting(path, config, group, "type", value)
    toModify_Groups()


def Add():
    log = open(".inventory.lg", "a")
    nam = (str(name.get())).replace(" ","_")
    dat = str(cal.get())
    qt = str(qty.get())
    typ = str(type)
    if nam != "" and qt != "":
        db = open('inventory.db', 'a')
        datetoday = datetime.now()
        datetoday = str(datetoday.strftime("%x"))
        statement = nam + " " + typ + " " + datetoday + " " + dat + " " + qt + " " + qt +"\n"
        db.write(statement)
        conf = configparser.ConfigParser()
        path = ".admin.ini"
        conf.read(path)
        key = bytes(conf.get("DATA", "d1"), encoding='utf-8')
        cipher = Fernet(key)
        log_statement = "Inserted: " + nam + " " + typ + " " + dat + " " + qt + " " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        msg = cipher.encrypt(bytes(log_statement, "utf-8"))
        log.write(msg.decode("utf-8"))
        log.write("\n")
        popupmsg("Written to file")
    else:
        popupmsg("Fill in all the details")
    log.close()
    db.close()


def Delete():
    file = open("inventory.db", "r")
    temp = open("temp.txt", "w")
    log = open(".inventory.lg", "a")
    for line in file:
        lines = line.split()
        if lines != text:
            temp.write(line)
    conf = configparser.ConfigParser()
    path = ".admin.ini"
    conf.read(path)
    key = bytes(conf.get("DATA", "d1"), encoding='utf-8')
    cipher = Fernet(key)
    log_statement = "Deleted: " +  text[0] + " " + text[1] + " " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    msg = cipher.encrypt(bytes(log_statement, "utf-8"))
    log.write(msg.decode("utf-8"))
    log.write("\n")
    file.close()
    temp.close()
    log.close()
    os.remove("inventory.db")
    os.rename("temp.txt", "inventory.db")
    toCheck_Inventory()
    popupmsg("Item Deleted")


def Update_Qty():
    file = open("inventory.db", "r")
    temp = open("temp.txt", "w")
    log = open(".inventory.lg", "a")
    for line in file:
        lines = line.split()
        if lines != text:
            temp.write(line)
        else:
            line1 = lines[0] + " " + lines[1] + " " + lines[2] + " " + lines[3] + " " + lines[4] + " " + str(qty.get()) + "\n"
            use = int(lines[5]) - qty.get()
            UpdateUsage(lines[1], use)
            temp.write(line1)
    conf = configparser.ConfigParser()
    path = ".admin.ini"
    conf.read(path)
    key = bytes(conf.get("DATA", "d1"), encoding='utf-8')
    cipher = Fernet(key)
    log_statement = "Changed: " + lines[0] + " " + lines[1] + " " + lines[2] + " " + lines[3] + " " + lines[4] + " " + str(qty.get()) + " " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    msg = cipher.encrypt(bytes(log_statement, "utf-8"))
    log.write(msg.decode("utf-8"))
    log.write("\n")
    log.close()
    file.close()
    temp.close()
    os.remove("inventory.db")
    os.rename("temp.txt", "inventory.db")
    toCheck_Inventory()
    popupmsg("Quantity Updated.")


def Search_Type():
    global searchbox1

    selection = (typesbox.curselection())[0]
    groups = Get_Groups()
    group = groups[current_selection[0]]
    types = Get_Types(group)
    type = types[selection]
    file = open("inventory.db", "r")
    searchbox1 = tk.Listbox(modify_inventory_screen)
    for line in file:
        text = line.split()
        if text[1] == type:
            searchbox1.insert(tk.END, text[0].replace("_", " "))
    tk.Label(modify_inventory_screen, text="Names", bg="white", font=("Calibri", 25)).place(x=850,y=80,width=400,height=40)
    searchbox1.bind("<Double-Button-1>", reading_type)
    searchbox1.place(x=850, y=120, width=400,height=400)


def Search_Name():
    file = open("inventory.db", "r")
    searchbox1 = tk.Listbox(modify_inventory_screen)
    for line in file:
        text = line.split()
        name = str(search_name.get())
        if text[0] == name.replace(" ", "_"):
            display_reading_type(line)


def Search_Date(date):
    file = open("inventory.db", "r")
    searchbox1 = tk.Listbox(modify_inventory_screen)
    for line in file:
        text = line.split()
        times = {'In 24 Hours':24,'This Week':(24*7),'This Month':(24*7*4),'Next Three Months':(24*7*4*3),'Next Six Months':(24*7*4*6)}
        obj = " ".join(line.split()[-3:-2])
        time = datetime.strptime(obj, "%d/%m/%y")
        diff = ((time - datetime.now()).total_seconds())/3600
        print(diff)
        searchbox1 = tk.Listbox(modify_inventory_screen)
        if diff <= times[date]:
            searchbox1.insert(tk.END, text[0].replace("_", " "))
        tk.Label(modify_inventory_screen, text="Names", bg="white", font=("Calibri", 25)).place(x=850,y=80,width=400,height=40)
        searchbox1.bind("<Double-Button-1>", reading_type)
        searchbox1.place(x=850, y=120, width=400,height=400)


def popupmsg(msg):
    popup = tk.Toplevel(master)
    popup.wm_title("!")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def popupmain(msg):
    popup = tk.Toplevel(main_account_screen)
    popup.wm_title("!")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def Check_Inventory():
    global modify_inventory_screen
    global visible
    global L1
    global search_name
    global timeline
    global reading_type_frame

    search_name = tk.StringVar()

    modify_inventory_screen = tk.Frame(master, bg = "white")
    tk.Label(modify_inventory_screen, text="Check Inventory", bg="white", font=("Calibri", 25), borderwidth=5, relief="solid").place(x=120,y=10,width=1126,height=60)

    L1 = tk.Label(modify_inventory_screen, text="Groups", bg="white", font=("Calibri", 25))
    L1.place(x=160,y=75,width=120,height=50)


    groupsbox = tk.Listbox(modify_inventory_screen)
    groups = Get_Groups()
    for group in groups:
        groupsbox.insert(tk.END, group)
    groupsbox.bind("<Double-Button-1>", Draw_Types_Box_Same_Place)
    groupsbox.place(x=40,y=120,width=400,height=550)

    tk.Label(modify_inventory_screen, text="Search by time remaining before Expiry", bg="white").place(x=500, y=130)
    timeline = tk.StringVar(modify_inventory_screen)
    choices = { 'In 24 Hours','This Week','This Month','Next Three Months','Next Six Months'}
    timeline.set('In 24 Hours')
    timeMenu = tk.OptionMenu(modify_inventory_screen, timeline, *choices, command=Search_Date).place(x=500,y=150)

    tk.Button(modify_inventory_screen, text='Search by Type', command=Search_Type).place(x=500, y=250)
    tk.Label(modify_inventory_screen, text="Name", bg="white").place(x=500, y=300)
    tk.Entry(modify_inventory_screen, textvariable=search_name, width=30).place(x=500, y=330)
    tk.Button(modify_inventory_screen, text='Search by Name', command=Search_Name).place(x=500, y=360)

    reading_type_frame = tk.Frame(modify_inventory_screen, bg="white")
    reading_type_frame.place(x = 500, y = 550, width=500, height=500)

    visible = modify_inventory_screen
    modify_inventory_screen.place(x=0, y=0, width=1366, height=768)


def Add_Inventory():
    global add_inventory_screen
    global name
    global type
    global cal
    global qty
    global place_holder
    global visible

    add_inventory_screen = tk.Frame(master, bg = "white")

    name = tk.StringVar(add_inventory_screen)
    qty = tk.StringVar(add_inventory_screen)

    tk.Label(add_inventory_screen, text="Add to Inventory", bg="white", font=("Calibri", 25), borderwidth=5, relief="solid").place(x=120,y=10,width=1126,height=60)

    tk.Label(add_inventory_screen, text="Groups", bg="white", font=("Calibri", 25)).place(x=160,y=75,width=120,height=50)
    groupsbox = tk.Listbox(add_inventory_screen)
    groups = Get_Groups()
    for group in groups:
        groupsbox.insert(tk.END, group)
    groupsbox.bind("<Double-Button-1>", Draw_Types_Box)
    groupsbox.place(x=40,y=120,width=400,height=550)

    tk.Label(add_inventory_screen, text="Types", bg="white", font=("Calibri", 25)).place(x=620,y=75,width=100,height=50)
    place_holder = tk.Label(add_inventory_screen, text="Please Choose a group first.", bg="white", borderwidth=5, relief="solid")
    place_holder.place(x=490,y=120,width=400,height=550)

    tk.Label(add_inventory_screen, text="Name", bg="white").place(x=950, y=310)
    tk.Entry(add_inventory_screen, textvariable=name,width=30).place(x=1050, y=310)

    tk.Label(add_inventory_screen, text="Date of Expiry", bg="white").place(x=950, y=340)
    cal = DateEntry(add_inventory_screen, width=29, background='black', foreground='white', borderwidth=2)
    cal.place(x=1050, y=340)

    tk.Label(add_inventory_screen, text="Quantity", bg="white").place(x=950, y=370)
    tk.Entry(add_inventory_screen, textvariable=qty,width=30).place(x=1050, y=370)

    tk.Button(add_inventory_screen, text = 'Save to file', command=Add).place(x=1075, y=400)

    visible = add_inventory_screen
    add_inventory_screen.place(x=0, y=0, width=1366, height=768)


def Logsbox(timeline):
    logsfile = open(".inventory.lg", "r")
    logsbox = tk.Listbox(logs_screen)
    conf = configparser.ConfigParser()
    path = ".admin.ini"
    conf.read(path)
    key = bytes(conf.get("DATA", "d1"), encoding='utf-8')
    cipher = Fernet(key)
    for log in logsfile:
        log_ = cipher.decrypt(bytes(log, encoding='utf-8'))
        text = ""
        obj = " ".join(log_.decode("utf-8").split()[-2:])
        time = datetime.strptime(obj, "%m/%d/%Y, %H:%M:%S")
        diff = ((datetime.now() - time).total_seconds())/3600
        if timeline == 'Last 24 Hours' and diff < 24:
            for txt in log_.split()[0:2]:
                text += txt.decode("utf-8") + " "
            logsbox.insert(tk.END, text)
        elif timeline == 'Last Week' and diff < 24*7:
            for txt in log_.split()[0:2]:
                text += txt.decode("utf-8") + " "
            logsbox.insert(tk.END, text)
        elif timeline == 'Last Month' and diff < 24*7*30:
            for txt in log_.split()[0:2]:
                text += txt.decode("utf-8") + " "
            logsbox.insert(tk.END, text)
        elif timeline == 'Last Year' and diff < 24*7*30*365:
            for txt in log_.split()[0:2]:
                text += txt.decode("utf-8") + " "
            logsbox.insert(tk.END, text)
        elif timeline == 'All':
            for txt in log_.split()[0:2]:
                text += txt.decode("utf-8") + " "
            logsbox.insert(tk.END, text)
    logsbox.bind("<Double-Button-1>", log_sel)
    logsbox.place(x=83,y=170,width=800,height=500)


def Logs():
    global logs_screen
    global logsbox
    global current_selection
    global visible
    global timeline

    logs_screen = tk.Frame(admin_controls_master, bg="white")

    tk.Label(logs_screen, text="Logs", bg="white", font=("Calibri", 25), borderwidth=5, relief="solid").place(x=120,y=10,width=1126,height=60)
    tk.Button(logs_screen, text="Back", width=10, height=1, command = toAdmin_Controls).place(x=120, y=80)
    timeline = tk.StringVar(logs_screen)
    choices = { 'Last 24 Hours','Last Week','Last Month','Last Year','All'}
    timeline.set('Last 24 Hours')
    timeMenu = tk.OptionMenu(logs_screen, timeline, *choices, command=Logsbox).place(x=83,y=120)
    Logsbox(timeline.get())
    visible = logs_screen
    logs_screen.place(x=0, y=0, width=1366, height=768)


def Admin_Controls():
    global admin_controls_screen
    global visible

    admin_controls_screen = tk.Frame(admin_controls_master, bg="white")


    tk.Label(admin_controls_screen, text="Select Your Choice", bg="white", font=("Calibri", 25), borderwidth=5, relief="solid").place(x=120,y=10,width=1126,height=60)
    tk.Button(admin_controls_screen, text="View Logs", height="2", width="30", command = toLogs).place(x=533,y=250,width=300,height=100)
    tk.Button(admin_controls_screen, text="Register New User", height="2", width="30", command = Register).place(x=533,y=400,width=300,height=100)


    visible = admin_controls_screen
    admin_controls_screen.place(x=0, y=0, width=1366, height=768)


def Admin_Controls_Master():
    global admin_controls_master

    admin_controls_master = tk.Tk()
    admin_controls_master.title("Admin Controls")
    admin_controls_master.geometry("1366x768")
    admin_controls_master.configure(bg="white")
    menubar = tk.Menu(admin_controls_master)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="View Logs", command=Logs)
    filemenu.add_command(label="Register New User", command=Register)
    filemenu.add_command(label="Log Out", command=Admin_Out)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=admin_controls_master.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    admin_controls_master.config(menu=menubar)
    Admin_Controls()
    admin_controls_master.mainloop()


def Main_Account():
    global main_account_screen
    global visible

    main_account_screen = tk.Frame(main_account_master, bg = "white")

    tk.Label(main_account_screen, text="Select Your Choice", bg="white", font=("Calibri", 25), borderwidth=5, relief="solid").place(x=120,y=10,width=1126,height=60)
    tk.Button(main_account_screen, text="Login", height="2", width="30", command = Login).place(x=533,y=250,width=300,height=100)
    tk.Button(main_account_screen, text="Admin Login", height="2", width="30", command = Admin_Login).place(x=533,y=400,width=300,height=100)

    visible = main_account_screen
    main_account_screen.place(x=0, y=0, width=1366, height=768)


def Main_Account_Master():
    global main_account_master

    main_account_master = tk.Tk()
    main_account_master.title("Medical Inventory Management")
    main_account_master.geometry("1366x768")
    main_account_master.configure(bg="white")
    Main_Account()
    main_account_master.mainloop()


def Master(user):
    global master

    master = tk.Tk()
    title = "User: " + user
    master.title(title)
    master.geometry("1366x768")
    master.configure(bg="white")

    tk.Label(master, text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).place(x=120,y=10,width=1126,height=60)
    tk.Button(master, text="Add to Inventory", height="2", width="30", command = Add_Inventory).place(x=533,y=250,width=300,height=100)
    tk.Button(master, text="Check Inventory", height="2", width="30", command = Check_Inventory).place(x=533,y=400,width=300,height=100)

    menubar = tk.Menu(master)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Add to Inventory", command=toAdd_Inventory)
    filemenu.add_command(label="Check Inventory", command=toCheck_Inventory)
    filemenu.add_command(label="Modify Groups", command=toModify_Groups)
    filemenu.add_command(label="Log Out", command=Log_Out)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=master.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    master.config(menu=menubar)

    master.mainloop()


def SendMail():
    db = open("inventory.db", "r")
    today = datetime.now()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("expiry.informer@gmail.com", "Simple Password")
    conf = configparser.ConfigParser()
    path = ".admin.ini"
    conf.read(path)
    receiver = conf.get("DATA", "d4")
    temp = open("temp.txt", "w")
    for line in db:
        expiry = line.split()[3]
        org = int(line.split()[4])
        now = int(line.split()[5])
        left = now*100/org
        e_date = datetime.strptime(expiry, "%d/%m/%y")
        days_left = (e_date-today).days
        if days_left == 0:
            msg = line.split()[0] + " expires on " + "today. You still have " + line.split()[5] + " units left."
            server.sendmail("expiry.informer@gmail.com", receiver, msg)
        elif days_left <= 7:
            msg = line.split()[0] + " expires on " + line.split()[3] + ". You still have " + line.split()[5] + " units left."
            server.sendmail("expiry.informer@gmail.com", receiver, msg)
            temp.write(line)
        elif days_left == 30:
            msg = line.split()[0] + " expires on " + line.split()[3] + ". You still have " + line.split()[5] + " units left."
            server.sendmail("expiry.informer@gmail.com", receiver, msg)
            temp.write(line)
        elif left == 0:
            pass
        elif left <= 10:
            msg = "You have less than 10% units of " + line.split()[0] + " left. It expires on " + line.split()[3] + "."
            server.sendmail("expiry.informer@gmail.com", receiver, msg)
            temp.write(line)
        else:
            temp.write(line)
    server.quit()
    temp.close()
    db.close()
    os.remove("inventory.db")
    os.rename("temp.txt", "inventory.db")
    file = open("Mail.txt", "a")
    file.write(datetime.now().strftime("%d-%m-%y"))
    file.close()


def MonthlyInventoryFiles():
    month_year = datetime.now().strftime("%B-%Y")
    usage = "Usage/" + month_year + ".ini"
    if not(os.path.exists("Usage")):
        os.makedirs("Usage")
    if not(os.path.exists(usage)):
        file = open(usage, "w")
        conf = configparser.ConfigParser()
        conf.read("Config.ini")
        config = configparser.ConfigParser()
        config.read(usage)
        sections = conf.sections()
        config["DATA"] = {}
        for section in sections:
            types = conf[section]["type"].split(", ")
            for type in types:
                config["DATA"][type] = "0"
        config.write(file)


def UpdateUsage(type, used):
    month_year = datetime.now().strftime("%B-%Y")
    usage = "Usage/" + month_year + ".ini"
    path = usage
    config = configparser.ConfigParser()
    config.read(usage)
    val = int(config.get("DATA", type.lower()))
    val += used
    update_setting(path, config, "DATA", type.lower(), str(val))


if __name__ == "__main__":
    if not(os.path.exists(".users.db")):
        open(".user.db", "w")
    if not(os.path.exists("Mail.txt")):
        open("Mail.txt", "w")
    MonthlyInventoryFiles()
    Main_Account_Master()
    if datetime.now().strftime("%d-%m-%y") not in open("Mail.txt"):
        SendMail()

## TODO:
## colour
