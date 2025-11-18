from tkinter import *
from tkinter import messagebox
from functools import partial
import sqlite3
import hashlib
import xml.etree.ElementTree as ET

DB_NAME = "database.db"
XML_FILE_NAME = "week6_oct2025.xml"

# Create a window
window = Tk()
window.geometry("400x250")
window.title("Tkinter SQLite login form")


def read_XML():
    """ Read and print login details from XML file."""
    try:
        tree = ET.parse(XML_FILE_NAME)
    except FileNotFoundError:
        messagebox.showwarning("Warning",f"XML file '{XML_FILE_NAME}' not found.")
        print(f"XML file '{XML_FILE_NAME}' not found.")
        return

    root = tree.getroot()
    print("Root: ", root.tag)

    # Read data from XML file
    for elem in root.iter():
        print(elem.tag," : ",elem.text)

    messagebox.showinfo("XML Read", "XML content printet to console")


def write_XML():
    """ Write login details from the database to the XML file."""
    # 1. read data
    connection = sqlite3.connect("DB_NAME")
    cursor = connection.cursor()
    # Retrieve data from database using SQL query
    cursor.execute('SELECT * FROM login_details;')
    login_data = cursor.fetchall()
    connection.close()

    # 2. Write data
    data = ET.Element("user")
    for row in login_data:
        user = ET.SubElement(data,"login_details",username="",password="")
        user.set("username", row[0])
        user.set("password", row[1])
    tree = ET.ElementTree(data)
    tree.write(XML_FILE_NAME)
    messagebox.showinfo("XML Write", "XML content has been written to the file.")

write_XML()



# Loop to show window
window.mainloop()