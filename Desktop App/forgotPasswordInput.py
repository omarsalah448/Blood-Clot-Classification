import tkinter 
import customtkinter 
from tkinter import messagebox
import sqlite3
import re
import subprocess







#--------------------- Functions ---------------------#


# Function to insert placeholder text
def insert_placeholder(entry_widget, placeholder_text, placeholder_color="grey"):
    if entry_widget.get() == "":
        entry_widget.insert(0, placeholder_text)
        entry_widget.configure(text_color=placeholder_color)
        
# Function to remove placeholder text
def remove_placeholder(entry_widget, placeholder_text, default_color="black"):
    if entry_widget.get() == placeholder_text:
        entry_widget.delete(0, "end")
        entry_widget.configure(text_color=default_color)
        
def continue_check():
    email_entered = email_entry.get()
    email = email_entered.lower()

    if email == "":
        messagebox.showerror("Error", "Field Is Required")
    else:
        try:
            # Connect to the database
            conn = sqlite3.connect("app_database.db", timeout=20)
            cursor = conn.cursor()

            # Execute an SQL SELECT query to check if the entered email exists
            cursor.execute("SELECT * FROM user WHERE Email = ?", (email,))
            result = cursor.fetchone()

            # Close the database connection
            conn.close()

            # If result is not None, email exists in the database
            if result:
                print("Email exists in the database")
                subprocess.Popen(["python", "updatePassword.py", email])
                frame.destroy()
            elif not is_valid_email(email):
                messagebox.showerror("Error", "Write a valid email.")
            else:
                messagebox.showerror("Error", "Email does not exist in our database for registered doctors.")
                   
        except Exception as e:
            print("Error:",e)
            messagebox.showerror("Error","Something went wrong! Try again")
            
# Function to validate email
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Function to check email validity
def check_email(event=None):
    email = email_entry.get()
    if is_valid_email(email):
        continue_result.configure(text="Valid", text_color="green", height=8, font=('Century Gothic', 10))
        continue_result.place(x=283, y=158)
    else:
        continue_result.configure(text="Invalid email!", text_color="red", height=8, font=('Century Gothic', 9))
        continue_result.place(x=245, y=158)






#------------------ Frame and its content ------------------#

frame = customtkinter.CTk()  # Initialize customtkinter frame

# Get the screen width and height
screen_width = frame.winfo_screenwidth()
screen_height = frame.winfo_screenheight()

# Set the size of the dialog
dialog_width = 350
dialog_height = 250 
x_offset = 150  # Adjust to move the dialog box more to the right

x = (screen_width - dialog_width) // 2 + x_offset
y = (screen_height - dialog_height) // 2

# Set frame properties
frame.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
frame.resizable(width=False, height=False)
frame.title("Forgot Password")
frame.iconbitmap(r'icons/001_first_aid_box_Dnj_icon.ico')

# Add label
label = customtkinter.CTkLabel(frame, text="Forgot Your Password?", font=('Arial', 21))
label.pack(pady=20)

label2 = customtkinter.CTkLabel(frame, text="Enter your email and we will send you \ninstructions to reset your password.", font=('', 12))
label2.place(x=75, y=60)
    
# Add entry box
email_entry = customtkinter.CTkEntry(frame, height=37, width=290)
email_entry.place(x=31, y=120)
# Bind the check_email function to the Entry widget
email_entry.bind("<KeyRelease>", check_email)
# Bind events to insert and remove placeholder text
email_entry.bind("<FocusIn>", lambda event: remove_placeholder(email_entry, "Enter your email"))
email_entry.bind("<FocusOut>", lambda event: insert_placeholder(email_entry, "Enter your email"))
insert_placeholder(email_entry, "Enter your email")  # Call insert_placeholder initially

# Add "Submit" button
continue_button = customtkinter.CTkButton(frame, text="Continue", font=('Arial', 14, 'bold'), height=37, width=290, command=continue_check)
continue_button.place(x=31, y=175)

# Create sign-in result label
continue_result = customtkinter.CTkLabel(master=frame, text="")

frame.mainloop()