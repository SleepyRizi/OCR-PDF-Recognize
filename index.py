from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import json
import os
import tempfile
import subprocess

root = Tk()
root.title("Hospital Database")
width = 900
height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)




dictionary  = []

with open("dictionary.json", "r") as file:
    data = json.load(file)
    dictionary = data
    # print(dictionary)



# pdf_dictionary = dictionary[0]


def open_pdf(event):
    cur_item = tree.focus()
    item = tree.item(cur_item)
    pdf_name = item["values"][19]
    os.startfile(pdf_name)


#=====================================METHODS==============================================
def Database():
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT,
                            Place Text,
                            Date TEXT,
                            Blood_Bank_Receptionist TEXT,
                            Blood_Unit_No TEXT,
                            First_Name Text,
                            Fathers_Name Text,
                            Grandfather_Name Text,
                            Family_Name Text,
                            National_ID Text,
                            City Text,
                            Area Text,
                            Street Text,
                            Mobile Text,
                            Date_of_Birth text,
                            Age Text,
                            Occupation Text,
                            Nationality text,
                            Gender text,
                            pdf_name text)''')

    cursor.execute("SELECT * FROM `member`")



    if cursor.fetchone() is None:
        for record in dictionary:
            cursor.execute('''INSERT INTO `member` (
                            Place,
                            Date,
                            Blood_Bank_Receptionist ,
                            Blood_Unit_No ,
                            First_Name ,
                            Fathers_Name ,
                            Grandfather_Name ,
                            Family_Name ,
                            National_ID ,
                            City ,
                            Area ,
                            Street ,
                            Mobile ,
                            Date_of_Birth ,
                            Age ,
                            Occupation ,
                            Nationality ,
                            Gender,
                            pdf_name ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                                                         (
                                                            record['Place of Donation'],
                                                            record['Date'],
                                                            record['Blood Bank Receptionist'],
                                                            record['Blood Unit No.'],
                                                            record['First Name'],
                                                            record['Father Name'],
                                                            record['Grandfather Name'],
                                                            record['Family Name'],
                                                            record['National ID No.'],
                                                            record['City'],
                                                            record['Area'],
                                                            record['Street'],
                                                            record['Mobile No.'],
                                                            record['Date of Birth'],
                                                            record['Age'],
                                                            record['Occupation'],
                                                            record['Nationality'],
                                                            record['Gender'],
                                                            record['pdf_name']
                                                            ))
        conn.commit()
        
    # cursor.execute("SELECT * FROM `member` ORDER BY `Date` ASC")
    # fetch = cursor.fetchall()
    # for data in fetch:
    #     tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    
