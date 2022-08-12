# import modules
from ast import Try, arguments
from distutils.log import info
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
import os
import sqlite3
#import io

class CustomError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Error: %s" % self.value

#implementing ItemVar object
class ItemVar:
    def __init__(self, description, price, cost_to_make, cost_to_ship, units_sold, beginning_INV, ending_INV, physical_volume):
        self.description = description
        self.price = float(price)
        self.units_sold = int(units_sold)
        self.cost_to_make = float(cost_to_make)
        self.cost_to_ship = float(cost_to_ship)
        self.beginning_INV = float(beginning_INV)
        self.ending_INV = float(ending_INV)
        self.physical_volume = float(physical_volume)

    def are_fields_filled(self, Description, price, units_sold, cost_to_make, cost_to_ship, beginning_INV, ending_INV, physical_volume):
        if(len(Description) > 0 and len(price) > 0 and len(units_sold) > 0 and 
           len(cost_to_make) > 0 and len(cost_to_ship) > 0 and
           len(beginning_INV) > 0 and len(ending_INV) > 0 or len(physical_volume) > 0):
            return True
        else:
            errorbox("No textboxes may have an empty input")

    def are_fields_correct_type(self, price, units_sold, cost_to_make, cost_to_ship, beginning_INV, ending_INV, physical_volume):
        # try to convert to approriate types just to verify the data types
        try:
            #test if conversion was successful
            assert type(price) is float, "Price should be a decimal"
            assert type(units_sold) is int, "Units_Sold should be a whole number"
            assert type(cost_to_make) is float, "Cost to Make should be a decimal"
            assert type(cost_to_ship) is float, "Cost to Ship should be a decimal"
            assert type(beginning_INV) is float, "Beginning Inventory should be a decimal"
            assert type(ending_INV) is float, "Ending Inventory should be a decimal"
            assert type(physical_volume) is float, "Physical Volume should be a decimal"
         # Handle errors
        except ValueError as error:
            errorstring = "An invalid type was entered - " + error
            errorbox(errorstring)
            print("Item must be text, units sold must be a whole number and all other fields must be numbers")
        except Exception as e:
            errorbox(e)
            errorstring = "Unknown Error" + e
            raise CustomError(errorstring)
            
# Designing root(first) window
def root():
    global Root_Screen
    Root_Screen = Tk()
    Root_Screen.geometry("400x300+800+0")
    Root_Screen.title("Account Login")
    Label(text = "Select Your Choice", bg = "gray71", width = "300", height = "2",
        font = ("Calibri", 13)).pack()
    Label(text = "").pack()
    Button(text = "Login", height = "2", width = "30", command = login).pack()
    Label(text = "").pack()
    Button(text = "Skip Login", height = "2", width = "30", command = admin).pack()
    #Button(text = "Skip Login", height = "2", width = "30", command = delete_login_success).pack()
    Label(text = "").pack()
    #The following line is there is case Alex wants to see register user work
    # Button(text = "Register", height = "2", width = "30", command = register).pack()
    Button(text = "Register", height = "2", width = "30").pack()
    Root_Screen.mainloop()

# Client only requires 1 user
# Designing window for registration
# def register():
#    global register_screen
#    register_screen = Toplevel(Root_Screen)
#    register_screen.title("Register")
#    register_screen.geometry("300x250+800+0")

#    Label(register_screen, text = "Please enter details below", bg = "gray71").pack()
#    Label(register_screen, text = "").pack()
#    lbl_Username = Label(register_screen, text = "Username * ")
#    lbl_Username.pack()
#    ent_Username = Entry(register_screen, textvariable = username)
#    ent_Username.pack()
#    lbl_Password = Label(register_screen, text = "Password * ")
#    lbl_Password.pack()
#    ent_Password = Entry(register_screen, textvariable = password, show = '*')
#    ent_Password.pack()
#    Label(register_screen, text = "").pack()
#    Button(register_screen, text = "Register", width = 10, height = 1, bg = "grey", command = register_user).pack()

