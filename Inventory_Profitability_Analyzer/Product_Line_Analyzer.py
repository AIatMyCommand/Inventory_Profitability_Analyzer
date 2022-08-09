# import modules
from ast import Try, arguments
from distutils.log import info
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
import os
import sqlite3
import io

class CustomError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Error: %s" % self.value

class ItemVar:
    def __init__(self, ItemD, price, units_sold, cost_to_make, cost_to_ship, beginning_INV, ending_INV, physical_volume):
        self.ItemD = ItemD
        self.price = price
        self.units_sold = units_sold
        self.cost_to_make = cost_to_make
        self.cost_to_ship = cost_to_ship
        self.beginning_INV = beginning_INV
        self.ending_INV = ending_INV
        self.physical_volume = physical_volume

    def Are_Fields_Filled(self, ItemD, price, units_sold, cost_to_make, cost_to_ship, beginning_INV, ending_INV, physical_volume):
        if(len(ItemD) > 0 and len(price) > 0 and 
           len(units_sold) > 0 and len(cost_to_make) > 0 and
           len(cost_to_ship) > 0 and len(beginning_INV) > 0 and
           len(ending_INV) > 0 or len(physical_volume) > 0):
            return True
        else:
            errorbox("No textboxes may have an empty input")

    def Are_Fields_Correct_Type(self, price, units_sold, cost_to_make, cost_to_ship, beginning_INV, ending_INV, physical_volume):
        # try to convert to approriate types just to verify the data types
        try:
            price = float(price)
            units_sold = int(units_sold)
            cost_to_make = float(cost_to_make)
            cost_to_ship = float(cost_to_ship)
            beginning_INV = float(beginning_INV)
            ending_INV = float(ending_INV)
            physical_volume = float(physical_volume)
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
        raise CustomError("Unknown Error")        
            
# Designing root(first) window
def Root():
    global Root_Screen
    Root_Screen = Tk()
    Root_Screen.geometry("400x300+800+0")
    Root_Screen.title("Account Login")
    Label(text = "Select Your Choice", bg = "gray71", width = "300", height = "2",
        font = ("Calibri", 13)).pack()
    Label(text = "").pack()
    Button(text = "Login", height = "2", width = "30", command = Login).pack()
    Label(text = "").pack()
    Button(text = "Skip Login", height = "2", width = "30", command =
           Admin).pack()
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
def Login():
    global Login_screen, Username, Password, ent_Username, ent_Password
    global Username_Verify, Password_Verify, ent_Username_Login, ent_Password_Login
    Username = StringVar()
    Password = StringVar()
    Login_screen = Toplevel(Root_Screen)
    Login_screen.title("Login")
    Login_screen.geometry("300x250+800+0")
    Label(Login_screen, text = "Please enter details below to Login").pack()
    Label(Login_screen, text = "").pack()
    Username_Verify = StringVar()
    Password_Verify = StringVar()
    Label(Login_screen, text = "Username: ").pack()
    ent_Username_Login = Entry(Login_screen, textvariable = Username_Verify)
    ent_Username_Login.pack()
    Label(Login_screen, text = "").pack()
    Label(Login_screen, text = "Password: ").pack()
    ent_Password_Login = Entry(Login_screen, textvariable = Password_Verify, show = "*")
    ent_Password_Login.pack()
    Label(Login_screen, text = "").pack()
    Button(Login_screen, text = "Login", width = 10, height = 1, command = Login_Verify).pack()
    
# Implementing event on register button
def Register_User():
    Username_Info = Username.get()
    Password_Info = Password.get()
    file = open(Username_Info, "w")
    file.write(Username_Info + "\n")
    file.write(Password_Info)
    file.close()
    # Label(register_screen, text = "Registration Success", fg = "green", font = ("calibri", 11)).pack()

# Implementing event on Login button
def Login_Verify():
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
    Label(Login_Success_Screen, text = "Login Success").pack()
    Button(Login_Success_Screen, text = "OK", command = delete_Login_Success).pack()

# Designing popup for Login invalid password
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(Login_screen)
    password_not_recog_screen.title("Error")
    password_not_recog_screen.geometry("150x100+0+800")
    Label(password_not_recog_screen, text = "Your password is incorrect").pack()
    Button(password_not_recog_screen, text = "OK",
           command = delete_Password_Not_Recognised).pack()

