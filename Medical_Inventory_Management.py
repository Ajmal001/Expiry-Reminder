import tkinter as tk
import tkinter.ttk
from tkcalendar import Calendar, DateEntry
import os
import time
from datetime import datetime
from tkinter.font import Font
import configparser
import re


def toAdd_Inventory():
    visible.place_forget()
    Add_Inventory()


def toModify_Groups():
    visible.place_forget()
    Modify_Groups()


def toCheck_Inventory():
    visible.place_forget()
    Check_Inventory()


def Login():
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

    tk.Label(login_screen, text="Username:", bg="white", font=("Calibri", 20)).place(x=450, y=250, width=250, height=50)
    username_login_Entry = tk.Entry(login_screen, textvariable=username_verify, font=("Calibri", 20))
    username_login_Entry.place(x=650, y=250, width=250, height=50)
    tk.Label(login_screen, text="Password:", bg="white", font=("Calibri", 20)).place(x=450, y=350, width=250, height=50)
    password_login_Entry = tk.Entry(login_screen, textvariable=password_verify, show= '*', font=("Calibri", 20))
    password_login_Entry.place(x=650, y=350, width=250, height=50)
    tk.Button(login_screen, text="Login", width=10, height=1, command = login_verify).place(x=650, y=450, width=100, height=40)
    visible = login_screen
    login_screen.place(x=0, y=0, width=1366, height=768)


def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_Entry.delete(0, tk.END)
    password_login_Entry.delete(0, tk.END)

    if username1 != "" and password1 != "":
        file = open("users.db", "r")
        for line in file:
            if line.split()[0] == username1 and line.split()[1] == password1:
                Master()
            else:
                popupmain("Username or Password Wrong.")
    else:
        popupmain("Please Enter Username and Password.")


def Admin_Login():

    global visible

    if os.path.exists("admin.ini"):
        global admin_login_screen
        global username_verify
        global password_verify
        global username_login_Entry
        global password_login_Entry

        username_verify = tk.StringVar()
        password_verify = tk.StringVar()

        admin_login_screen = tk.Frame(main_account_screen, bg = "white")

        tk.Label(admin_login_screen, text="Please enter details below to Login as Admin", bg="white", font=("Calibri", 25), borderwidth=5, relief="solid").place(x=120,y=10,width=1126,height=60)

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
        path = "admin.ini"
        conf.read(path)
        user = conf.get("DATA", "username")
        passw = conf.get("DATA", "password")
        if username1 == user and password1 == passw:
            print("Welcome to Admin Controls.")
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
        print("Yes")
    else:
        print("No")


def Register():
    global register_screen
    register_screen = tk.Frame(main_account_screen, bg = "white")

    global username
    global password
    global username_Entry
    global password_Entry
    username = tk.StringVar()
    password = tk.StringVar()

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
        file = open("users.db", "r")
        for line in file:
            if line.split()[0] != username_info:
                file = open("users.db", "a")
                file.write(username_info + " ")
                file.write(password_info + "\n")
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

    text = line.split()
    qty = tk.IntVar(modify_inventory_screen, text[5])
    tk.Label(modify_inventory_screen, text="Name:", bg="white").place(x = 500, y = 550)
    tk.Label(modify_inventory_screen, text=text[0].replace("_", " "), bg="white").place(x = 600, y = 550)
    tk.Label(modify_inventory_screen, text="Date of Expiry:", bg="white").place(x = 500, y = 580)
    tk.Label(modify_inventory_screen, text=text[3], bg="white").place(x = 600, y = 580)
    tk.Label(modify_inventory_screen, text="Quantity Left:", bg="white").place(x = 500, y = 610)
    tk.Entry(modify_inventory_screen, textvariable=qty).place(x = 600, y = 610)
    tk.Button(modify_inventory_screen, text="Update Quantity", command=Update_Qty).place(x=540, y=640)
    tk.Button(modify_inventory_screen, text="Delete from Inventory", command=Delete).place(x=685, y=640)


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
    log = open("inventory.lg", "a")
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
        log_statement = "Inserted: " + nam + " " + typ + " " + dat + " " + qt + " " + time.ctime() + "\n"
        log.write(log_statement)
        popupmsg("Written to file")
    else:
        popupmsg("Fill in all the details")
    log.close()
    db.close()


def Delete():
    file = open("inventory.db", "r")
    temp = open("temp.txt", "w")
    for line in file:
        lines = line.split()
        if lines != text:
            temp.write(line)
    file.close()
    temp.close()
    os.remove("inventory.db")
    os.rename("temp.txt", "inventory.db")
    toCheck_Inventory()
    popupmsg("Item Deleted")


def Update_Qty():
    file = open("inventory.db", "r")
    temp = open("temp.txt", "w")
    for line in file:
        lines = line.split()
        if lines != text:
            temp.write(line)
        else:
            line1 = lines[0] + " " + lines[1] + " " + lines[2] + " " + lines[3] + " " + lines[4] + " " + str(qty.get()) + "\n"
            temp.write(line1)
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

    tk.Button(modify_inventory_screen, text='Search by Type', command=Search_Type).place(x=500, y=140)

    tk.Label(modify_inventory_screen, text="Name", bg="white").place(x=500, y=300)
    tk.Entry(modify_inventory_screen, textvariable=search_name, width=30).place(x=500, y=330)
    tk.Button(modify_inventory_screen, text='Search by Name', command=Search_Name).place(x=500, y=360)

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
    tkvar = tk.StringVar(add_inventory_screen)
    choices = { 'Syringes','Medicine'}
    tkvar.set('Medicine')
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


def Main_Account():
    global main_account_screen
    global visible

    main_account_screen = tk.Tk()
    main_account_screen.geometry("1366x768")
    main_account_screen.configure(bg="white")

    tk.Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).place(x=120,y=10,width=1126,height=60)
    tk.Button(text="Login", height="2", width="30", command = Login).place(x=533,y=250,width=300,height=100)
    tk.Button(text="Admin Login", height="2", width="30", command = Admin_Login).place(x=533,y=400,width=300,height=100)

    visible = main_account_screen
    main_account_screen.mainloop()


def Master():
    global master

    master = tk.Tk()
    master.title("Inventory Management")
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
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=master.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    master.config(menu=menubar)

    master.mainloop()

Main_Account()