# Designing window for Login
def login():
    global Login_Screen, Username, Password, ent_Username, ent_Password
    global Username_Verify, Password_Verify, ent_Username_Login, ent_Password_Login
    Username = StringVar()
    Password = StringVar()
    Login_Screen = Toplevel(Root_Screen)
    Login_Screen.title("Login")
    Login_Screen.geometry("300x250+800+0")
    Label(Login_Screen, text = "Please enter details below to Login").pack()
    Label(Login_Screen, text = "").pack()
    Username_Verify = StringVar()
    Password_Verify = StringVar()
    Label(Login_Screen, text = "Username: ").pack()
    ent_Username_Login = Entry(Login_Screen, textvariable = Username_Verify)
    ent_Username_Login.pack()
    Label(Login_Screen, text = "").pack()
    Label(Login_Screen, text = "Password: ").pack()
    ent_Password_Login = Entry(Login_Screen, textvariable = Password_Verify, show = "*")
    ent_Password_Login.pack()
    Label(Login_Screen, text = "").pack()
    Button(Login_Screen, text = "Login", width = 10, height = 1, command = login_verify).pack()
    
# Implementing event on register button
def register_user():
    Username_Info = Username.get()
    Password_Info = Password.get()
    file = open(Username_Info, "w")
    file.write(Username_Info + "\n")
    file.write(Password_Info)
    file.close()
    # Label(register_screen, text = "Registration Success", fg = "green", font = ("calibri", 11)).pack()

# Implementing event on Login button
def login_verify():
    # This version uses a clear text file to store the username & password. The next version will encrypt the file
    username1 = Username_Verify.get()
    password1 = Password_Verify.get()
    ent_Username_Login.delete(0, END)
    ent_Password_Login.delete(0, END)
    if(username1 == "" or password1 == ""):
        errorbox("Username or password field is empty")
    else:
        list_of_files = os.listdir()
        if username1 in list_of_files:
            file1 = open(username1, "r")
            verify = file1.read().splitlines()
            if password1 in verify:
                # Login_success()
                #infobox("Login success")
                login_success
            else:
                # password_not_recognised()
                errorbox("Your password is incorrect")
        else:
            # user_not_found()
            errorbox("User not found")

# Designing popup for Login success
def login_success():
    global Login_Success_Screen
    Login_Success_Screen = Toplevel(Login_Screen)
    Login_Success_Screen.title("Success")
    Login_Success_Screen.geometry("150x100+800+0")
    Label(Login_Success_Screen, text = "Login Success").pack()
    Button(Login_Success_Screen, text = "OK", command = delete_login_success).pack()
    admin

# Designing popup for Login invalid password
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(Login_Screen)
    password_not_recog_screen.title("Error")
    password_not_recog_screen.geometry("150x100+800+0")
    Label(password_not_recog_screen, text = "Your password is incorrect").pack()
    Button(password_not_recog_screen, text = "OK",
           command = delete_Password_Not_Recognised).pack()

# Designing popup for user not found
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(Login_Screen)
    user_not_found_screen.title("Error")
    user_not_found_screen.geometry("150x100+800+0")
    Label(user_not_found_screen, text = "User Not Found").pack()
    Button(user_not_found_screen, text = "OK", command = delete_User_Not_Found_Screen
           ).pack()
    
# Deleting popups
def delete_login_success():
    Login_Success_Screen.destroy()
    admin

def delete_Password_Not_Recognised():
    password_not_recog_screen.destroy()

def delete_User_Not_Found_Screen():
    user_not_found_screen.destroy()

