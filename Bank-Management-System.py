# Importing necessary modules
from ast import While
from codecs import charmap_build
from curses.ascii import isalpha, isdigit
import datetime as date
from distutils.log import error
from logging import exception, raiseExceptions
from sqlite3 import IntegrityError

# List of special characters
SpecialSym = ['$', '@', '#', '%']

# Importing MySQL Connector
import mysql.connector as sql

# Getting the current date and time
dates1 = date.datetime.now()

# Establishing a connection to the MySQL database
mycon = sql.connect(host="localhost", user="root", password="12345678", database="hubnet")
mycur = mycon.cursor()

# Main loop for user interaction
while True:
    print("\n")
    print("___________________________________________________________________________")
    print("*******************  Welcome To Colony Bank Of India  *******************")
    print("____________________________________________________________________________")
    print("Press 1 to for Sign Up ")
    print("Press 2 to for Sign In  ")

    try:
        ch = int(input("Enter Your Choice : "))
        if (isalpha(ch)) or (ch >= 3):
            raise Exception("Oops! That was not a valid number. Try again... :( ")

        elif ch == 1:
            # User sign up section
            while True:
                try:
                    # Checking for special characters in the name
                    ut = input("Enter Your Name Here : ")
                    if any(char in ut for char in SpecialSym):
                        raise TypeError
                    break
                except TypeError:
                    print("Special Character are not allowed like . , @ # < > ? / ; ")

            while True:
                try:
                    # Checking for special characters in the username
                    p = input("Enter Your User Name : ")
                    if any(char in p for char in SpecialSym):
                        raise TypeError
                    break
                except TypeError as m:
                    print("Special Character are not allowed like . ,@ # $ % * & = < > ? !")

            while True:
                try:
                    # Validating password complexity
                    z = input("Enter Your Password : ")
                    if len(z) < 6 or not any(char.isdigit() for char in z) \
                            or not any(char.isupper() for char in z) \
                            or not any(char.islower() for char in z) \
                            or not any(char in SpecialSym for char in z):
                        raise ValueError("Password should contain at least 1 upper case, "
                                         "1 Lower Case, 1 Special Character, and Password Must Contain at least 7 characters")
                    break
                except ValueError:
                    print("Password should contain at least 1 upper case, 1 Lower Case, "
                          "1 Special Character, and Password Must Contain at least 7 characters")

            k = int(input("Enter the Amount of money you want to deposit : "))

            while True:
                try:
                    # Validating date of birth format
                    a = input("Enter Your Date of Birth : ")
                    a = date.datetime.strptime(a, "%d/%m/%Y").date()
                    break
                except ValueError:
                    print("Please enter Date of birth in proper format !!! DD/MM/YYYY")

            s = input("Enter Your Address : ")

            while True:
                try:
                    # Validating phone number
                    d = input("Enter Your Phone Number : ")
                    if (len(d) != 10) or (d.isalpha()):
                        raise ValueError("Please enter a valid 10-digit Number")
                    break
                except ValueError as m:
                    print(m)

            while True:
                try:
                    # Validating Aadhar number
                    f = input("Enter Your 12 Digit Aadhar Number : ")
                    if (len(f) != 12) or (f.isalpha()):
                        raise ValueError("Please Enter a valid 12 digit Aadhar Number")
                    break
                except ValueError as m:
                    print(m)

            # Inserting user details into the database
            q = "insert into bank values('{}','{}','{}','{}','{}','{}','{}','{}')".format(ut, p, z, a, s, d, f, k)
            mycur.execute(q)
            mycon.commit()
            print("\n")
            print("_________________________________________________________________________")
            print("***********Account Has Been Created Successfully Kindly Login************")
            print("_________________________________________________________________________")
        break
    except Exception:
        print("\n")
        print("_________________________________________________")
        print("Oops! This  Username is not available  ")
        print("_________________________________________________")