# Designing popup for user not found
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(Login_screen)
    user_not_found_screen.title("Error")
    user_not_found_screen.geometry("150x100+800+0")
    Label(user_not_found_screen, text = "User Not Found").pack()
    Button(user_not_found_screen, text = "OK",
           command = delete_User_Not_Found_Screen).pack()
    
# Deleting popups
def delete_Login_Success():
    Login_Success_Screen.destroy()
    Admin()

def delete_Password_Not_Recognised():
    password_not_recog_screen.destroy()

def delete_User_Not_Found_Screen():
    user_not_found_screen.destroy()

# Admin screen
def Admin():
    global Admin_Screen, ItemD, Price, Units_Sold, Cost_to_Make, Cost_to_Ship, Marginal_Cost, Beginning_INV, Ending_INV, AVG_Value_of_Item_Inventory
    global Turnover, Profitability, Physical_Volume, sqliteConnection, cursor
    Admin_Screen = Toplevel(Root_Screen)
    Admin_Screen.title("Admin")
    Admin_Screen.geometry("300x400+800+0")
    Label(Admin_Screen, text = "You are the best wife ever.", bg = "gray71").pack(
        side = "top")
    Label(Admin_Screen, text = "What Would You Like To Do Today?", bg = "gray71").pack(
        side = "top")
    Label(Admin_Screen, text = "").pack()
    # connect to the database
    try:
        print("starting try")
        # Connect to DB and create a cursor
        sqliteConnection = sqlite3.connect("Product_Line_Analyzer.db")
        cursor = sqliteConnection.cursor()
        query = "CREATE TABLE IF NOT EXISTS Product_Lines(ItemID INT PRIMARY KEY NOT NULL, ItemD CHAR(25) NOT NULL, Price, Units_Sold INT NOT NULL, Marginal Cost REAL NOT NULL, Turnover REAL NOT NULL, Profitability REAL NOT NULL, Physical Volume REAL NOT NULL)"
        res = cursor.execute(query)
        print(res)

    # Handle errors
    except sqlite3.Error as error:
        print("An error occured - ", error)

    except Exception:
        print("starting raise")
        raise CustomError("Unknown Error")
    Label(Admin_Screen, text = "    ").pack()
    Button(Admin_Screen, text = "Add Items", width = 10, height = 1, bg = "grey",
           command = add_Items).pack()
    Button(Admin_Screen, text = "Browse Items", width = 10, height = 1, bg = "grey",
        command = browse_Items).pack()
    Button(Admin_Screen, text = "Search Items", width = 10, height = 1, bg = "grey",
        command = search_items,).pack()
    Button(Admin_Screen, text = "Backup", width = 10, height = 1, bg = "grey",
           command = Backup).pack()
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