# Admin screen
def admin():
    global Admin_Screen
    #global Admin_Screen, Description, Price, Units_Sold, Cost_to_Make, Cost_to_Ship, Marginal_Cost, Beginning_INV, Ending_INV, AVG_Value_of_Item_Inventory
    #global Turnover, Profitability, Physical_Volume
    Admin_Screen = Toplevel(Root_Screen)
    Admin_Screen.title("Admin")
    Admin_Screen.geometry("300x400+800+0")
    Label(Admin_Screen, text = "You are the best wife ever.", bg = "gray71").pack(
        side = "top")
    Label(Admin_Screen, text = "What Would You Like To Do Today?", bg = "gray71").pack(
        side = "top")
    Label(Admin_Screen, text = "").pack()
    Label(Admin_Screen, text = "    ").pack()
    Button(Admin_Screen, text = "Add Items", width = 10, height = 1, bg = "grey",
           command = add_items).pack()
    Button(Admin_Screen, text = "Browse Items", width = 10, height = 1, bg = "grey",
        command = browse_items).pack()
    Button(Admin_Screen, text = "Search Items", width = 10, height = 1, bg = "grey",
        command = search_items).pack()
    Button(Admin_Screen, text = "Backup", width = 10, height = 1, bg = "grey",
           command = backup).pack()
    Button(Admin_Screen, text = "Restore", width = 10, height = 1, bg = "grey",
           command = restore).pack()
    Label(Admin_Screen, text = "").pack()
    Label(Admin_Screen, text = "").pack()
    Button(Admin_Screen, text = "Logout", width = 10, height = 1, bg = "grey",
           command = logout).pack()
    # print("breakpoint")

def infobox(msg):
    messagebox.showinfo("Info", msg)

def errorbox(msg):
    messagebox.showerror("Error", msg)

def yes_no_box(msg):
    choice = messagebox.askyesno("Please choose an option", msg)
    # This returns a string of yes or no in lower case
    return choice

