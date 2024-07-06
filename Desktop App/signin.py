import customtkinter
import tkinter as tk
from tkinter import messagebox, StringVar
from PIL import Image
import re
import sqlite3
import hashlib
import subprocess
from emailVerification import send_email, generate_random




# Initialize customtkinter app
signin = customtkinter.CTk()

# Get screen dimensions
screen_width = signin.winfo_screenwidth()
screen_height = signin.winfo_screenheight()

# Set app properties
signin.rowconfigure(0, weight=1)
signin.columnconfigure(0, weight=1)
height = 700
width = 1240
x = (signin.winfo_screenwidth() // 2) - (width // 2)
y = (signin.winfo_screenheight() // 4) - (height // 4)
signin.geometry('{}x{}+{}+{}'.format(width, height, x, y))
signin.resizable(width=True, height=True)
signin.title("Sign in")
signin.iconbitmap(r'icons/001_first_aid_box_Dnj_icon.ico')

# define variables
Email = StringVar()
Password = StringVar()

# Load image for background
image = Image.open("images/cover.jpg")

# Add image
img = customtkinter.CTkImage(light_image=image, dark_image=image, size=(screen_width, screen_height))

# Create background label
label1 = customtkinter.CTkLabel(master=signin, text="", image=img)
label1.pack(fill='both', expand=True)





#--------------------- Functions ---------------------#

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def clear():
    Email.set("")
    Password.set("")
    
def login():
    emailEntered = emailEntry.get()
    email = emailEntered.lower()
    password = passwordEntry.get()
    if email == "" or password == "":
        messagebox.showerror("Error", "All Fields Are Required")
    else:
        try:
            conn = sqlite3.connect("app_database.db", timeout=20)
            c = conn.cursor()
            c.execute("SELECT * FROM user WHERE Email=? and Password=?", [(email), hash_password(password)])
            result = c.fetchone()  # Fetch only one row since email should be unique
            if result:
                messagebox.showinfo("", "Check your email and write the sent 6-digit code")
                # Generate random number and send email
                random_number = generate_random(6)
                send_email(email, random_number)
                # Concatenate entry3 and random_number into a single string separated by a delimiter
                argument = email + ":" + random_number
                # Run subprocess with the concatenated argument
                pinResult = subprocess.run(["python", "emailVerificationInput.py", argument], capture_output=True, text=True)
                #Check if the input dialog returned success
                if pinResult.returncode == 0:
                    # save in database if and only if pin matched
                    pin_matched = pinResult.stdout.strip()
                    if pin_matched:
                        subprocess.Popen(["python", "homePage.py", email])
                        clear()
                        frame.destroy()
                        signin.destroy()
            elif not is_valid_email(email):
                messagebox.showerror("Error", "Write a valid email.")
            else:
                messagebox.showerror("Failed", "incorrect email or password!")
        except Exception as es:
            print("error", es)
            messagebox.showerror("Error", "Something went wrong! Try again")
      
def insert_placeholder(entry_widget, placeholder_text, placeholder_color="grey"):
    if entry_widget.get() == "":
        entry_widget.insert(0, placeholder_text)
        entry_widget.configure(text_color=placeholder_color)
        
# Function to remove placeholder text
def remove_placeholder(entry_widget, placeholder_text, default_color="black"):
    if entry_widget.get() == placeholder_text:
        entry_widget.delete(0, "end")
        entry_widget.configure(text_color=default_color)

# Function to insert placeholder text for password
def insert_placeholder_pass(entry_widget, placeholder_text, placeholder_color="grey"):
    if entry_widget.get() == "":
        entry_widget.configure(show="")
        entry_widget.insert(0, placeholder_text)
        entry_widget.configure(text_color=placeholder_color)

# Function to remove placeholder text for password
def remove_placeholder_pass(entry_widget, placeholder_text, default_color="black"):
    if entry_widget.get() == placeholder_text:
        entry_widget.delete(0, "end")
        entry_widget.configure(text_color=default_color)
        entry_widget.configure(show="*")
        
# Function to validate email
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Function to check email validity
def check_email(event=None):
    email = emailEntry.get()
    if is_valid_email(email):
        signin_result.configure(text="Valid", text_color="green", height=8, font=('Century Gothic', 10))
        signin_result.place(x=360, y=186)
    else:
        signin_result.configure(text="Invalid email!", text_color="red", height=8, font=('Century Gothic', 9))
        signin_result.place(x=330, y=186)

# Function to handle hover enter event
def on_hover_enter(event):
    label6.configure(text_color="blue")

# Function to handle hover leave event
def on_hover_leave(event):
    label6.configure(text_color="black")

# Function to handle forget password action
def forget_password():
    forgot_password_confirm = messagebox.askyesno("Forgot Password", "Are you sure you want to proceed?")
    if forgot_password_confirm:
        subprocess.run(["python", "forgotPasswordInput.py"])

# Function to toggle password visibility
def show_password():
    if passwordEntry.cget('show') == '*':
        passwordEntry.configure(show='')
    else:
        passwordEntry.configure(show='*')

# Function to display pop-up message on hover
def on_hover_entry(e):
    pop_up.configure(text="This is pop up message", text_color="red", height=34, font=('Century Gothic', 16), fg_color="white")
    pop_up.place(x=200, y=180)

# Function to hide pop-up message on leave
def leave_hover_entry(e):
    pop_up.configure(text="", fg_color="#C8E2E2")

def callback(file_path):
    subprocess.Popen(["python", file_path])
    frame.destroy()
    signin.destroy()





#------------------ Frames and their content ------------------#

# Create main frame #b9eae5
frame = customtkinter.CTkFrame(master=signin, width=500, height=510, fg_color="#C8E2E2")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
frame.update_idletasks() 
frame.configure(corner_radius=25)

# Create inside frame
inside_frame = customtkinter.CTkFrame(master=frame, fg_color="#C8E2E2")
inside_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=1, anchor=tk.CENTER)

# Create sign-in label
label3 = customtkinter.CTkLabel(master=inside_frame, text="Sign into your Account", font=('Century Gothic', 27), text_color="black")
label3.place(x=74, y=75)

# Create pop-up label
pop_up = customtkinter.CTkLabel(inside_frame, text='')

# Create email entry
emailEntry = customtkinter.CTkEntry(master=inside_frame, width=340, height=43, textvariable=Email)
emailEntry.place(x=55, y=145)

# Bind the check_email function to the Entry widget
emailEntry.bind("<KeyRelease>", check_email)
# Bind events to insert and remove placeholder text
emailEntry.bind("<FocusIn>", lambda event: remove_placeholder(emailEntry, "Enter Your Email"))
emailEntry.bind("<FocusOut>", lambda event: insert_placeholder(emailEntry, "Enter Your Email"))
insert_placeholder(emailEntry, "Enter Your Email")  # Call insert_placeholder initially

# Create password entry
passwordEntry = customtkinter.CTkEntry(master=inside_frame, width=340, show='*', height=43, textvariable=Password)
passwordEntry.place(x=55, y=206)
# Bind events to insert and remove placeholder text
passwordEntry.bind("<FocusIn>", lambda event: remove_placeholder_pass(passwordEntry, "Enter Your Password"))
passwordEntry.bind("<FocusOut>", lambda event: insert_placeholder_pass(passwordEntry, "Enter Your Password"))
insert_placeholder_pass(passwordEntry, "Enter Your Password")  # Call insert_placeholder initially

# Create checkbox to toggle password visibility
check_var = customtkinter.StringVar(value="off")
my_check = customtkinter.CTkCheckBox(inside_frame, text="Show password ", variable=check_var, onvalue="on", offvalue="off", command=show_password, width=1, height=1, text_color="black")
my_check.place(x=66, y=259)

# Create forgot password label
label4 = customtkinter.CTkLabel(master=inside_frame, text="Forgot password?", font=('Century Gothic', 13), text_color="blue", cursor="hand2")
label4.place(x=270, y=254)
label4.bind("<Button-1>", lambda event: forget_password())

# Create sign-in button
signin_button = customtkinter.CTkButton(master=inside_frame, width=335, height=42, text='Sign in', font=('', 14), corner_radius=6, command=login)
signin_button.place(x=57, y=350)

# Create sign-in result label
signin_result = customtkinter.CTkLabel(master=inside_frame, text="")

# Create label for registration prompt
label5 = customtkinter.CTkLabel(master=inside_frame, text="Don't have an account yet?", font=('Century Gothic', 12))
label5.place(x=60, y=398)

# Create label for sign-up link
label6 = customtkinter.CTkLabel(master=inside_frame, text=" Sign Up", font=('Century Gothic', 14.5), cursor="hand2")
label6.place(x=230, y=398)
label6.bind("<Enter>", on_hover_enter)
label6.bind("<Leave>", on_hover_leave)
label6.bind("<Button-1>", lambda event: callback("signup.py"))

# Run the application
signin.mainloop()