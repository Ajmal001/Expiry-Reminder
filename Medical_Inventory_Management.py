import tkinter as tk
import tkinter.ttk
from tkcalendar import Calendar, DateEntry
import os
import time
from datetime import datetime
from tkinter.font import Font


def Add():
    log = open("inventory.lg", "a")
    nam = (str(name.get())).replace(" ","_")
    dat = str(cal.get())
    qt = str(qty.get())
    type = str(tkvar.get())
    if nam != "" and qt != "":
        with open('inventory.db', 'a') as db:
            datetoday = datetime.now()
            datetoday = str(datetoday.strftime("%x"))
            statement = nam + " " + type + " " + datetoday + " " + dat + " " + qt + " " + qt +"\n"
            db.write(statement)
            log_statement = "Inserted: " + nam + " " + type + " " + dat + " " + qt + " " + time.ctime() + "\n"
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
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


master = tk.Tk()
master.title("Inventory Management")
master.geometry("320x200")


tk.Label(master, text="   ").grid(row=0,column=0)
name = tk.StringVar(master)
tk.Label(master, text="Name").grid(row=0,column=1)
tk.Entry(master, textvariable=name,width=39).grid(row=0,column=2)


tkvar = tk.StringVar(master)
choices = { 'Syringes','Medicine'}
tkvar.set('Medicine')
popupMenu = tk.OptionMenu(master, tkvar, *choices).grid(row = 1, column =2)
tk.Label(master, text="Type").grid(row = 1, column = 1)


tk.Label(master, text="Date").grid(row=2,column=1)
cal = DateEntry(master, width=36, background='black', foreground='white', borderwidth=2)
cal.grid(row=2,column=2)

qty = tk.StringVar(master)
tk.Label(master, text="Quantity").grid(row=3,column=1)
tk.Entry(master, textvariable=qty,width=39).grid(row=3,column=2)

tk.Button(master, text = 'Save to file', command=Add).grid(row=4,column=2)

del_name = tk.StringVar(master)
tk.Label(master, text="Name").grid(row=5,column=1)
tk.Entry(master, textvariable=del_name,width=39).grid(row=5,column=2)

del_qty = tk.StringVar(master)
tk.Label(master, text="Quantity").grid(row=6,column=1)
tk.Entry(master, textvariable=del_qty,width=39).grid(row=6,column=2)

tk.Button(master, text = 'Delete', command=Delete).grid(row=7,column=1)

tk.Button(master, text = 'Quantity used up', command=Del_sel).grid(row=7,column=2)
master.mainloop()
