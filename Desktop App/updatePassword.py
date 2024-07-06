import tkinter 
import customtkinter 
from tkinter import messagebox, Image
from PIL import Image
import sqlite3
import sys
import hashlib
import subprocess
import re
from emailVerification import send_email, generate_random


# Retrieve the email from forgetPassword.py
recipient_email = sys.argv[1]







#--------------------- Functions ---------------------#

# Function to hash password using MD5
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()



def mask_email(recipient_email):
    parts = recipient_email.split("@")
    if len(parts[0]) <= 2:
        masked_email = parts[0][0] + "*"*(len(parts[0])-1) + "@" + parts[1]
    else:
        masked_email = parts[0][0] + "*"*(len(parts[0])-2) + parts[0][-1] + "@" + parts[1]
    return masked_email


# Function to send email
random_number = generate_random(6)
send_email(recipient_email, random_number)
trials = 2  # Initialize count 

def change_password(code_entry, dialog):
    global trials  # Declare count as global to modify its value
    code = code_entry.get()
    password = password_entry.get()
    rewrite_password = rewrite_password_entry.get()

    if code == "" or password == "" or rewrite_password == "":
        messagebox.showerror("Error", "All Fields Are Required.")
    elif code == random_number:
        if is_valid_password(password) and is_valid_password(rewrite_password):
            if password == rewrite_password:  
                # Connect to the database
                conn = sqlite3.connect("app_database.db", timeout=20)
                cursor = conn.cursor()

                # Execute an SQL UPDATE query to update the password
                cursor.execute("UPDATE user SET password = ? WHERE email = ?", (hash_password(password), recipient_email))

                # Commit the transaction
                conn.commit()

                # Close the database connection
                conn.close()

                # Optional: Display a message indicating successful password update
                messagebox.showinfo("Success", "Password changed successfully!")
                frame.destroy()
                sys.exit(0)
            else:
                messagebox.showerror("Error", "Passwords must match.")
        elif not is_valid_password(rewrite_password) or not is_valid_password(password):
                messagebox.showerror("Error", "Write a valid password.")
        
    elif code.strip() and (code != random_number):
        trials -= 1
        if trials == 0:
            warningLabel.configure(text="No more trials", text_color="red", height=8, font=('Century Gothic', 9))
            warningLabel.place(x=316, y=191)
            messagebox.showerror("Error", "Failed to change password! No more trials left.")
            dialog.destroy()
            frame.destroy()
        else:
            messagebox.showerror("Error", "Incorrect code entered. Please try again.")
            warningLabel.configure(text=f"you have {trials} trial left", text_color="red", height=8, font=('Century Gothic', 9))
            warningLabel.place(x=285, y=191)

    


# Function to toggle password visibility for a specific entry
def show_password_for_entry(password_entry, show_label, unshow_label,x1,y1):
    if password_entry.cget('show') == '*':
        password_entry.configure(show='')
        show_label.place(x=x1, y=y1)  # Show the "show" image
        unshow_label.place_forget()  # Hide the "unshow" image
    else:
        password_entry.configure(show='*')
        show_label.place_forget()  # Hide the "show" image
        unshow_label.place(x=x1, y=y1)  # Show the "unshow" image

def is_valid_password(password):
    # Password must be at least 9 characters long
    # Password must contain at least one uppercase letter, one lowercase letter, one digit, one special character (such as @$!%*?&_)
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{9,}$"
    return re.match(pattern, password)

    
    # Function to check password validity
def check_password(event=None):
    password = password_entry.get()
    if is_valid_password(password):
        checking.configure(text="Valid password", text_color="green", height=8, font=('Century Gothic', 10))
        checking.place(x=300, y=266)
    else:
        checking.configure(text="Password must contain more than 8 characters, 1 uppercase letter, and 1 special character", text_color="red", height=8, font=('Century Gothic', 7.5))
        checking.place(x=15, y=266)
        
def check_rewritePass(event=None):
    rewritePassword = rewrite_password_entry.get()
    password = password_entry.get()
    if rewritePassword == password:
        checking_rewrite.configure(text="Valid password", text_color="green", height=8, font=('Century Gothic', 10))
        checking_rewrite.place(x=300, y=343)
    else:
        checking_rewrite.configure(text="Invalid password", text_color="red", height=8, font=('Century Gothic', 7.5))
        checking_rewrite.place(x=300, y=343)
        
        
        
        
        
        
#------------------ Frames and their content ------------------#