def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("db_member.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM `member`
                            WHERE `Place` LIKE ?
                               OR `Date` LIKE ?
                               OR `Blood_Bank_Receptionist` LIKE ?
                               OR `Blood_Unit_No` LIKE ?
                               OR `First_Name` LIKE ?
                               OR `Fathers_Name` LIKE ?
                               OR `Grandfather_Name` LIKE ?
                               OR `Family_Name` LIKE ?
                               OR `National_ID` LIKE ?
                               OR `City` LIKE ?
                               OR `Area` LIKE ?
                               OR `Street` LIKE ?
                               OR `Mobile` LIKE ?
                               OR `Date_of_Birth` LIKE ?
                               OR `Age` LIKE ?
                               OR `Occupation` LIKE ?
                               OR `Nationality` LIKE ?
                               OR `Gender` LIKE ?
                                                ''', ('%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',
                                                       '%'+str(SEARCH.get())+'%',

                                                       ))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def Reset():
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    tree.delete(*tree.get_children())
    cursor.execute("SELECT * FROM `member` ORDER BY `Place` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

#=====================================VARIABLES============================================
SEARCH = StringVar()

#=====================================FRAME================================================
Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
MidFrame = Frame(root, width=500)
MidFrame.pack(side=TOP)
LeftForm= Frame(MidFrame, width=100)
LeftForm.pack(side=LEFT)
RightForm= Frame(MidFrame, width=10)
RightForm.pack(side=RIGHT)


#=====================================LABEL WIDGET=========================================
lbl_title = Label(Top, width=500, font=('arial', 18), text="Hospital Database")
lbl_title.pack(side=TOP, fill=X)
lbl_search = Label(LeftForm, font=('arial', 15), text="Search here...")
lbl_search.pack(side=TOP)

#=====================================ENTRY WIDGET=========================================
search = Entry(LeftForm, textvariable=SEARCH)
search.pack(side=TOP, pady=1)

#=====================================BUTTON WIDGET========================================
btn_search = Button(LeftForm, text="Search", bg="#006dcc", command=Search)
btn_search.pack(side=LEFT)
btn_reset = Button(LeftForm, text="Reset", command=Reset)
btn_reset.pack(side=LEFT)
#=====================================Table WIDGET=========================================
scrollbarx = Scrollbar(RightForm, orient=HORIZONTAL)
scrollbary = Scrollbar(RightForm, orient=VERTICAL)
tree = ttk.Treeview(RightForm, columns=("MemberID",
                                         "Place",
                                          "Date",
                                          "Blood_Bank_Receptionist",
                                           "Blood_Unit_No",
                                           "First_Name",
                                           "Fathers_Name",
                                           "Grandfather_Name",
                                           "Family_Name",
                                           "National_ID",
                                           "City",
                                           "Area",
                                           "Street",
                                           "Mobile",
                                           "Date_of_Birth",
                                           "Age",
                                           "Occupation",
                                           "Nationality",
                                           "Gender",
                                           "pdf_name"

                                        ), selectmode="extended", height=400, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID",anchor=W)
tree.heading('Place', text="Place",anchor=W)
tree.heading('Date', text="Date",anchor=W)
tree.heading('Blood_Bank_Receptionist', text="Blood_Bank_Receptionist",anchor=W)
tree.heading('Blood_Unit_No', text="Blood_Unit_No",anchor=W)
tree.heading('First_Name', text="First_Name",anchor=W)
tree.heading('Fathers_Name', text="Fathers_Name",anchor=W)
tree.heading('Grandfather_Name', text="Grandfather_Name",anchor=W)
tree.heading('Family_Name', text="Family_Name",anchor=W)
tree.heading('National_ID', text="National_ID",anchor=W)
tree.heading('City', text="City",anchor=W)
tree.heading('Area', text="Area",anchor=W)
tree.heading('Street', text="Street",anchor=W)
tree.heading('Mobile', text="Mobile",anchor=W)
tree.heading('Date_of_Birth', text="Date_of_Birth",anchor=W)
tree.heading('Age', text="Age",anchor=W)
tree.heading('Occupation', text="Occupation",anchor=W)
tree.heading('Nationality', text="Nationality",anchor=W)
tree.heading('Gender', text="Gender",anchor=W)
tree.heading('pdf_name', text="pdf_name",anchor=W)


tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=170)
tree.column('#5', stretch=NO, minwidth=0, width=80)
tree.column('#6', stretch=NO, minwidth=0, width=80)
tree.column('#7', stretch=NO, minwidth=0, width=80)
tree.column('#8', stretch=NO, minwidth=0, width=80)
tree.column('#9', stretch=NO, minwidth=0, width=80)
tree.column('#10', stretch=NO, minwidth=0, width=80)
tree.column('#11', stretch=NO, minwidth=0, width=80)
tree.column('#12', stretch=NO, minwidth=0, width=80)
tree.column('#13', stretch=NO, minwidth=0, width=80)
tree.column('#14', stretch=NO, minwidth=0, width=80)
tree.column('#15', stretch=NO, minwidth=0, width=80)
tree.column('#16', stretch=NO, minwidth=0, width=80)
tree.column('#17', stretch=NO, minwidth=0, width=80)
tree.column('#18', stretch=NO, minwidth=0, width=80)

for record in dictionary:
    tree.bind("<Double-1>", open_pdf)


tree.pack()

#=====================================INITIALIZATION=======================================
if __name__ == '__main__':
    Database()
    root.mainloop()

