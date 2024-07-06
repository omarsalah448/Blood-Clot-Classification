import tkinter
import customtkinter  
from PIL import Image
from tkinter import messagebox, StringVar
import subprocess
import re
import hashlib
import sqlite3
from emailVerification import send_email, generate_random




customtkinter.set_appearance_mode("system")

signupview = customtkinter.CTk()
screen_width = signupview.winfo_screenwidth()
screen_height = signupview.winfo_screenheight()

signupview.rowconfigure(0, weight=1)
signupview.columnconfigure(0, weight=1)
height = 700
width = 1240
x = (screen_width // 2) - (width // 2)
y = (screen_height // 4) - (height // 4)
signupview.geometry('{}x{}+{}+{}'.format(width, height, x, y))
signupview.resizable(width=True, height=True)
signupview.title("Sign up")
signupview.iconbitmap(r'icons/001_first_aid_box_Dnj_icon.ico')

# define variables
EmployeeID = StringVar()
Name = StringVar()
Email = StringVar()
Password = StringVar()
Confirm_pass = StringVar()








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
        
def clear():
    EmployeeID.set("")
    Name.set("")
    Email.set("")
    Password.set("")
    Confirm_pass.set("")

# Function to handle signup process
def signup():   
    employeeId = IdEntry.get()
    name = nameEntry.get()
    emailEntered = emailEntry.get()
    email = emailEntered.lower()
    password = passwordEntry.get()
    confirmPassword = confirmPassEntry.get()
    
    if employeeId == "" or name == "" or email == "" or password == "" or confirmPassword == "":
        messagebox.showerror("Error", "All Fields Are Required")
    elif password != confirmPassword:
        messagebox.showerror("Error", "Password and Confirm password did not match!!")
    else:
        try:
            conn = sqlite3.connect("app_database.db", timeout=20)
            c = conn.cursor()

            # Check if the doctor exists in the hospital
            c.execute("SELECT Email FROM hospital_doctor WHERE EmployeeID=?", (employeeId,))
            email_doctor = c.fetchone()

            if email_doctor is not None:
                # Check for correctness of id and email
                if email_doctor[0] == email:
                    # Check if the doctor belongs to the Laboratory department
                    check_department = c.execute("SELECT 1 FROM hospital_doctor WHERE EmployeeID=? AND Department=?", (employeeId, "Laboratory"))
                    check_department_result = check_department.fetchone()

                    if check_department_result:
                        # Check if the email and id are unique before inserting into the user table
                        c.execute("SELECT Email,EmployeeID FROM user WHERE Email=?", (email,))
                        existing_user = c.fetchall()

                        if existing_user:
                            messagebox.showerror("Error", "User already exists")
                        else:
                            messagebox.showinfo("", "Check your email and write the sent 6-digit code")
                            # Generate random number and send email
                            random_number = generate_random(6)
                            send_email(email, random_number)
                            # Concatenate entry3 and random_number into a single string separated by a delimiter
                            argument = email + ":" + random_number
                            # Run subprocess with the concatenated argument
                            result = subprocess.run(["python", "emailVerificationInput.py", argument], capture_output=True, text=True)
                            #Check if the input dialog returned success
                            if result.returncode == 0:
                                # save in database if and only if pin matched
                                pin_matched = result.stdout.strip()
                                if pin_matched:
                                    c.execute("INSERT INTO user(EmployeeID, Name, Email, Password) VALUES(?, ?, ?, ?)",
                                    (employeeId, name, email, hashlib.md5(password.encode()).hexdigest()))
                                    conn.commit()
                                    conn.close()
                                    # Passing name as an argument to accountCreated.py
                                    subprocess.Popen(["python", "signin.py"])
                                    clear()
                                    signupview.destroy()
                    else:
                        messagebox.showerror("Error", "Doctor is not from Laboratory department")
                else:
                    messagebox.showerror("Error", "Incorrect email or id")
            else:
                messagebox.showerror("Error", "Doctor not found in hospital")
                
        except Exception as es:
            print("error", es)
            messagebox.showerror("Error", "Something went wrong! Try again")
            
            
def callback(file_path):
    subprocess.Popen(["python", file_path])
    signupview.destroy()


# Function to toggle password visibility for a specific entry
def show_password_for_entry(password_entry, show_label, unshow_label,x1,y1):
    if password_entry.cget('show') == '':
        password_entry.configure(show='*')
        show_label.place_forget()  # Hide the "show" image
        unshow_label.place(x=x1, y=y1)  # Show the "unshow" image
    else:
        password_entry.configure(show='')
        show_label.place(x=x1, y=y1)  # Show the "show" image
        unshow_label.place_forget()  # Hide the "unshow" image

# Function to insert placeholder text
def insert_placeholder_password(entry_widget, placeholder_text, placeholder_color="grey"):
    if entry_widget.get() == "":
        entry_widget.insert(0, placeholder_text)
        entry_widget.configure(text_color=placeholder_color, show='')  # Show the placeholder text initially

# Function to remove placeholder text
def remove_placeholder_password(entry_widget, placeholder_text, default_color="black"):
    if entry_widget.get() == placeholder_text:
        entry_widget.delete(0, "end")
        entry_widget.configure(text_color=default_color, show='*')  # Hide the placeholder text when typing starts
        
def is_valid_password(password):
    # Password must be at least 9 characters long
    # Password must contain at least one uppercase letter, one lowercase letter, one digit, one special character (such as @$!%*?&_)
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{9,}$"
    return re.match(pattern, password)

    # Function to check password validity
def check_password(event=None):
    password = passwordEntry.get()
    
    if is_valid_password(password):
        checking_Password.configure(text="Valid password", text_color="green", height=8, font=('Century Gothic', 10))
        checking_Password.place(x=359, y=495)
    else:
        checking_Password.configure(text="Password must contain more than 8 characters, 1 uppercase letter, and 1 special character", text_color="red", height=8, font=('Century Gothic', 8))
        checking_Password.place(x=50, y=495)
        
def check_rewritePass(event=None):
    rewritePassword = confirmPassEntry.get()
    password = passwordEntry.get()
    if rewritePassword == password:
        checking_rewrite.configure(text="Valid password", text_color="green", height=8, font=('Century Gothic', 10))
        checking_rewrite.place(x=359, y=583)
    else:
        checking_rewrite.configure(text="Invalid password", text_color="red", height=8, font=('Century Gothic', 8))
        checking_rewrite.place(x=359, y=583)
        
# Function to validate email
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Function to check email validity
def check_email(event=None):
    email = emailEntry.get()
    if is_valid_email(email):
        checking_email.configure(text="Valid email", text_color="green", height=8, font=('Century Gothic', 10))
        checking_email.place(x=359, y=404)
    else:
        checking_email.configure(text="Invalid email!", text_color="red", height=8, font=('Century Gothic', 9))
        checking_email.place(x=359, y=404)
        
        





#------------------ Frames and their content ------------------#

frame = customtkinter.CTkFrame(master=signupview, width=screen_width, height=900)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

left_frame = customtkinter.CTkFrame(master=frame, fg_color="darkgray")
left_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Set relwidth to 0 to take up half of the screen

image = Image.open('images/cover.JPG')
img = customtkinter.CTkImage(light_image=image, dark_image=image, size=(screen_width, 800))

# Create the label with the image
label1 = customtkinter.CTkLabel(master=left_frame, text="", image=img)
label1.pack(fill='both', expand=True)

right_frame = customtkinter.CTkFrame(master=frame, fg_color="white")
right_frame.place(relx=0.5, rely=0, relwidth=1, relheight=1)  # Set relwidth to 0.5 to take up half of the screen

# Calculate the dimensions for inside_bottom_frame to be centered within bottom_frame
inside_right_frame_width = 0.8 * right_frame.winfo_width()  # 30% of bottom_frame width
inside_right_frame_height = 0.6 * right_frame.winfo_height()  # 60% of bottom_frame height
inside_right_frame_relx = 0.02  # Move  from the left edge of bottom_frame
inside_right_frame_rely = (1 - 0.8) / 2  # Center vertically within bottom_frame

inside_right_frame = customtkinter.CTkFrame(master=right_frame, fg_color="white")
inside_right_frame.place(relx=inside_right_frame_relx, rely=inside_right_frame_rely, relwidth=0.6, relheight=0.8)

label2=customtkinter.CTkLabel(master=inside_right_frame, text="Create new account", font= ('Century Gothic', 25))
label2.place(x=90,y=47)

labelForSignin=customtkinter.CTkLabel(master=inside_right_frame, text="Already a member?", font= ('Century Gothic', 14))
labelForSignin.place(x=50,y=110)

linkForSignin=customtkinter.CTkLabel(master=inside_right_frame, text="Sign in", font= ('Century Gothic', 14), text_color="blue", cursor="hand2")
linkForSignin.place(x=220,y=110)
linkForSignin.bind("<Button-1>", lambda event: callback("signin.py"))

label3=customtkinter.CTkLabel(master=inside_right_frame, text="Employee ID", font= ('Century Gothic', 14, 'bold'))
label3.place(x=50,y=155)

# Create entry widget
IdEntry = customtkinter.CTkEntry(master=inside_right_frame, width=390, height=43, textvariable=EmployeeID)
IdEntry.place(x=50, y=180)

# Bind events to insert and remove placeholder text
IdEntry.bind("<FocusIn>", lambda event: remove_placeholder(IdEntry, "EmployeeID"))
IdEntry.bind("<FocusOut>", lambda event: insert_placeholder(IdEntry, "EmployeeID"))
insert_placeholder(IdEntry, "EmployeeID")  # Call insert_placeholder initially

label4=customtkinter.CTkLabel(master=inside_right_frame, text="Name", font= ('Century Gothic', 14, 'bold'))
label4.place(x=50,y=245)

nameEntry=customtkinter.CTkEntry(master=inside_right_frame, width=390, height=43, textvariable=Name)
nameEntry.place(x=50, y=270)

# Bind events to insert and remove placeholder text
nameEntry.bind("<FocusIn>", lambda event: remove_placeholder(nameEntry, "Name"))
nameEntry.bind("<FocusOut>", lambda event: insert_placeholder(nameEntry, "Name"))
insert_placeholder(nameEntry, "Name")  # Call insert_placeholder initially

label5=customtkinter.CTkLabel(master=inside_right_frame, text="Email", font= ('Century Gothic', 14, 'bold'))
label5.place(x=50,y=335)

emailEntry=customtkinter.CTkEntry(master=inside_right_frame, width=390, height=43, textvariable=Email)
emailEntry.place(x=50, y=360)

# Bind events to insert and remove placeholder text
emailEntry.bind("<FocusIn>", lambda event: remove_placeholder(emailEntry, "Email"))
emailEntry.bind("<FocusOut>", lambda event: insert_placeholder(emailEntry, "Email"))
insert_placeholder(emailEntry, "Email")  # Call insert_placeholder initially
emailEntry.bind("<KeyRelease>", check_email)
checking_email = customtkinter.CTkLabel(master=inside_right_frame, text="")

label6=customtkinter.CTkLabel(master=inside_right_frame, text="Password", font= ('Century Gothic', 14, 'bold'))
label6.place(x=50,y=425)

# Set up your password entry
passwordEntry = customtkinter.CTkEntry(master=inside_right_frame, width=390, height=43, placeholder_text="Password", textvariable=Password)
passwordEntry.place(x=50, y=450)

# Bind events to insert and remove placeholder text
passwordEntry.bind("<FocusIn>", lambda event: remove_placeholder_password(passwordEntry, "Password"))
passwordEntry.bind("<FocusOut>", lambda event: insert_placeholder_password(passwordEntry, "Password"))
insert_placeholder(passwordEntry, "Password")  # Call insert_placeholder initially

passwordEntry.bind("<KeyRelease>", check_password)
checking_Password = customtkinter.CTkLabel(master=inside_right_frame, text="")

label7=customtkinter.CTkLabel(master=inside_right_frame, text="Confirm Password", font= ('Century Gothic', 14, 'bold'))
label7.place(x=50,y=515)

confirmPassEntry=customtkinter.CTkEntry(master=inside_right_frame, width=390, height=43, placeholder_text="Confirm Password", textvariable=Confirm_pass)
confirmPassEntry.place(x=50, y=540)

# Bind events to insert and remove placeholder text
confirmPassEntry.bind("<FocusIn>", lambda event: remove_placeholder_password(confirmPassEntry, "Confirm Password"))
confirmPassEntry.bind("<FocusOut>", lambda event: insert_placeholder_password(confirmPassEntry, "Confirm Password"))
insert_placeholder(confirmPassEntry, "Confirm Password")  # Call insert_placeholder initially

confirmPassEntry.bind("<KeyRelease>", check_rewritePass)
checking_rewrite = customtkinter.CTkLabel(master=inside_right_frame, text="")

# Add show image
showImg = Image.open("images/showPass.png")
resizedShow = customtkinter.CTkImage(light_image=showImg, dark_image=showImg, size=(25, 20))

# Add unshow image
unshowImg = Image.open("images/unshow.png")
resizedUnshow = customtkinter.CTkImage(light_image=unshowImg, dark_image=unshowImg, size=(25, 20))


# label image for password
label_showImg = customtkinter.CTkLabel(master=inside_right_frame, text="", image=resizedShow, bg_color='#f9f9fa', cursor="hand2")
label_showImg.place(x=395, y=456)
label_showImg.bind("<Button-1>", lambda event: show_password_for_entry(passwordEntry, label_showImg, label_unshowImg,395,456))

label_unshowImg = customtkinter.CTkLabel(master=inside_right_frame, text="", image=resizedUnshow, bg_color='#f9f9fa', cursor="hand2")
label_unshowImg.place(x=395, y=456)
label_unshowImg.bind("<Button-1>", lambda event: show_password_for_entry(passwordEntry, label_showImg, label_unshowImg,395,456))


# label image for rewrite password
label_showImg2 = customtkinter.CTkLabel(master=inside_right_frame, text="", image=resizedShow, bg_color='#f9f9fa', cursor="hand2")
label_showImg2.place(x=395, y=546)
label_showImg2.bind("<Button-1>", lambda event: show_password_for_entry(confirmPassEntry, label_showImg2, label_unshowImg2,395,546))

label_unshowImg2 = customtkinter.CTkLabel(master=inside_right_frame, text="", image=resizedUnshow, bg_color='#f9f9fa', cursor="hand2")
label_unshowImg2.place(x=395, y=546)
label_unshowImg2.bind("<Button-1>", lambda event: show_password_for_entry(confirmPassEntry, label_showImg2, label_unshowImg2,395,546))

button1=customtkinter.CTkButton(master=inside_right_frame,width=370,text='Sign up', font=('', 14), corner_radius=15, height=43, cursor="hand2", command=signup)
button1.place(x=50,y=620)

signupview.mainloop()