# Implementing event on Add_Items button
def add_items():
    Admin_Screen.destroy()
    global Add_Items_Screen, sqliteConnection, cursor
    Add_Items_Screen = Toplevel(Root_Screen)
    Add_Items_Screen.title("Add Items")
    Add_Items_Screen.geometry("400x300+800+0")

    # implementing event on submit button click
    def submit():
        Item1 = ItemVar(ent_Description.get(),  ent_Price.get(),  ent_Cost_to_Make.get(), ent_Cost_to_Ship.get(),
                        ent_Units_Sold.get(), ent_Beginning_INV.get(),  ent_Ending_INV.get(),
                        ent_Physical_Volume.get())
        if(Item1.are_fields_filled and Item1.are_fields_correct_type):
            # connect to the database
            try:
                print("starting try")
                # Connect to DB and create a cursor
                sqliteConnection = sqlite3.connect("Product_Line_Analyzer.db")
                cursor = sqliteConnection.cursor()
                query = '''CREATE TABLE IF NOT EXISTS Product_Lines(ItemID INT PRIMARY KEY NOT NULL, Description CHAR(25) NOT NULL, Price, Units_Sold INT NOT NULL, Turnover REAL NOT NULL, Profitability REAL NOT NULL, Physical Volume REAL NOT NULL)'''
                res = cursor.execute(query)
                print(res)
                Marginal_Cost = Item1.cost_to_make - Item1.cost_to_ship
                AVG_Value_of_Item_Inventory = (Item1.beginning_INV + Item1.ending_INV)/2
                Turnover = (Marginal_Cost/AVG_Value_of_Item_Inventory)
                Profitability = ((Item1.price + Marginal_Cost)/Marginal_Cost)
                args = (Item1.description, Item1.price, Marginal_Cost, Item1.units_sold, Turnover, Profitability,
                        Item1.physical_volume)
                cursor.execute('''INSERT INTO Product_Lines VALUES '{}', '{}', '{}', '{}', '{}', '{}', '{}';'''.format(args))
                sqliteConnection.commit()
                print("successfully added")
                cursor.close()
                sqliteConnection.close()
            # Handle errors
            except sqlite3.Error as error:
                print("An error occured - ", error)
            except Exception:
                print("starting raise")
                raise CustomError("Unknown Error")
            finally:
                ent_Description.delete(0, END)
                ent_Price.delete(0, END)
                ent_Cost_to_Make.delete(0, END)
                ent_Cost_to_Ship.delete(0, END)
                ent_Units_Sold.delete(0, END)
                ent_Beginning_INV.delete(0, END)
                ent_Ending_INV.delete(0, END)
                ent_Physical_Volume.delete(0, END)
                del Item1

    # Implementing event on back button
    def back():
        ent_Description.delete(0, END)
        ent_Price.delete(0, END)
        ent_Cost_to_Make.delete(0, END)
        ent_Cost_to_Ship.delete(0, END)
        ent_Units_Sold.delete(0, END)
        ent_Beginning_INV.delete(0, END)
        ent_Ending_INV.delete(0, END)
        ent_Physical_Volume.delete(0, END)
        Add_Items_Screen.destroy
        admin

    Label(Add_Items_Screen, text = "     ").grid(row = 0, column = 0)
    Label(Add_Items_Screen, text = "     ").grid(row = 1, column = 0)
    Label(Add_Items_Screen, text = "     ").grid(row = 2, column = 0)
    Label(Add_Items_Screen, text = "     ").grid(row = 3, column = 0)
    Label(Add_Items_Screen, text = "     ").grid(row = 4, column = 0)
    Label(Add_Items_Screen, text = "     ").grid(row = 5, column = 0)
    Label(Add_Items_Screen, text = "     ").grid(row = 6, column = 0)
    Label(Add_Items_Screen, text = "     ").grid(row = 7, column = 0)
    Label(Add_Items_Screen, text = "     ").grid(row = 8, column = 0)
    Label(Add_Items_Screen, text = "").grid(row = 0, column = 1)
    Label(Add_Items_Screen, text = "Item", anchor = "w").grid(row = 1, column = 1)
    Label(Add_Items_Screen, text = "Price", justify = LEFT).grid(row = 2, column = 1)
    Label(Add_Items_Screen, text = "Cost to Make", justify = LEFT).grid(row = 3, column = 1)
    Label(Add_Items_Screen, text = "Cost to Ship", justify = LEFT).grid(row = 4, column = 1)
    Label(Add_Items_Screen, text = "Units Sold", justify = LEFT).grid(row = 5, column = 1)
    Label(Add_Items_Screen, text = "Beginning INV", justify = LEFT).grid(row = 6, column = 1)
    Label(Add_Items_Screen, text = "Ending INV", justify = LEFT).grid(row = 7, column = 1)
    Label(Add_Items_Screen, text = "Physical Volume", justify = LEFT).grid(row = 8, column = 1)
    Label(Add_Items_Screen).grid(row = 0, column = 2)

    ent_Description = Entry(Add_Items_Screen)
    ent_Description.bind()
    ent_Description.grid(row = 1, column = 2)

    ent_Price = Entry(Add_Items_Screen)
    ent_Price.bind()
    ent_Price.grid(row = 2, column = 2)

    ent_Cost_to_Make = Entry(Add_Items_Screen)
    ent_Cost_to_Make.bind()
    ent_Cost_to_Make.grid(row = 3, column = 2)

    ent_Cost_to_Ship = Entry(Add_Items_Screen)
    ent_Cost_to_Ship.bind()
    ent_Cost_to_Ship.grid(row = 4, column = 2)

    ent_Units_Sold = Entry(Add_Items_Screen)
    ent_Units_Sold.bind()
    ent_Units_Sold.grid(row = 5, column = 2)

    ent_Beginning_INV = Entry(Add_Items_Screen)
    ent_Beginning_INV.bind()
    ent_Beginning_INV.grid(row = 6, column = 2)

    ent_Ending_INV = Entry(Add_Items_Screen)
    ent_Ending_INV.bind()
    ent_Ending_INV.grid(row = 7, column = 2)

    ent_Physical_Volume = Entry(Add_Items_Screen)
    ent_Physical_Volume.bind()
    ent_Physical_Volume.grid(row = 8, column = 2)

    btnSubmit = Button(Add_Items_Screen, text = "Submit", height = "2", width = "30",
                       command = submit)
    btnSubmit.grid(row = 10, column = 2)

    btnBack = Button(Add_Items_Screen, text = "Back", height = "2", width = "30",
                     command = back)
    btnBack.grid(row = 11, column = 2)