# User sign in section
while True:
    if ch == 2:
        u = input("Enter Your Username : ")
        p = input("Enter Your Password : ")
        a = "select * from bank where UserName='{}' and Password='{}'".format(u, p)
        mycur.execute(a)
        data = mycur.fetchall()
        if data:
            while True:
                print("\n")
                print("___________________________________________________________________________")
                print("*************** Welcome To Colony Bank Of India : *************************")
                print("___________________________________________________________________________")
                print("\n")
                print("Press 1 To Withdraw Money")
                print("Press 2 To Deposit Money")
                print("Press 3 to view Last Five Transactions ")
                print("Press 4 To View Your Profile ")
                print("Press 5 To Update Account Details")
                print("Press 6 to Delete Your Account Permanently : ")
                print("Press 7 for Log Out")
                try:
                    ch1 = int(input("Enter Your Choice : "))
                    if ch1 >= 8:
                        raise TypeError("")
                except TypeError:
                    print("________________________________________________")
                    print("     OOPs !!! That Was an Invalid Input :(  ")
                    print("________________________________________________")
                if ch1 == 1:
                    # Withdrawal section
                    try:
                        np = "select Balance from bank where UserName='{}'".format(u)
                        mycur.execute(np)
                        bal = mycur.fetchone()[0]
                    except Exception:
                        print("oops")

                    print("\n")
                    print("________________________________ ")
                    print("Your Account Balance is : ", bal)
                    print("_________________________________")
                    print("\n")

                    while True:
                        try:
                            a1 = int(input("Enter the amount for withdrawal : "))
                        except ValueError:
                            print("_______________________________________________________________________ ")
                            print("   ***OOPs that was an invalid input***  :)  ")
                            print("_______________________________________________________________________ ")
                            print("\n")
                            continue

                        if a1 <= bal:
                            credited = 0

                            # Updating balance in the database
                            t6 = "update bank set Balance=GREATEST(0,Balance - '{}') where UserName='{}'".format(a1, u)
                            mycur.execute(t6)
                            mycon.commit()

                            # Disabling foreign key checks to avoid transaction table constraints
                            gfn = "SET FOREIGN_KEY_CHECKS=0"
                            mycur.execute(gfn)
                            mycon.commit()

                            # Inserting transaction details into the transaction table
                            bp = "insert into transaction values('{}','{}','{}','{}')".format(credited, a1, u, dates1)
                            mycur.execute(bp)
                            mycon.commit()

                            # Enabling foreign key checks
                            gf = "SET FOREIGN_KEY_CHECKS=1"
                            mycur.execute(gf)
                            mycon.commit()

                            np9 = "select Balance from bank where UserName='{}'".format(u)
                            mycur.execute(np9)
                            bal1 = mycur.fetchone()[0]

                            print("\n")
                            print("____________________________________________________________________")
                            print("Your UserName ", u, "is debited with Rs", a1, "on ", dates1)
                            print("towards Net Banking. Available balance is Rs: ", bal1, " ₹ only ")
                            print("________________________________________________________________________")
                        elif a1 > bal:
                            print("________________________________________________________________________")
                            print("   ********* OOPS Insufficient Balance Please Try Again !  **********")
                            print("________________________________________________________________________")
                        break

                elif ch1 == 2:
                    # Deposit section
                    Debited = 0

                    while True:
                        try:
                            a11 = input("Enter the amount to deposit : ")
                            if a11.isalpha():
                                raiseExceptions("")
                            else:
                                # Updating balance in the database
                                t6 = "update bank set Balance=Balance +'{}' where UserName='{}'".format(a11, u)
                                mycur.execute(t6)
                                mycon.commit()

                                # Inserting transaction details into the transaction table
                                mn = "insert into transaction values('{}','{}','{}','{}')".format(a11, Debited, u, dates1)
                                mycur.execute(mn)
                                mycon.commit()

                                np9 = "select Balance from bank where UserName='{}'".format(u)
                                mycur.execute(np9)
                                bal2 = mycur.fetchone()[0]

                                print("\n")
                                print("____________________________________________________________________")
                                print("Your UserName ", u, "is Credited with Rs", a11, "on ", dates1)
                                print("towards Net Banking. Available balance is Rs: ", bal2, " ₹ only")
                                print("________________________________________________________________________")
                                break
                        except TypeError:
                            print("oops")
                        except IntegrityError:
                            print("oopss")

                elif ch1 == 3:
                    # View last five transactions
                    prt = "Select Credited,Debited,Date from Transaction where UserName1='{}'".format(u)
                    mycur.execute(prt)
                    print("______________________________________________________________________________")
                    print("*************** The Transaction Details are as Follows*********************")
                    print("\n")
                    for i in mycur:
                        print("___________________________________________________________________________")
                        print("Credited , Debited  : ", i)
                        print("___________________________________________________________________________")

                elif ch1 == 4:
                    # View profile
                    nmm = "Select Name,UserName,Password,  Address,  Mobile_Number, Aadhar_no, Balance from bank where UserName='{}'".format(u)
                    mycur.execute(nmm)
                    print("______________________________________________________________________________")
                    print("*******************************ACCOUNT DETAILS *******************************")
                    print("______________________________________________________________________________")
                    print("\n")
                    print("_______________________________________________________________________________")
                    print("    Name      User Name  PassWord   Address     Mob No \t   Aadhar No    Balance")
                    print("_______________________________________________________________________________")
                    print("\n")
                    for i in mycur:
                        print("______________________________________________________________________________")
                        print(i)
                        print("______________________________________________________________________________")

                elif ch1 == 5:
                    # Update account details
                    while True:
                        print("\n")
                        print("_____________________________________________________")
                        print("    *******    Account Setting *********       ")
                        print("_____________________________________________________")

                        print("Press 1 To Update Your Name : ")
                        print("Press 2 To Update Your UserName : ")
                        print("Press 3 To Update Your PassWord : ")
                        print("Press 4 To Update Your Phone Number : ")
                        print("Press 5 To Update Address : ")

                        try:
                            ch2 = int(input("Enter Your Choice : "))
                            if ch2 >= 6:
                                raise ValueError("")
                        except ValueError:
                            print("___________________________________________________")
                            print("      ****OOP's That's Was an invalid input****    ")
                            print("___________________________________________________")
                            continue
                        break

                    if ch2 == 1:
                        # Update name
                        try:
                            name = input("Enter Your New Name : ")
                            ns = "update bank set name='{}' where UserName='{}'".format(name, u)
                            mycur.execute(ns)
                            mycon.commit()
                            print("_________________________________________________________________________")
                            print("   ****Hurray !!! Name is Updated Successfully***   :) ")
                            print("_________________________________________________________________________")
                        except IndexError:
                            print("Oh Something Went Wrong !!!")

                    elif ch2 == 2:
                        # Update username
                        try:
                            gf = "SET FOREIGN_KEY_CHECKS=0"
                            mycur.execute(gf)
                            mycon.commit()

                            mp = input("Enter Your New UserName : ")
                            nm = "update bank set UserName='{}' where password='{}'".format(mp, p)
                            mycur.execute(nm)
                            mycon.commit()
                            print("_________________________________________________________________________")
                            print("   ****Hurray !!! UserName is Updated Successfully***   :) ")
                            print("_________________________________________________________________________")

                            gf1 = "SET FOREIGN_KEY_CHECKS=1"
                            mycur.execute(gf1)
                            mycon.commit()

                        except Exception:
                            print("")

                    elif ch2 == 3:
                        # Update password
                        try:
                            newpassword = input("Enter Your New Password : ")
                            us = "update bank set Password='{}' where UserName='{}'".format(newpassword, u)
                            mycur.execute(us)
                            mycon.commit()
                            print("Hurray !!! Password is Updated Successfully")
                        except IndexError:
                            print("Oh Something Went Wrong")

                    elif ch2 == 4:
                        # Update phone number
                        while True:
                            try:
                                newphone = input("Enter Your New Phone Number : ")
                                if (len(newphone) != 10) or newphone.isalpha():
                                    raise ValueError("")
                                us = "update bank set Mobile_Number='{}' where  UserName='{}'".format(newphone, u)
                                mycur.execute(us)
                                mycon.commit()
                                print("_________________________________________________________________________")
                                print("   ****Hurray !!! Mobile Number is Updated Successfully***   :) ")
                                print("_________________________________________________________________________")

                            except ValueError:
                                print("________________________________________________________")
                                print("**** Please Enter a valid 10-digit Number ******")
                                print("________________________________________________________")
                                print("\n")
                                continue
                            break

                    elif ch2 == 5:
                        # Update address
                        try:
                            newadd = input("Enter Your New Address : ")
                            ns1 = "update bank set address='{}' where UserName='{}'".format(newadd, u)
                            mycur.execute(ns1)
                            mycon.commit()
                            print("_________________________________________________________________________")
                            print("   *** Hurray !!! Address is Updated Successfully ***  :) ")
                            print("_________________________________________________________________________")
                        except IndexError:
                            print("OOPS Something Went Wrong !!! ")

                elif ch1 == 6:
                    # Delete account
                    
                    ns = "SET FOREIGN_KEY_CHECKS=0"
                    mycur.execute(ns)
                    mycon.commit()

                    ps = "delete from bank where password='{}'".format(p)
                    mycur.execute(ps)
                    mycon.commit()

                    gs = "delete from transaction where UserName1='{}'".format(u)
                    mycur.execute(gs)
                    mycon.commit()

                    ns1 = "SET FOREIGN_KEY_CHECKS=1"
                    mycur.execute(ns1)
                    mycon.commit()

                    print("\n")
                    print("_________________________________________________________________________")
                    print("************* ACCOUNT HAS BEEN DELETED SUCCESSFULLY *******************")
                    print("_________________________________________________________________________")
                    print("\n")
                    exit()

                elif ch1 == 7:
                    # Log out
                    print("\n")
                    print("_____________________________________________________________________________")
                    print("************* Thanks For Choosing Colony Bank Of India *****************")
                    print("____________________________________________________________________________")
                    exit()

        else:
            print("\n")
            print("_______________________________________________")
            print("        Login Failed Please Try Again       :( ")
            print("_______________________________________________")
            print("\n")


