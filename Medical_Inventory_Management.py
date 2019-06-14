import tkinter as tk
import tkinter.ttk
from tkcalendar import Calendar, DateEntry
import os
import time
from datetime import datetime
from tkinter.font import Font
import configparser


def toAdd_Inventory():
    visible.place_forget()
    Add_Inventory()


def toModify_Groups():
    visible.place_forget()
    Modify_Groups()


def toModify_Inventory():
    visible.place_forget()
    Modify_Inventory()


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


def OnMouseWheel(event):
        searchbox1.yview("scroll",event.delta,"units")
        searchbox2.yview("scroll",event.delta,"units")
        searchbox3.yview("scroll",event.delta,"units")


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
    tk.Button(modify_inventory_screen, text="Back", command=Modify_Inventory).place(x=40,y=100, width=50,height=20)
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
        print(group)
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
        with open('inventory.db', 'a') as db:
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


def Search_Type():
    global searchbox1
    global searchbox2
    global searchbox3

    selection = (typesbox.curselection())[0]
    groups = Get_Groups()
    group = groups[current_selection[0]]
    types = Get_Types(group)
    type = types[selection]
    file = open("inventory.db", "r")
    searchbox1 = tk.Listbox(modify_inventory_screen)
    searchbox2 = tk.Listbox(modify_inventory_screen)
    searchbox3 = tk.Listbox(modify_inventory_screen)
    for line in file:
        text = line.split()
        if text[1] == type:
            searchbox1.insert(tk.END, text[0])
            searchbox2.insert(tk.END, text[2])
            searchbox3.insert(tk.END, text[5])
    searchbox1.bind("<MouseWheel>", OnMouseWheel)
    searchbox2.bind("<MouseWheel>", OnMouseWheel)
    searchbox3.bind("<MouseWheel>", OnMouseWheel)
    searchbox1.bind("<Button-4>", OnMouseWheel)
    searchbox2.bind("<Button-4>", OnMouseWheel)
    searchbox3.bind("<Button-4>", OnMouseWheel)
    searchbox1.bind("<Button-5>", OnMouseWheel)
    searchbox2.bind("<Button-5>", OnMouseWheel)
    searchbox3.bind("<Button-5>", OnMouseWheel)
    searchbox1.place(x=850, y=120, width=100,height=550)
    searchbox2.place(x=975, y=120, width=100,height=550)
    searchbox3.place(x=1100, y=120, width=100,height=550)


def Search_Name():
    pass


def popupmsg(msg):
    popup = tk.Toplevel(master)
    popup.wm_title("!")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def Modify_Inventory():
    global modify_inventory_screen
    global visible
    global L1
    global search_name

    search_name = tk.StringVar()

    modify_inventory_screen = tk.Frame(master, bg = "white")
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


master = tk.Tk()
master.title("Inventory Management")
master.geometry("1366x768")

#Add_Inventory()
Modify_Inventory()

menubar = tk.Menu(master)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Add to Inventory", command=toAdd_Inventory)
filemenu.add_command(label="Modify Inventory", command=toModify_Inventory)
filemenu.add_command(label="Modify Groups", command=toModify_Groups)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=master.quit)
menubar.add_cascade(label="File", menu=filemenu)
master.config(menu=menubar)

master.mainloop()
