import sqlite3
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import hashlib
import os.path

# connect to database
db = sqlite3.connect('OnlineShopping.db')

# mouse position
cursor = db.cursor()

# generate encryption key (store this key)
key = Fernet.generate_key()

# Check if key_file exists, if not create one in later stage
key_file = 'encryption_Nov2025_key.key'

if os.path.exists(key_file):
    # Load that key
    with open(key_file,'rb') as file:
        key = file.read()
    # Create one
else:
    key = Fernet.generate_key()
    with open(key_file,'wb') as file:
        file.write(key)

# making cipher
cipher = Fernet(key)

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Encrypt data
def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()
# Decrypt data
def decrypt_data(encrypted_data):
    return cipher.decrypt(encrypted_data.encode()).decode()

# User registration function
def register_user():
    username = username_entry.get()
    password = password_entry.get()

    encrypted_loging = encrypt_data(username)
    hashed_password = hash_password(password)

    try:
        cursor.execute("SELECT * from login_details WHERE User_Login == ?",(username,))
        row = cursor.fetchone()
        if row:
            messagebox.showinfo("Error","Username exists.")
        else:
            cursor.execute("INSERT INTO login_details (User_Login,User_Password) VALUES (?,?)",(username,hashed_password))
            db.commit()
            messagebox.showinfo("Success", "User registration successful.")
    except sqlite3.InternalError:
        messagebox.showerror("Error","Username exist.")



def log_in():
    username = username_entry.get()
    password = password_entry.get()

    hashed_password = hash_password(password)

    cursor.execute("SELECT * FROM login_details WHERE User_Login = ? AND User_Password = ?",(username,hashed_password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Success.",f"Welcome {username}")
    else:
        messagebox.showinfo("Error","Invalid username or password")

window = tk.Tk()
window.title("Online shopping - secure login")
window.geometry("400x300")

tk.Label(window, text = "Username").pack()
username_entry = tk.Entry(window)
username_entry.pack()

tk.Label(window, text="Password").pack()
password_entry = tk.Entry(window,show="*")
password_entry.pack()

tk.Button(window, text = "Register", command = register_user).pack()
tk.Button(window, text = "Login", command=log_in).pack()

window.mainloop()