# Implementing event on Browse_Items button
def browse_items():
    global Browse_Items_Screen
    Admin_Screen.destroy()
    Browse_Items_Screen = Tk()
    Browse_Items_Screen.geometry("900x500+600+0")
    Browse_Items_Screen.title("Browse Items")
    cursor = sqliteConnection.cursor()
    
    def modify(i):
        Item1 = ItemVar(ent_Description.get(),  ent_Price.get(),  ent_Cost_to_Make.get(),
                        ent_Cost_to_Ship.get(), ent_Units_Sold.get(),  
                        ent_Beginning_INV.get(),  ent_Ending_INV.get(),
                        Physical_Volume.get)
        if(Item1.are_fields_filled and Item1.are_fields_correct_type):
            try:
                Marginal_Cost = Item1.Cost_to_Make - Item1.Cost_to_Ship
                AVG_Value_of_Item_Inventory = (Item1.Beginning_INV + Item1.Ending_INV)/2
                Turnover = (Marginal_Cost/AVG_Value_of_Item_Inventory)
                Profitability = ((Item1.Price + Marginal_Cost)/Marginal_Cost)
                sqliteConnection = sqlite3.connect("Product_Line_Analyzer.db")
                args = (ent_Description.get(), ent_Price.get(), Marginal_Cost, ent_Units_Sold.get(),
                        Turnover, Profitability, Physical_Volume.get(), i)
                Modify_Command = ("Update Product_Lines SET '{}', '{}', '{}', '{}', '{}', '{}', '{}'".format(args) +
                         " WHERE ItemID = '{}'".format(i)) #how to pass a variable in a tuple
                cursor.execute(Modify_Command)
                sqliteConnection.commit()
                cursor.close()
                sqliteConnection.close()
            # Handle errors
            except sqlite3.Error as error:
                print("An error occurred - ", error)
            except Exception:
                print("Unknown Error")
                raise CustomError("Unknown Error")    
            # clearing the contents of text entry boxes
            finally:
                ent_Description.delete(0, END)
                ent_Price.delete(0, END)
                ent_Cost_to_Make.delete(0, END)
                ent_Cost_to_Ship.delete(0, END)
                ent_Units_Sold.delete(0, END)
                ent_Beginning_INV.delete(0, END)
                ent_Ending_INV.delete(0, END)
                ent_Physical_Volume.delete(0, END)
                del Item1

    #Implementing Delete button click event
    def delete(i):
        Confirmation_Delete = yes_no_box("Are you sure that you want to delete this entry?")
        if(Confirmation_Delete == "yes"):
            Delete_Command = ("DELETE FROM Product_Lines WHERE ItemID = ?", i)
            cursor.execute(Delete_Command)
            sqliteConnection.commit()
    
    def back():
        ent_Description.delete(0, END)
        ent_Price.delete(0, END)
        ent_Cost_to_Make.delete(0, END)
        ent_Cost_to_Ship.delete(0, END)
        ent_Units_Sold.delete(0, END)
        ent_Beginning_INV.delete(0, END)
        ent_Ending_INV.delete(0, END)
        ent_Physical_Volume.delete(0, END)
        Add_Items_Screen.destroy
        admin
    # Fetch and output result
    # result = cursor.fetchall()

    #Left-margin
    Label(Browse_Items_Screen, text = "     ").grid(row = 0, column = 0)
    Label(Browse_Items_Screen, text = "     ").grid(row = 1, column = 0)
    Label(Browse_Items_Screen, text = "     ").grid(row = 2, column = 0)
    Label(Browse_Items_Screen, text = "     ").grid(row = 3, column = 0)
    Label(Browse_Items_Screen, text = "     ").grid(row = 4, column = 0)
    Label(Browse_Items_Screen, text = "     ").grid(row = 5, column = 0)
    Label(Browse_Items_Screen, text = "     ").grid(row = 6, column = 0)
    Label(Browse_Items_Screen, text = "     ").grid(row = 7, column = 0)
    Label(Browse_Items_Screen, text = "     ").grid(row = 8, column = 0)
    #Label(Browse_Items_Screen, text = "").pack
    #headers
    Label(Browse_Items_Screen, text = "     ").grid(row = 0, column = 1)
    Label(Browse_Items_Screen, text = "     ").grid(row = 1, column = 1)
    Label(Browse_Items_Screen, text = "     ").grid(row = 1, column = 2)
    Label(Browse_Items_Screen, text = "  Item  ", anchor = "w").grid(row = 1, column = 3)
    Label(Browse_Items_Screen, text = "  Price  ", justify = LEFT).grid(row = 1, column = 4)
    Label(Browse_Items_Screen, text = "  Cost to Make  ", justify = LEFT).grid(row = 1, column = 5)
    Label(Browse_Items_Screen, text = "  Cost to Ship  ", justify = LEFT).grid(row = 1, column = 6)
    Label(Browse_Items_Screen, text = "  Units Sold  ", justify = LEFT).grid(row = 1, column = 7)
    Label(Browse_Items_Screen, text = "  Beginning INV  ", justify = LEFT).grid(row = 1, column = 8)
    Label(Browse_Items_Screen, text = "  Ending INV  ", justify = LEFT).grid(row = 1, column = 9)
    Label(Browse_Items_Screen, text = "  Physical Volume  ", justify = LEFT).grid(row = 1, column = 10)
    #Label(Browse_Items_Screen).grid(row = 0, column = 2)

    #rows = cursor.fetchall() <--Do I need this?
    for i in range(10):
        btnModify = Button(Browse_Items_Screen, text = "Modify", height = "2", width = "8", command = modify(i))
        btnModify.grid(row = i + 2, column = 1)
        
        btnDelete = Button(Browse_Items_Screen, text = "Delete", height = "2", width = "8", command = delete(i))
        btnDelete.grid(row = i + 2, column = 2)

        ent_Description = Entry(Browse_Items_Screen, width = "6")
        ent_Description.bind()
        ent_Description.grid(row = i + 2, column = 3)
        get_Description = cursor.execute("SELECT Description FROM Product_Lines WHERE ItemID = ?", i)
        Description = cursor.execute(get_Description)
        ent_Description.insert(END, Description)

        ent_Price = Entry(Browse_Items_Screen, width = "6")
        ent_Price.bind()
        ent_Price.grid(row = i + 2, column = 3)
        get_Price = cursor.execute("SELECT Price FROM Product_Lines WHERE ItemID = ?", i)
        Price = cursor.execute(get_Price)
        ent_Price.insert(END, Price)

        ent_Cost_to_Make = Entry(Browse_Items_Screen, width = "6")
        ent_Cost_to_Make.bind()
        ent_Cost_to_Make.grid(row = i + 2, column = 4)
        get_Cost_to_Make = cursor.execute("SELECT Cost_to_Make FROM Product_Lines WHERE ItemID = ?", i)
        Cost_to_Make = cursor.execute(get_Cost_to_Make)
        ent_Cost_to_Make.insert(END, Cost_to_Make)

        ent_Cost_to_Ship = Entry(Browse_Items_Screen, width = "6")
        ent_Cost_to_Ship.bind()
        ent_Cost_to_Ship.grid(row = i + 2, column = 5)
        get_Cost_to_Ship = cursor.execute("SELECT Cost_to_Ship FROM Product_Lines WHERE ItemID = ?", i)
        Cost_to_Ship = cursor.execute(get_Cost_to_Ship)
        ent_Cost_to_Ship.insert(END, Cost_to_Ship)

        ent_Units_Sold = Entry(Browse_Items_Screen, width = "6")
        ent_Units_Sold.bind()
        ent_Units_Sold.grid(row = i + 2, column = 6)
        get_Units_Sold = cursor.execute("SELECT Units_Sold FROM Product_Lines WHERE ItemID = ?", i)
        Units_Sold = cursor.execute(get_Units_Sold)
        ent_Units_Sold.insert(END, Units_Sold)

        ent_Beginning_INV = Entry(Browse_Items_Screen, width = "6")
        ent_Beginning_INV.bind()
        ent_Beginning_INV.grid(row = i + 2, column = 7)
        get_Beginning_INV = cursor.execute("SELECT Beginning_INV FROM Product_Lines WHERE ItemID = ?", i)
        Beginning_INV = cursor.execute(get_Beginning_INV)
        ent_Beginning_INV.insert(END, Beginning_INV)

        ent_Ending_INV = Entry(Browse_Items_Screen, width = "6")
        ent_Ending_INV.bind()
        ent_Ending_INV.grid(row = i + 2, column = 8)
        get_Ending_INV = cursor.execute("SELECT Ending_INV FROM Product_Lines WHERE ItemID = ?", i)
        Beginning_INV = cursor.execute(get_Ending_INV)
        ent_Ending_INV.insert(END, Beginning_INV)

        ent_Physical_Volume = Entry(Browse_Items_Screen, width = "6")
        ent_Physical_Volume.bind()
        ent_Physical_Volume.grid(row = i + 2, column = 9)
        get_Physical_Volume = cursor.execute("SELECT Physical_Volume FROM Product_Lines WHERE ItemID = ?", i)
        Physical_Volume = cursor.execute(get_Physical_Volume)
        ent_Physical_Volume.insert(END, Physical_Volume)
    
        btnBack = Button(Browse_Items_Screen, text = "Back", height = "2", width = "30", command = back)
        btnBack.grid(row = 12, column = 2)
        btnBack.grid(row = 11, column = 2)

