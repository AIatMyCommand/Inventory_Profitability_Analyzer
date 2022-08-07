# import modules
from ast import arguments
from distutils.log import info
from tkinter import *
import os
import sqlite3
import ctypes
import io
from tkinter import messagebox

class CustomError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Error: %s" % self.value

# Designing root(first) window
def Main_Account_Screen():
    global Root_Screen
    Root_Screen = Tk()
    Root_Screen.geometry("300x250+800+0")
    Root_Screen.title("Account Login")
    Label(
        text="Select Your Choice",
        bg="gray71",
        width="300",
        height="2",
        font=("Calibri", 13),
    ).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command=Login).pack()
    Label(text="").pack()
    Button(text="Skip Login", height="2", width="30", command=Admin_Screen).pack()
    Label(text="").pack()
    # Button(text = "Register", height = "2", width = "30", command = register).pack()
    Button(text="Register", height="2", width="30").pack()
    Root_Screen.mainloop()

# Designing window for registration
# def register():
#    global register_screen
#    register_screen = Toplevel(Root_Screen)
#    register_screen.title("Register")
#    register_screen.geometry("300x250+Right+Top")

#    Label(register_screen, text = "Please enter details below", bg = "gray71").pack()
#    Label(register_screen, text = "").pack()
#    lbl_Username = Label(register_screen, text = "Username * ")
#    lbl_Username.pack()
#    txt_Username = Entry(register_screen, textvariable = username)
#    txt_Username.pack()
#    lbl_Password = Label(register_screen, text = "Password * ")
#    lbl_Password.pack()
#    txt_Password = Entry(register_screen, textvariable = password, show = '*')
#    txt_Password.pack()
#    Label(register_screen, text = "").pack()
#    Button(register_screen, text = "Register", width = 10, height = 1, bg = "grey", command = register_user).pack()

