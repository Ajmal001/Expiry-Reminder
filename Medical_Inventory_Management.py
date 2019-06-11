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


def Modify_Groups():
    global modify_groups_screen
    global place_holder
    global visible
    global new_grp
    global new_type

    new_grp = tk.StringVar()
    new_type = tk.StringVar()

    modify_groups_screen = tk.Frame(master, bg="white")

    tk.Label(modify_groups_screen, text="Modify Groups", bg="white", font=("Calibri", 25), borderwidth=5, relief="solid").place(x=120,y=10,width=1126,height=60)

    tk.Label(modify_groups_screen, text="Groups", bg="white", font=("Calibri", 25)).place(x=160,y=75,width=120,height=50)
    groupsbox = tk.Listbox(modify_groups_screen)
    groups = Get_Groups()
    for group in groups:
        groupsbox.insert(tk.END, group)
    groupsbox.bind("<Double-Button-1>", Get_Types)
    groupsbox.place(x=40,y=120,width=400,height=550)

    tk.Label(modify_groups_screen, text="Types", bg="white", font=("Calibri", 25)).place(x=620,y=75,width=100,height=50)
    place_holder = tk.Label(modify_groups_screen, text="Please Choose a group first.", bg="white", borderwidth=5, relief="solid")
    place_holder.place(x=490,y=120,width=400,height=550)

    tk.Label(modify_groups_screen, text="Add New Group", bg="white").place(x=1065, y=180)
    tk.Entry(modify_groups_screen, textvariable=new_grp, width=30).place(x=1000, y=210)
    tk.Button(modify_groups_screen, text='Add Group', command=Add_Group).place(x=1075, y=240)

    tk.Label(modify_groups_screen, text="Add New Type to Selcted Group", bg="white").place(x=1025, y=300)
    tk.Entry(modify_groups_screen, textvariable=new_type, width=30).place(x=1000, y=330)
    tk.Button(modify_groups_screen, text='Add Type').place(x=1075, y=360)

    tk.Button(modify_groups_screen, text='Delete Selected Group').place(x=1035, y=420)

    tk.Button(modify_groups_screen, text='Delete Type from Selcted Group').place(x=1000, y=480)

    visible = modify_groups_screen
    modify_groups_screen.place(x=0, y=0, width=1366, height=768)


def get_setting(config, section):
    #Returns a value
    value = config.get(section, "types")
    return value


def sel(event):
    global type
    widget = event.widget
    selection = widget.curselection()
    type = widget.get(selection[0]).strip()


def Get_Types(event):
    widget = event.widget
    selection = widget.curselection()
    group = widget.get(selection[0]).strip()
    config = configparser.ConfigParser()
    path = "Config.ini"
    config.read(path)
    types = get_setting(config, group).split(", ")
    typesbox = tk.Listbox(visible)
    for type in types:
        typesbox.insert(tk.END, type)
    typesbox.bind("<Double-Button-1>", sel)
    typesbox.place(x=490,y=120,width=400,height=550)


def Get_Groups():
    global config
    config = configparser.ConfigParser()
    path = "Config.ini"
    config.read(path)
    groups = config.sections()
    return groups


def Add_Group():
    grp = "\n[" + new_grp.get() + "]\n"
    with open("Config.ini", "a") as confg:
        confg.write(grp)
        confg.write("type = \n")
    Modify_Groups()


def Add():
    log = open("inventory.lg", "a")
    nam = (str(name.get())).replace(" ","_")
    dat = str(cal.get())
    qt = str(qty.get())
    typ = type
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


def Delete():
    nam = str(del_name.get())
    if nam != "":
        with open("inventory.db", 'r') as db:
            for line in db:
                li = []
                for word in line.split():
                    li.append(word)
                nam2 = li[0]
                nam2 = nam2.replace("_"," ")
                if nam2 != nam:
                    file = open("temp.db", 'w')
                    file.write(line)
                    file.close()
                elif nam2 == nam:
                    log = open("inventory.lg", "a")
                    log_statement = "Deleted: " + nam + " " + " " + time.ctime() + "\n"
                    log.write(log_statement)
            popupmsg("Deleted")
        os.remove("inventory.db")
        os.rename("temp.db", "inventory.db")
    else:
        popupmsg("Fill in all the details")


def Del_sel():
    nam = str(del_name.get())
    qt = str(del_qty.get())
    if nam!="" and qt!="":
        with open("inventory.db", 'r') as db:
            for line in db:
                li = []
                for word in line.split():
                    li.append(word)
                nam2 = li[0]
                nam2 = nam2.replace("_"," ")
                if nam2 != nam:
                    file = open("temp.db", 'w')
                    file.write(line)
                    file.close()
                else:
                    file = open("temp.db", 'w')
                    org = int(li[5])
                    qt = int(qt)
                    new = str(org-qt)
                    org = str(org)
                    type = li[1]
                    date = li[2]
                    statement = nam + " " + type + " " + date + " " + org + " " + new + "\n"
                    file.write(statement)
                    file.close()
                    log = open("inventory.lg", "a")
                    log_statement = "Deleted: " + nam + " " + type + " " + str(qt) + " " + time.ctime() + "\n"
                    log.write(log_statement)
                    popupmsg("Removed")
        os.remove("inventory.db")
        os.rename("temp.db", "inventory.db")
    else:
        popupmsg("  Fill in all the details")


def popupmsg(msg):
    popup = tk.Toplevel(master)
    popup.wm_title("!")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


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
    groupsbox.bind("<Double-Button-1>", Get_Types)
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
Modify_Groups()

menubar = tk.Menu(master)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Add to Inventory", command=toAdd_Inventory)
filemenu.add_command(label="Modify Groups", command=toModify_Groups)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=master.quit)
menubar.add_cascade(label="File", menu=filemenu)
master.config(menu=menubar)

master.mainloop()