# Implementing event on search_items button
def search_items():
    global Search_Screen
    Search_Screen = Tk()
    Search_Screen.geometry("400x300+800+0")
    Search_Screen.title("Search")
    query = ("SELECT * FROM Product_Lines ORDER BY Profitability, Turnover LIMIT 3")
    result = cursor.execute(query)
    i = 0 # row value inside the loop 
    for item in result:
        if(i == 0):
            Label(Search_Screen, text = "     ").grid(row = 0, column = 0)
            Label(Search_Screen, text = "     ").grid(row = 1, column = 0)
            Label(Search_Screen, text = "     ").grid(row = 2, column = 0)
            Label(Search_Screen, text = "     ").grid(row = 3, column = 0)
            Label(Search_Screen, text = "     ").grid(row = 4, column = 0)
            Label(Search_Screen, text = "     ").grid(row = 5, column = 0)
            Label(Search_Screen, text = "     ").grid(row = 6, column = 0)
            Label(Search_Screen, text = "     ").grid(row = 7, column = 0)
            Label(Search_Screen, text = "     ").grid(row = 8, column = 0)
            Label(Search_Screen, text = "").grid(row = 0, column = 1)
            Label(Search_Screen, text = "Item", anchor = "w").grid(row = 1, column = 1)
            Label(Search_Screen, text = "Price", justify = LEFT).grid(row = 2, column = 1)
            Label(Search_Screen, text = "Cost to Make", justify = LEFT).grid(row = 3, column = 1)
            Label(Search_Screen, text = "Cost to Ship", justify = LEFT).grid(row = 4, column = 1)
            Label(Search_Screen, text = "Units Sold", justify = LEFT).grid(row = 5, column = 1)
            Label(Search_Screen, text = "Turnover", justify = LEFT).grid(row = 6, column = 1)
            Label(Search_Screen, text = "Profitability", justify = LEFT).grid(row = 7, column = 1)
            Label(Search_Screen, text = "Physical Volume", justify = LEFT).grid(row = 8, column = 1)
        for j in range(len(item)):
            e = Entry(Search_Screen, width=10, fg = 'black') 
            e.grid(row = i, column = j) 
            e.insert(END, item[j])
        i=i+1
    cursor.close()


