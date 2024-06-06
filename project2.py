from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import tkinter.messagebox as tkMessageBox
import mysql.connector

def Database():
    global conn, cursor
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project2"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS STUD_REGISTRATON(STU_ID INT AUTO_INCREMENT PRIMARY KEY, STU_NAME VARCHAR(255), STU_CONTACT VARCHAR(255), STU_GMAIL VARCHAR(255), STU_REGNO VARCHAR(255), STU_NATIVE VARCHAR(255))")

def register():
    Database()
    name1 = Name.get()
    con1 = Contact.get()
    gmail1 = Gmail.get()
    regno1 = Regno.get()
    native1 = Native.get()

    if name1 == '' or con1 == '' or gmail1 == '' or regno1 == '' or native1 == '':
        tkMessageBox.showinfo("Warning", "Please Fill Empty Fields!!!")
    else:
        sql = "INSERT INTO STUD_REGISTRATON (STU_NAME, STU_CONTACT, STU_GMAIL, STU_REGNO, STU_NATIVE) VALUES (%s, %s, %s, %s, %s)"
        val = (name1, con1, gmail1, regno1, native1)
        cursor.execute(sql, val)
        conn.commit()
        tkMessageBox.showinfo("Message", "Stored successfully")
        DisplayData()
        conn.close()

def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")
    Name.set("")
    Contact.set("")
    Gmail.set("")
    Regno.set("")
    Native.set("")

def Delete():
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("warning","select data to delete")
    else:
        result = tkMessageBox.askquestion('conform','Are you sure want to delete this record?',icon="warning")
        if result == "yes":
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            sql = "DELETE FROM STUD_REGISTRATON WHERE STU_ID = %s"
            val = (selecteditem[0],)
            cursor.execute(sql, val)
            conn.commit()
            conn.close()

def Searchrecord():
    Database()
    if SEARCH.get() !="":
        tree.delete(*tree.get_children())
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM STUD_REGISTRATON WHERE STU_NAME LIKE %s", ('%' + str(SEARCH.get()) + '%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def DisplayData():
    Database()
    tree.delete(*tree.get_children())
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM STUD_REGISTRATON")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

display_screen = Tk()
display_screen.geometry("900x500")
display_screen.title("STUDENT DATABASE MANAGEMENT SYSTEM")

SEARCH = StringVar()
Name = StringVar()
Contact = StringVar()
Gmail = StringVar()
Regno = StringVar()
Native = StringVar()

TopViewForm = Frame(display_screen, width=600, bd=1, relief=SOLID)
TopViewForm.pack(side=TOP, fill=X)

LForm = Frame(display_screen, width="350")
LForm.pack(side=LEFT, fill=Y)

LeftViewForm = Frame(display_screen, width=800, bd=10, bg="red")
LeftViewForm.pack(side=LEFT, fill=Y)

MidViewForm = Frame(display_screen, width=800)
MidViewForm.pack(side=RIGHT)

lbl_text = Label(TopViewForm, text="STUDENT MANAGEMENT SYSTEM", font=('Britannic Bold', 20), width=60, bg="black", fg="white")
lbl_text.pack(fill=X)

lbl_txtsearch = Label(LForm, text="Personal Details", font=('verdana', 12), bg="white")
lbl_txtsearch.pack()

Label(LForm, text="Name", font=('Arial', 12)).pack()
Entry(LForm, font=("Arial", 10, "bold"), textvariable=Name).pack(side=TOP, padx=10,fill=X)

Label(LForm, text="Contact", font=('Arial', 12)).pack()
Entry(LForm, font=("Arial", 10, "bold"), textvariable=Contact).pack(side=TOP, padx=10,fill=X)

Label(LForm, text="Gmail", font=('Arial', 12)).pack()
Entry(LForm, font=("Arial", 10, "bold"), textvariable=Gmail).pack(side=TOP, padx=10,fill=X)

Label(LForm, text="Regno", font=('Arial', 12)).pack()
Entry(LForm, font=("Arial", 10, "bold"), textvariable=Regno).pack(side=TOP, padx=10, fill=X)

Label(LForm, text="Native", font=('Arial', 12)).pack()
Entry(LForm, font=("Arial", 10, "bold"), textvariable=Native).pack(side=TOP, padx=10,fill=X)

Button(LForm, text="Submit", font=("Arial", 12, "bold"), command=register).pack(side=TOP, padx=20, pady=10, fill=X)

lbl_txtsearch = Label(LeftViewForm, text="Enter Name To Search", font=('verdana', 12), bg="white")
lbl_txtsearch.pack()

search = Entry(LeftViewForm, textvariable=SEARCH, font=('verdana', 12), width=10)
search.pack(side=TOP, padx=10, fill=X)

btn_search = Button(LeftViewForm, text="Search", command=Searchrecord)
btn_search.pack(side=TOP, padx=10, pady=12, fill=X)

btn_view = Button(LeftViewForm, text="View All", command=DisplayData)
btn_view.pack(side=TOP, padx=10, pady=12, fill=X)

btn_reset = Button(LeftViewForm, text="Reset", command=Reset)
btn_reset.pack(side=TOP, padx=10, pady=12, fill=X)

btn_delete = Button(LeftViewForm, text="Delete", command=Delete)
btn_delete.pack(side=TOP, padx=10, pady=12, fill=X)

scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
tree = ttk.Treeview(MidViewForm, columns=("Student ID", "Name", "Contact", "Gmail", "Regno", "Native"),
                    selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)

tree.heading('Student ID', text="Student Id", anchor=W)
tree.heading('Name', text="Name", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)
tree.heading('Gmail', text="Gmail", anchor=W)
tree.heading('Regno', text="Regno", anchor=W)
tree.heading('Native', text="Native", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=100)
tree.column('#2', stretch=NO, minwidth=0, width=150)
tree.column('#3', stretch=NO, minwidth=0, width=80)
tree.column('#4', stretch=NO, minwidth=0, width=120)

tree.pack()
DisplayData()

display_screen.mainloop()