frame = customtkinter.CTk()  # Initialize customtkinter frame

# Get the screen width and height
screen_width = frame.winfo_screenwidth()
screen_height = frame.winfo_screenheight()

# Set the size of the dialog
dialog_width = 400
dialog_height = 440
x_offset = 150  # Adjust to move the dialog box more to the right

x = (screen_width - dialog_width) // 2 + x_offset
y = (screen_height - dialog_height) // 2

# Set frame properties
frame.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
frame.resizable(width=False, height=False)
frame.title("Changing Password")
frame.iconbitmap(r'icons/001_first_aid_box_Dnj_icon.ico')

# Create the dialog frame inside parent frame 
dialog = customtkinter.CTkFrame(master=frame)
dialog.grid(row=0, column=0, sticky="nsew")  # Use grid to make the dialog frame fill the entire parent frame

# Ensure resizing of the dialog frame with the parent frame
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

label = customtkinter.CTkLabel(dialog, text="We have sent a password reset code by email to", font=('', 13))
label.place(x=13, y=55)
label2 = customtkinter.CTkLabel(dialog, text=f"{mask_email(recipient_email)}. Enter it below to reset your password.", font=('', 13))
label2.place(x=13, y=75)


label3 = customtkinter.CTkLabel(dialog, text="Code", font=('', 15))
label3.place(x=15, y=123)
code_entry = customtkinter.CTkEntry(dialog, height=35, width=370)
code_entry.place(x=13, y=155)

label4 = customtkinter.CTkLabel(dialog, text="New Password", font=('', 15))
label4.place(x=15, y=200)
password_entry = customtkinter.CTkEntry(dialog, height=35, width=370, show='*')
password_entry.place(x=13, y=232)
password_entry.bind("<KeyRelease>", check_password)
checking = customtkinter.CTkLabel(master=dialog, text="")

label5 = customtkinter.CTkLabel(dialog, text="Enter New Password Again", font=('', 15))
label5.place(x=15, y=277)
rewrite_password_entry = customtkinter.CTkEntry(dialog, height=35, width=370, show='*')
rewrite_password_entry.place(x=13, y=309)
rewrite_password_entry.bind("<KeyRelease>", check_rewritePass)
checking_rewrite = customtkinter.CTkLabel(master=dialog, text="")


warningLabel = customtkinter.CTkLabel(master=dialog, text="")

# Add show image
showImg = Image.open("images/showPass.png")
resizedShow = customtkinter.CTkImage(light_image=showImg, dark_image=showImg, size=(25, 20))

# Add unshow image
unshowImg = Image.open("images/unshow.png")
resizedUnshow = customtkinter.CTkImage(light_image=unshowImg, dark_image=unshowImg, size=(25, 20))


# label image for password
label_showImg = customtkinter.CTkLabel(master=dialog, text="", image=resizedShow, bg_color='#f9f9fa', cursor="hand2")
label_showImg.place(x=343, y=235)
label_showImg.bind("<Button-1>", lambda event: show_password_for_entry(password_entry, label_showImg, label_unshowImg,343,235))

label_unshowImg = customtkinter.CTkLabel(master=dialog, text="", image=resizedUnshow, bg_color='#f9f9fa', cursor="hand2")
label_unshowImg.place(x=343, y=235)
label_unshowImg.bind("<Button-1>", lambda event: show_password_for_entry(password_entry, label_showImg, label_unshowImg,343,235))



# label image for rewrite password
label_showImg2 = customtkinter.CTkLabel(master=dialog, text="", image=resizedShow, bg_color='#f9f9fa', cursor="hand2")
label_showImg2.place(x=343, y=312)
label_showImg2.bind("<Button-1>", lambda event: show_password_for_entry(rewrite_password_entry, label_showImg2, label_unshowImg2,343,312))

label_unshowImg2 = customtkinter.CTkLabel(master=dialog, text="", image=resizedUnshow, bg_color='#f9f9fa', cursor="hand2")
label_unshowImg2.place(x=343, y=312)
label_unshowImg2.bind("<Button-1>", lambda event: show_password_for_entry(rewrite_password_entry, label_showImg2, label_unshowImg2,343,312))

# Add button to submit changes
button = customtkinter.CTkButton(dialog, text="Change Password", font=('Arial', 14, 'bold'), height=37, width=370,  command=lambda:change_password(code_entry, dialog))
button.place(x=13, y=367)

frame.mainloop()