# Implementing event on Report button
def report():
    global Report_Screen
    Report_Screen = Tk()
    Report_Screen.geometry("400x300+800+0")
    Report_Screen.title("Report")
    query = ("SELECT * FROM Product_Lines ORDER BY Profitability, Turnover, DESC")
    Summary = cursor.execute(query)
    i = 0 # row value inside the loop 
    for item in Summary:
        if(i == 0):
            Label(Report_Screen, text = "     ").grid(row = 0, column = 0)
            Label(Report_Screen, text = "     ").grid(row = 1, column = 0)
            Label(Report_Screen, text = "     ").grid(row = 2, column = 0)
            Label(Report_Screen, text = "     ").grid(row = 3, column = 0)
            Label(Report_Screen, text = "     ").grid(row = 4, column = 0)
            Label(Report_Screen, text = "     ").grid(row = 5, column = 0)
            Label(Report_Screen, text = "     ").grid(row = 6, column = 0)
            Label(Report_Screen, text = "     ").grid(row = 7, column = 0)
            Label(Report_Screen, text = "     ").grid(row = 8, column = 0)
            Label(Report_Screen, text = "").grid(row = 0, column = 1)
            Label(Report_Screen, text = "Item", anchor = "w").grid(row = 1, column = 1)
            Label(Report_Screen, text = "Price", justify = LEFT).grid(row = 2, column = 1)
            Label(Report_Screen, text = "Cost to Make", justify = LEFT).grid(row = 3, column = 1)
            Label(Report_Screen, text = "Cost to Ship", justify = LEFT).grid(row = 4, column = 1)
            Label(Report_Screen, text = "Units Sold", justify = LEFT).grid(row = 5, column = 1)
            Label(Report_Screen, text = "Turnover", justify = LEFT).grid(row = 6, column = 1)
            Label(Report_Screen, text = "Profitability", justify = LEFT).grid(row = 7, column = 1)
            Label(Report_Screen, text = "Physical Volume", justify = LEFT).grid(row = 8, column = 1)
        for j in range(len(item)):
            e = Entry(Report_Screen, width=10, fg = 'black') 
            e.grid(row = i, column = j) 
            e.insert(END, item[j])
        i=i+1

