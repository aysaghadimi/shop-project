import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import json

# -------------- functions --------------------

def loadUserGrade(username):
    with open("settings.json") as file:
        data = json.load(file)
        if username in data:
            return int(data[username])
        return 0

def isEmpty(username, password):
    return username == '' or password == ''

def checkUser(username, password=None):
    query = f'''SELECT * FROM users WHERE username="{username}" '''
    if password:
        query += f'''AND password="{password}" '''
    result = conn.execute(query)
    rows = result.fetchall()
    return len(rows) > 0

def handleLogin():
    global currentUser
    username = txtUsername.get()
    password = txtPassword.get()

    if isEmpty(username, password):
        lblMessage.config(text='empty fields error!', fg='red')
        return

    if checkUser(username, password):
        lblMessage.config(text='Welcome!', fg='green')
        currentUser = username
        txtUsername.delete(0, 'end')
        txtPassword.delete(0, 'end')
        txtUsername.config(state='disabled')
        txtPassword.config(state='disabled')
        btnLogin.config(state='disabled')
        btnDeleteAccount.config(state='normal')
        btnOpenShop.config(state='normal')
        btnOpenCart.config(state='normal')
    else:
        lblMessage.config(text='Invalid credentials', fg='red')

def handleSignup():
    def validateSignup(username, password, confirmPassword):
        if username == '' or password == '' or confirmPassword == '':
            return False, 'Empty fields error!'
        if password != confirmPassword:
            return False, 'Password and confirmation mismatch!'
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password):
            return False, 'Password must have at least 8 chars, one letter, and one number'
        if checkUser(username):
            return False, 'Username already exists!'
        return True, ''

    def addUserToDatabase(username, password):
        try:
            query = f'INSERT INTO users (username, password, grade) VALUES ("{username}", "{password}", 0)'
            conn.execute(query)
            conn.commit()
            return True
        except:
            return False

    def submitSignup():
        username = entryUsername.get()
        password = entryPassword.get()
        confirmPassword = entryConfirmPassword.get()
        valid, message = validateSignup(username, password, confirmPassword)
        if not valid:
            lblSignupMessage.config(text=message, fg='red')
            return
        if addUserToDatabase(username, password):
            lblSignupMessage.config(text='Account created!', fg='green')
            entryUsername.delete(0, 'end')
            entryPassword.delete(0, 'end')
            entryConfirmPassword.delete(0, 'end')
        else:
            lblSignupMessage.config(text='Database error!', fg='red')

    signupWindow = tk.Toplevel(mainWindow)
    signupWindow.title('Signup')
    signupWindow.geometry('300x300')
    lblUsername = tk.Label(signupWindow, text='Username:')
    lblUsername.pack()
    entryUsername = tk.Entry(signupWindow)
    entryUsername.pack()
    lblPassword = tk.Label(signupWindow, text='Password:')
    lblPassword.pack()
    entryPassword = tk.Entry(signupWindow, show='*')
    entryPassword.pack()
    lblConfirmPassword = tk.Label(signupWindow, text='Confirm Password:')
    lblConfirmPassword.pack()
    entryConfirmPassword = tk.Entry(signupWindow, show='*')
    entryConfirmPassword.pack()
    lblSignupMessage = tk.Label(signupWindow, text='')
    lblSignupMessage.pack()
    btnSubmitSignup = tk.Button(signupWindow, text='Submit', command=submitSignup)
    btnSubmitSignup.pack()
    signupWindow.mainloop()

def deleteUserAccount():
    global currentUser
    if not messagebox.askyesno("Confirm", "Are you sure you want to delete your account?"):
        lblMessage.config(text='Operation cancelled.', fg='red')
        return
    if removeUserFromDatabase(currentUser):
        lblMessage.config(text='Account deleted.', fg='green')
        txtUsername.config(state='normal')
        txtPassword.config(state='normal')
        currentUser = ''
    else:
        lblMessage.config(text='Error deleting account.', fg='red')

def removeUserFromDatabase(username):
    try:
        query = f'DELETE FROM users WHERE username="{username}"'
        conn.execute(query)
        conn.commit()
        return True
    except:
        return False

def shopPanel():
    shopWindow = tk.Toplevel(mainWindow)
    shopWindow.title('Shop Panel')
    shopWindow.geometry('400x300')
    lblShop = tk.Label(shopWindow, text='Welcome to the Shop')
    lblShop.pack()
    
    shopWindow.mainloop()

def showCart():
    cartWindow = tk.Toplevel(mainWindow)
    cartWindow.title('My Cart')
    cartWindow.geometry('300x200')
    lblCart = tk.Label(cartWindow, text='Your cart is empty.')
    lblCart.pack()
    # Add more widgets and functionality for the cart here
    cartWindow.mainloop()

# ------------ Main window -----------------
conn = sqlite3.connect('shop.db')
currentUser = ''
mainWindow = tk.Tk()
mainWindow.title('Shop Application')
mainWindow.geometry('400x400')

lblUsername = tk.Label(mainWindow, text='Username:')
lblUsername.pack()
txtUsername = tk.Entry(mainWindow)
txtUsername.pack()
lblPassword = tk.Label(mainWindow, text='Password:')
lblPassword.pack()
txtPassword = tk.Entry(mainWindow, show='*')
txtPassword.pack()
lblMessage = tk.Label(mainWindow, text='')
lblMessage.pack()

btnLogin = tk.Button(mainWindow, text='Login', command=handleLogin)
btnLogin.pack()
btnSignup = tk.Button(mainWindow, text='Signup', command=handleSignup)
btnSignup.pack()
btnDeleteAccount = tk.Button(mainWindow, text='Delete Account', state='disabled', command=deleteUserAccount)
btnDeleteAccount.pack()
btnOpenShop = tk.Button(mainWindow, text='Shop', state='disabled', command=shopPanel)
btnOpenShop.pack()
btnOpenCart = tk.Button(mainWindow, text='My Cart', state='disabled', command=showCart)
btnOpenCart.pack()

mainWindow.mainloop()