def Add_Items():
    Admin_Screen.destroy()
    global Add_Items_Screen
    Add_Items_Screen = Toplevel(Root_Screen)
    Add_Items_Screen.title("Add Items")
    Add_Items_Screen.geometry("400x300+800+0")

    # implementing event on submit button click
    def Submit():
        Item1 = ItemVar(ent_ItemD.get(),  ent_Price.get(),  ent_Cost_to_Make.get(),
                        ent_Cost_to_Ship.get(), ent_Units_Sold.get(),  
                        ent_Beginning_INV.get(),  ent_Ending_INV.get(),
                        ent_Ending_INV.get(), Physical_Volume.get)
        if(Item1.Are_Fields_Filled and Item1.Are_Fields_Correct_Type):
            #txt_Price = str(ent_Price.get())
            #ent_Cost_to_Make.get()
            #ent_Cost_to_Ship.get()
            #txt_Units_Sold = str(units_sold)
            #Marginal_Cost = (ent_Cost_to_Make.get() + cost_to_ship)
            #AVG_Value_of_Item_Inventory = (beginning_INV + ending_INV)/2
            #txt_Turnover = str(Marginal_Cost/AVG_Value_of_Item_Inventory)
            #txt_Profitability = str(price/Marginal_Cost)
            #txt_Physical_Volume = str(physical_volume)
            #query = "INSERT INTO Product_Lines VALUES ?", ItemD, txt_Price, txt_Marginal_Cost, txt_Units_Sold, txt_Turnover, txt_Profitability, txt_Physical_Volume
            try:
                #cursor.execute("INSERT INTO Product_Lines VALUES ?", ent_ItemD.get(),
                #               ent_Price.get(), txt_Marginal_Cost, txt_Units_Sold,
                #               txt_Turnover, txt_Profitability, txt_Physical_Volume)
                Marginal_Cost = float(ent_Cost_to_Make.get()) - float(ent_Cost_to_Ship.get())
                AVG_Value_of_Item_Inventory = (float(ent_Beginning_INV.get()) + float(ent_Ending_INV.get()))/2
                Turnover = (Marginal_Cost/AVG_Value_of_Item_Inventory)
                Profitability = ((ent_Price.get() + Marginal_Cost)/Marginal_Cost)
                cursor.execute("INSERT INTO Product_Lines VALUES ?", ent_ItemD.get(),
                               ent_Price.get(), Marginal_Cost, ent_Units_Sold.get(),
                               Turnover, Profitability, Physical_Volume.get())
                sqliteConnection.commit()
            # Handle errors
            except sqlite3.Error as error:
                print("An error occurred - ", error)
            except Exception:
                print("Unknown Error")
                raise CustomError("Unknown Error")    
            # clearing the contents of text entry boxes
            ent_ItemD.delete(0, END)
            ent_Price.delete(0, END)
            ent_Cost_to_Make.delete(0, END)
            ent_Cost_to_Ship.delete(0, END)
            ent_Units_Sold.delete(0, END)
            ent_Beginning_INV.delete(0, END)
            ent_Ending_INV.delete(0, END)
            del Item1

    # Implementing event on back button
    def Back():
        ent_ItemD.delete(0, END)
        ent_Price.delete(0, END)
        ent_Cost_to_Make.delete(0, END)
        ent_Cost_to_Ship.delete(0, END)
        ent_Units_Sold.delete(0, END)
        ent_Beginning_INV.delete(0, END)
        ent_Ending_INV.delete(0, END)
        Add_Items_Screen.destroy
        Admin

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

    ent_ItemD = Entry(Add_Items_Screen)
    ent_ItemD.bind()
    ent_ItemD.grid(row = 1, column = 2)

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

    btnSubmit = Button(Add_Items_Screen, text = "Submit", height = "2", width = "30", command = Submit)
    btnSubmit.grid(row = 10, column = 2)

    btnBack = Button(Add_Items_Screen, text = "Back", height = "2", width = "30", command = Back)
    btnBack.grid(row = 11, column = 2)