# Implementing event on backup button
def backup():
    Admin_Screen.destroy()
    backupCommand = ""
    filename = "Product_Line_Analyzer.db"
    infobox("Select a new file to use as a backup, otherwise an existing file will be overwritten")
    backupCommand = (filename + " .dump > " + filename + "bak")
    cursor.execute(backupCommand)

# Implementing event on restore button
def restore():
    # TODO: check folder + file exist
    #mv sample.db sample.db.old
    Ans_File_Loc = "no"
    Ans_Overwrite = "no"
    filename = "Product_Line_Analyzer.db.bak"
    restoreCommand = (filename + " .dump > " + filename + "bak")
    Ans_File_Loc = yes_no_box("Would you like to specify a file to use as to restore the database?")
    if(Ans_File_Loc == "yes"):
        filename = fd.askopenfilename()
    Ans_Overwrite = yes_no_box("This will overwrite the current database. Are you sure that you want to overite the database?")
    if(Ans_Overwrite == "yes"):
        restoreCommand = (filename + " .dump > " + filename + "bak")
        cursor.execute(restoreCommand)

# Implementing event on logout button
def logout():
    Admin_Screen.destroy()
    cursor.close()
    sqliteConnection.close()
    print("SQLite Connection closed")
    root()

# Start here
if __name__ == "__main__":
    #   print("This file is being run directly")
    root()
else:
    print("This file has been imported")