# Designing window for Login
def Login():
    global Login_screen, username, password, txt_Username, txt_Password
    username = StringVar()
    password = StringVar()
    Login_screen = Toplevel(Root_Screen)
    Login_screen.title("Login")
    Login_screen.geometry("300x250+800+0")
    Label(Login_screen, text="Please enter details below to Login").pack()
    Label(Login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global txt_Username_Login
    global txt_Password_Login

    Label(Login_screen, text="Username: ").pack()
    txt_Username_Login = Entry(Login_screen, textvariable=username_verify)
    txt_Username_Login.pack()
    Label(Login_screen, text="").pack()
    Label(Login_screen, text="Password: ").pack()
    txt_Password_Login = Entry(Login_screen, textvariable=password_verify, show="*")
    txt_Password_Login.pack()
    Label(Login_screen, text="").pack()
    Button(Login_screen, text="Login", width=10, height=1, command=Login_Verify).pack()


# Implementing event on register button
def register_user():

    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()
    # Label(register_screen, text = "Registration Success", fg = "green", font = ("calibri", 11)).pack()


# Implementing event on Login button
def Login_Verify():
    # This version uses a clear text file to store the username & password. The next version will encrypt the file
    username1 = username_verify.get()
    password1 = password_verify.get()
    txt_Username_Login.delete(0, END)
    txt_Password_Login.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            # Login_sucess()
            infobox("Login success")

        else:
            # password_not_recognised()
            errorbox("Your password is incorrect")

    else:
        # user_not_found()
        errorbox("User not found")
        # Note: user enumeration vulnerability


# Designing popup for Login success
def Login_sucess():
    Admin_Screen.destroy()
    global Login_Success_Screen
    Login_Success_Screen = Toplevel(Login_screen)
    Login_Success_Screen.title("Success")
    Login_Success_Screen.geometry("150x100+800+0")
    Label(Login_Success_Screen, text="Login Success").pack()
    Button(Login_Success_Screen, text="OK", command=delete_Login_Success).pack()


# Designing popup for Login invalid password
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(Login_screen)
    password_not_recog_screen.title("Error")
    password_not_recog_screen.geometry("150x100+0+800")
    Label(password_not_recog_screen, text="Your password is incorrect").pack()
    Button(
        password_not_recog_screen, text="OK", command=delete_Password_Not_Recognised
    ).pack()


# Designing popup for user not found
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(Login_screen)
    user_not_found_screen.title("Error")
    user_not_found_screen.geometry("150x100+800+0")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(
        user_not_found_screen, text="OK", command=delete_User_Not_Found_Screen
    ).pack()


# Deleting popups
def delete_Login_Success():
    Login_Success_Screen.destroy()
    Admin_Screen()

def delete_Password_Not_Recognised():
    password_not_recog_screen.destroy()

def delete_User_Not_Found_Screen():
    user_not_found_screen.destroy()

# Admin screen
def Admin_Screen():
    global Admin_Screen, Item, Price, Units_Sold, Cost_to_Make, Cost_to_Ship, Marginal_Cost, Beginning_INV, Ending_INV, AVG_Value_of_Item_Inventory
    global Turnover, Profitability, Physical_Volume, sqliteConnection, cursor
    Admin_Screen = Toplevel(Root_Screen)
    Admin_Screen.title("Admin")
    Admin_Screen.geometry("300x250+800+0")
    Label(Admin_Screen, text="You are the best wife ever.", bg="gray71").pack(
        side="top")
    Label(Admin_Screen, text="What Would You Like To Do Today?", bg="gray71").pack(
        side="top"
    )
    Label(Admin_Screen, text="").pack()
    # connect to the database
    try:
        print("starting try")
        # Connect to DB and create a cursor
        sqliteConnection = sqlite3.connect("Product_Line_Analyzer.db")
        cursor = sqliteConnection.cursor()

        # Write a query and execute it with cursor
        # query = "SELECT sqlite_version();"
        # query = "sqlite;"
        # version = cursor.execute(query)
        # infobox(version)
        query = "CREATE TABLE IF NOT EXISTS inventory(ID INT PRIMARY KEY NOT NULL, Item CHAR(25) NOT NULL, Price, Units_Sold INT NOT NULL, Marginal_Cost,  AVG_Value_of_Item_Inventory, Turnover, Profitability, Physical_Volume)"
        res = cursor.execute(query)
        print(res)

    # Handle errors
    except sqlite3.Error as error:
        print("An error occured - ", error)

    except Exception:
        print("starting raise")
        raise CustomError("Unknown Error")

    Button(
        Admin_Screen, text="Add Items", width=10, height=1, bg="grey", command=Add_Items
    ).pack()
    Label(text="").pack()
    Button(
        Admin_Screen,
        text="Browse Items",
        width=10,
        height=1,
        bg="grey",
        command=Browse_Items,
    ).pack()
    Label(text="").pack()
    Button(
        Admin_Screen,
        text="Search Items",
        width=10,
        height=1,
        bg="grey",
        command=search_items,
    ).pack()
    Label(text="").pack()
    Button(
        Admin_Screen, text="Backup", width=10, height=1, bg="grey", command=backup
    ).pack()
    Label(text="").pack()
    Button(
        Admin_Screen, text="Restore", width=10, height=1, bg="grey", command=restore
    ).pack()
    Label(text="").pack()
    Label(text="").pack()
    Button(
        Admin_Screen, text="Logout", width=10, height=1, bg="grey", command=logout
    ).pack()
    # print("breakpoint")

def infobox(msg):
    messagebox.showinfo("Info", msg)

def errorbox(msg):
    messagebox.showerror("Error", msg)

def yes_no_box(msg):
    choice = messagebox.askyesno("Please choose an option", msg)
    # TODO: what does this return?
    return choice

# Functions to set focus (cursor)
#def focus_Item(event):
#    # set focus on the Item box
#    Item.focus_set()
 
#def focus_Price(event):
#    # set focus on the Price box
#    Price.focus_set()
 
#def focus_Cost_to_Make(event):
#    # set focus on the Cost_to_Make box
#    Cost_to_Make.focus_set()
 
#def focus_Cost_to_Ship(event):
#    # set focus on the Cost_to_Ship box
#    Cost_to_Ship.focus_set()
 
#def focus_Units_Sold(event):
#    # set focus on the Units_Sold box
#    Units_Sold.focus_set()
 
#def focus_Beginning_INV(event):
#    # set focus on the Beginning_INV box
#    Beginning_INV.focus_set()

#def focus_Ending_INV(event):
#    # set focus on the Ending_INV box
#    Ending_INV.focus_set()

#def focus_Physical_Volume(event):
#    # set focus on the Physical_Volume box
#    Physical_Volume.focus_set()

# Implementing event on Add_Items button click
def Add_Items():
    Admin_Screen.destroy()
    global Add_Items_Screen#, Item, Price, Cost_to_Make, Cost_to_Ship, Units_Sold, Beginning_INV, Ending_INV
    Item = ""
    Units_Sold = ""
    Cost_to_Make = ""
    Cost_to_Ship = ""
    Beginning_INV = ""
    Ending_INV = ""
    Physical_Volume = ""
    Add_Items_Screen = Toplevel(Root_Screen)
    Add_Items_Screen.title("Add Items")
    Add_Items_Screen.geometry("400x300+800+0")
    Label(Add_Items_Screen, text="     ").grid(row=0, column=0)
    Label(Add_Items_Screen, text="     ").grid(row=1, column=0)
    Label(Add_Items_Screen, text="     ").grid(row=2, column=0)
    Label(Add_Items_Screen, text="     ").grid(row=3, column=0)
    Label(Add_Items_Screen, text="     ").grid(row=4, column=0)
    Label(Add_Items_Screen, text="     ").grid(row=5, column=0)
    Label(Add_Items_Screen, text="     ").grid(row=6, column=0)
    Label(Add_Items_Screen, text="     ").grid(row=7, column=0)
    Label(Add_Items_Screen, text="     ").grid(row=8, column=0)
    Label(Add_Items_Screen, text="").grid(row=0, column=1)
    Label(Add_Items_Screen, text="Item", anchor="w").grid(row=1, column=1)
    Label(Add_Items_Screen, text="Price", justify=LEFT).grid(row=2, column=1)
    Label(Add_Items_Screen, text="Cost to Make", justify=LEFT).grid(row=3, column=1)
    Label(Add_Items_Screen, text="Cost to Ship", justify=LEFT).grid(row=4, column=1)
    Label(Add_Items_Screen, text="Units Sold", justify=LEFT).grid(row=5, column=1)
    Label(Add_Items_Screen, text="Beginning INV", justify=LEFT).grid(row=6, column=1)
    Label(Add_Items_Screen, text="Ending INV", justify=LEFT).grid(row=7, column=1)
    Label(Add_Items_Screen, text="Physical Volume", justify=LEFT).grid(row=8, column=1)
    Label(Add_Items_Screen).grid(row=0, column=2)

    Item = Entry(Add_Items_Screen)
    #Item.bind("<Return>", focus_Item)
    Item.bind("<Return>")
    Item.grid(row=1, column=2)
    Price = Entry(Add_Items_Screen)
    #Price.bind("<Return>", focus_Price)
    Price.bind("<Return>")
    Price.grid(row=2, column=2)
    Cost_to_Make = Entry(Add_Items_Screen)
    #Cost_to_Make.bind("<Return>", focus_Cost_to_Make)
    Cost_to_Make.bind("<Return>")
    Cost_to_Make.grid(row=3, column=2)
    Cost_to_Ship = Entry(Add_Items_Screen)
    #Cost_to_Ship.bind("<Return>", focus_Cost_to_Ship)
    Cost_to_Ship.bind("<Return>")
    Cost_to_Ship.grid(row=4, column=2)
    Units_Sold = Entry(Add_Items_Screen)
    #Units_Sold.bind("<Return>", focus_Units_Sold)
    Units_Sold.bind("<Return>")
    Units_Sold.grid(row=5, column=2)
    Beginning_INV = Entry(Add_Items_Screen)
    #Beginning_INV.bind("<Return>", focus_Beginning_INV)
    Beginning_INV.bind("<Return>")
    Beginning_INV.grid(row=6, column=2)
    Ending_INV = Entry(Add_Items_Screen)
    #Ending_INV.bind("<Return>", focus_Ending_INV)
    Ending_INV.bind("<Return>")
    Ending_INV.grid(row=7, column=2)
    Physical_Volume = Entry(Add_Items_Screen)
    #Physical_Volume.bind("<Return>", focus_Physical_Volume)
    Physical_Volume.bind("<Return>")
    Physical_Volume.grid(row=8, column=2)
    btnSubmit = Button(Add_Items_Screen, text="Submit", height="2", width="30", command=submit)
    btnSubmit.grid(row=10, column=2)
    btnBack = Button(Add_Items_Screen, text="Back", height="2", width="30", command=back)
    btnBack.grid(row=11, column=2)

    # implementing event on submit button click
    def submit():
        if(Item == "" or
           Units_Sold == "" or
           Cost_to_Make == "" or
           Cost_to_Ship == "" or
           Beginning_INV == "" or
           Ending_INV == "" or
           Physical_Volume == ""):
            errorbox("no textboxes may have an empty input")
        # try to convert to approriate types just to verify the data types
        try:
            Units_Sold = IntVar(Units_Sold)
            Cost_to_Make = float(Cost_to_Make.get())
            Cost_to_Ship = float(Ending_INV.get())
            Beginning_INV = float(Beginning_INV.get())
            Ending_INV = float(Ending_INV.get())
            Physical_Volume = float(Physical_Volume.get())
            AVG_Value_of_Item_Inventory = (Beginning_INV + Ending_INV) / 2
            Marginal_Cost = Cost_to_Make + Cost_to_Ship
            try:
                query = ("ADD TABLE Product_Lines " + Item + str(Price) + str(Marginal_Cost)
                    + str(Units_Sold) + str(AVG_Value_of_Item_Inventory)
                    + str(Marginal_Cost / AVG_Value_of_Item_Inventory)
                    + str((Price + Marginal_Cost) / Marginal_Cost) + str(Physical_Volume))
                cursor.execute(query)
                sqliteConnection.commit()
                # clearing the contents of text entry boxes
                Item.delete(0, END)
                Price.delete(0, END)
                Cost_to_Make.delete(0, END)
                Cost_to_Ship.delete(0, END)
                Units_Sold.delete(0, END)
                Beginning_INV.delete(0, END)
                Ending_INV.delete(0, END)
            # Handle errors
            except sqlite3.Error as error:
                print("An error occured - ", error)

            except Exception:
                raise CustomError("Unknown Error")    
        # Handle errors
        except ValueError as error:
            errorbox("An invalid type was entered - ", error)
            print("Item must be text, units sold must be a whole number and all other fields must be numbers")
        except Exception as e:
            errorbox(e)
            raise CustomError("Unknown Error")
        
    # Implementing event on back button
    def back():
        Item.delete(0, END)
        Price.delete(0, END)
        Cost_to_Make.delete(0, END)
        Cost_to_Ship.delete(0, END)
        Units_Sold.delete(0, END)
        Beginning_INV.delete(0, END)
        Ending_INV.delete(0, END)    
        Add_Items_Screen.destroy
        Admin_Screen

# Implementing event on Browse_Items button
def Browse_Items():
    Admin_Screen.destroy()
    global Browse_Items_Screen
    # Fetch and output result
    # result = cursor.fetchall()
    result = sqliteConnection.execute("SELECT * FROM Product_Lines")
    i = 0  # row value inside the loop
    for Product_Lines in result:
        for j in range(len(Product_Lines)):
            Table = Entry(Browse_Items_Screen, width=10, fg="black")
            Table.grid(row=i, column=j)
            Table.insert(END, Product_Lines[j])
        i =+ 1
    


# Implementing event on search_items button
def search_items():
    cursor.close()


# Implementing event on backup button
def backup():
    Admin_Screen.destroy()
    # Open() function
    # TODO: check folder exists
    target = r'C:\data\sqlite\target.db'
    dllpath = u'C:\Users\nicho\anaconda3\\sqlite3.dll'

    # Constants from the SQLite 3 API defining various return codes of state.
    SQLITE_OK = 0
    SQLITE_ERROR = 1
    SQLITE_BUSY = 5
    SQLITE_LOCKED = 6
    SQLITE_OPEN_READONLY = 1
    SQLITE_OPEN_READWRITE = 2
    SQLITE_OPEN_CREATE = 4

    # Tweakable variables
    pagestocopy = 20
    millisecondstosleep = 100

    # dllpath = ctypes.util.find_library('sqlite3') # I had trouble with this on Windows
    sqlitedll = ctypes.CDLL(dllpath)
    sqlitedll.sqlite3_backup_init.restype = ctypes.c_void_p

    # Setup some ctypes
    p_src_db = ctypes.c_void_p(None)
    p_dst_db = ctypes.c_void_p(None)
    null_ptr = ctypes.c_void_p(None)

    # Check to see if the first argument (source database) can be opened for reading.
    # ret = sqlitedll.sqlite3_open_v2(sqliteConnection, ctypes.byref(p_src_db), SQLITE_OPEN_READONLY, null_ptr)
    #assert ret == SQLITE_OK
    #assert p_src_db.value is not None

    # Check to see if the second argument (target database) can be opened for writing.
    ret = sqlitedll.sqlite3_open_v2(target, ctypes.byref(p_dst_db), SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE, null_ptr)
    assert ret == SQLITE_OK
    assert p_dst_db.value is not None

    # Start a backup.
    print 'Starting backup to SQLite database "%s" to SQLite database "%s" ...' % (sqliteConnection, target)
    p_backup = sqlitedll.sqlite3_backup_init(p_dst_db, 'main', sqliteConnection, 'main')
    print '    Backup handler: {0:#08x}'.format(p_backup)
    assert p_backup is not None

    # Step through a backup.
    while True:
        ret = sqlitedll.sqlite3_backup_step(p_backup, pagestocopy)
        remaining = sqlitedll.sqlite3_backup_remaining(p_backup)
        pagecount = sqlitedll.sqlite3_backup_pagecount(p_backup)
        print '    Backup in progress: {0:.2f}%'.format((pagecount - remaining) / float(pagecount) * 100)
        if remaining == 0:
            break
        if ret in (SQLITE_OK, SQLITE_BUSY, SQLITE_LOCKED):
            sqlitedll.sqlite3_sleep(millisecondstosleep)

    # Finish the bakcup
    sqlitedll.sqlite3_backup_finish(p_backup)

    # Close database connections
    sqlitedll.sqlite3_close(p_dst_db)
    sqlitedll.sqlite3_close(p_src_db)
    #    Ans = yes_no_box("This will replace the current database. Are you sure you want to replace the current database?")
    #    if(Ans == "yes"):
    #        # iterdump() function
    #        for line in sqliteConnection.iterdump():
    #            p.write("%s\n" % line)
    #    else:
    #        pass
    #print("Backup performed successfully!")
    #print("Data Saved as backupdatabase_dump.sql")


# Implementing event on restore button
def restore():
    # TODO: check folder + file exist
    query = "ATTACH Inv_Analyzer 'bak\\backupdatabase_dump.sql' AS Inv;"
    cursor.execute(query)


# Implementing event on logout button
def logout():
    cursor.close()
    sqliteConnection.close()
    print("SQLite Connection closed")
    Main_Account_Screen()


# Start here
if __name__ == "__main__":
    #   print("This file is being run directly")
    Main_Account_Screen()
else:
    print("This file is running from an imported file")