# Implementing event on Browse_Items button
def Browse_Items():
    global Browse_Items_Screen
    Admin_Screen.destroy()
    Browse_Items_Screen = Tk()
    Browse_Items_Screen.geometry("800x650+800+0")
    Browse_Items_Screen.title("Browse Items")
    
    def Modify0():
        
        Item1 = ItemVar(ent_ItemD.get(),  ent_Price.get(),  ent_Cost_to_Make.get(),
                        ent_Cost_to_Ship.get(), ent_Units_Sold.get(),  
                        ent_Beginning_INV.get(),  ent_Ending_INV.get(),
                        ent_Ending_INV.get(), Physical_Volume.get)
        if(Item1.Are_Fields_Filled and Item1.Are_Fields_Correct_Type):
            #txt_Price = str(ent_Price.get())
            #ent_Cost_to_Make.get()
            #ent_Cost_to_Ship.get()
            #txt_Units_Sold = str(units_sold)
            #Marginal_Cost = (ent_Cost_to_Make.get() + cost_to_ship)
            #AVG_Value_of_Item_Inventory = (beginning_INV + ending_INV)/2
            #txt_Turnover = str(Marginal_Cost/AVG_Value_of_Item_Inventory)
            #txt_Profitability = str(price/Marginal_Cost)
            #txt_Physical_Volume = str(physical_volume)
            #query = "INSERT INTO Product_Lines VALUES ?", ItemD, txt_Price, txt_Marginal_Cost, txt_Units_Sold, txt_Turnover, txt_Profitability, txt_Physical_Volume
            try:
                #cursor.execute("INSERT INTO Product_Lines VALUES ?", ent_ItemD.get(),
                #               ent_Price.get(), txt_Marginal_Cost, txt_Units_Sold,
                #               txt_Turnover, txt_Profitability, txt_Physical_Volume)
                Marginal_Cost = float(ent_Cost_to_Make.get()) - float(ent_Cost_to_Ship.get())
                AVG_Value_of_Item_Inventory = (float(ent_Beginning_INV.get()) + float(ent_Ending_INV.get()))/2
                Turnover = (Marginal_Cost/AVG_Value_of_Item_Inventory)
                Profitability = ((ent_Price.get() + Marginal_Cost)/Marginal_Cost)
                cursor.execute("INSERT INTO Product_Lines VALUES ?", ent_ItemD.get(),
                               ent_Price.get(), Marginal_Cost, ent_Units_Sold.get(),
                               Turnover, Profitability, Physical_Volume.get())
                sqliteConnection.commit()
            # Handle errors
            except sqlite3.Error as error:
                print("An error occurred - ", error)
            except Exception:
                print("Unknown Error")
                raise CustomError("Unknown Error")    
            # clearing the contents of text entry boxes
            ent_ItemD.delete(0, END)
            ent_Price.delete(0, END)
            ent_Cost_to_Make.delete(0, END)
            ent_Cost_to_Ship.delete(0, END)
            ent_Units_Sold.delete(0, END)
            ent_Beginning_INV.delete(0, END)
            ent_Ending_INV.delete(0, END)
            del Item1
        Modify_Command = "Update Product_Lines SET " + +" WHERE ItemID = 0"
        cursor.execute(Modify_Command)
    def Delete0():
        Confirmation_Delete = yes_no_box("Are you sure that you want to delete this entry?")
        if(Confirmation_Delete == "yes"):
            Delete_Command = "DELETE FROM Product_Lines WHERE ItemID = 0"
            cursor.execute(Delete_Command)
    # Fetch and output result
    # result = cursor.fetchall()
    item = sqliteConnection.execute("SELECT * FROM Product_Lines ORDER BY ItemID")
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
    Label(Browse_Items_Screen, text = "").grid(row = 0, column = 1)
    Label(Browse_Items_Screen, text = "Item", anchor = "w").grid(row = 1, column = 1)
    Label(Browse_Items_Screen, text = "Price", justify = LEFT).grid(row = 1, column = 2)
    Label(Browse_Items_Screen, text = "Cost to Make", justify = LEFT).grid(row = 1, column = 3)
    Label(Browse_Items_Screen, text = "Cost to Ship", justify = LEFT).grid(row = 1, column = 4)
    Label(Browse_Items_Screen, text = "Units Sold", justify = LEFT).grid(row = 1, column = 5)
    Label(Browse_Items_Screen, text = "Beginning INV", justify = LEFT).grid(row = 1, column = 6)
    Label(Browse_Items_Screen, text = "Ending INV", justify = LEFT).grid(row = 1, column = 7)
    Label(Browse_Items_Screen, text = "Physical Volume", justify = LEFT).grid(row = 1, column = 8)
    #Label(Browse_Items_Screen).grid(row = 0, column = 2)
    for i in 10:
        ent_ItemD = Entry(Browse_Items_Screen)
        ent_ItemD.bind()
        ent_ItemD.grid(row = i + 2, column = 1)

        ent_Price = Entry(Browse_Items_Screen)
        ent_Price.bind()
        ent_Price.grid(row = i + 2, column = 2)

        ent_Cost_to_Make = Entry(Browse_Items_Screen)
        ent_Cost_to_Make.bind()
        ent_Cost_to_Make.grid(row = i + 2, column = 3)

        ent_Cost_to_Ship = Entry(Browse_Items_Screen)
        ent_Cost_to_Ship.bind()
        ent_Cost_to_Ship.grid(row = i + 2, column = 4)

        ent_Units_Sold = Entry(Browse_Items_Screen)
        ent_Units_Sold.bind()
        ent_Units_Sold.grid(row = i + 2, column = 5)

        ent_Beginning_INV = Entry(Browse_Items_Screen)
        ent_Beginning_INV.bind()
        ent_Beginning_INV.grid(row = i + 2, column = 6)

        ent_Ending_INV = Entry(Browse_Items_Screen)
        ent_Ending_INV.bind()
        ent_Ending_INV.grid(row = i + 2, column = 7)

        ent_Physical_Volume = Entry(Browse_Items_Screen)
        ent_Physical_Volume.bind()
        ent_Physical_Volume.grid(row = i + 2, column = 8)
    
        btnBack = Button(Browse_Items_Screen, text = "Back", height = "2", width = "30", command = Back)
        btnBack.grid(row = 12, column = 2)
        btnBack.grid(row = 11, column = 2)

# Implementing event on search_items button
def search_items():
    cursor.close()
    
# Implementing event on backup button
def Backup():
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
    cursor.close()
    sqliteConnection.close()
    print("SQLite Connection closed")
    Root()

# Start here
if __name__ == "__main__":
    #   print("This file is being run directly")
    Root()
else:
    print("This file has been imported")