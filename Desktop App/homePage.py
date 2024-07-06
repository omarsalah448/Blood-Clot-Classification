import customtkinter 
import tkinter
from tkinter import Image, filedialog, messagebox, StringVar
from PIL import Image
import sqlite3
import sys
import subprocess
import tkinter.simpledialog
import hashlib
import re
from emailVerification import send_email, generate_random
import os
from datetime import datetime


# Retrieve the email from signin page
email = sys.argv[1]






main = customtkinter.CTk()
main.iconbitmap(r'icons/001_first_aid_box_Dnj_icon.ico')
main.title("My App")
main.rowconfigure(0, weight=1)
main.columnconfigure(0, weight=1)
height = 700
width = 1240
x = (main.winfo_screenwidth() // 2) - (width // 2)
y = (main.winfo_screenheight() // 4) - (height // 4)
main.geometry('{}x{}+{}+{}'.format(width, height, x, y))
main.resizable(width=True, height=True)





# Getting data from database
conn = sqlite3.connect("app_database.db", timeout=20)
c = conn.cursor()

c.execute("SELECT * FROM User WHERE Email=?", [(email)])
result = c.fetchone()  # Fetch only one row since email should be unique
UserID, EmployeeID, _, Email, Password = result


c.execute("SELECT * FROM hospital_doctor WHERE EmployeeID=?", [(EmployeeID)])
Third_result = c.fetchone()  
_, Name, NationalID, _, PhoneNumber, _ = Third_result








#--------------------- Functions ---------------------#
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def clear():
    patientName.set("")
    nationalID.set("")
    
def callbackToSignin(file_path):
    confirmedReturnToSignin = messagebox.askyesno("Confirmation", "Are you sure you want to go to sign out?")
    if confirmedReturnToSignin:
        subprocess.Popen(["python", file_path])
        main.destroy()
    
# Function to handle forget password action
def change_password():
    confirmedChangePassword = messagebox.askyesno("Change Password", "Are you sure you want to change password?")
    if confirmedChangePassword:
        Result = subprocess.run(["python", "updateProfilePassword.py", email], capture_output=True, text=True)
        if Result.returncode == 0:
            subprocess.Popen(["python", "signin.py"])
            main.destroy()


def delete_account():
    confirmedDeleteAccount = messagebox.askyesno("Confirmation", "Are you sure you want to permanently delete your account?")
    if confirmedDeleteAccount:
        random_number = generate_random(6)
        send_email(email, random_number)
        # Concatenate entry3 and random_number into a single string separated by a delimiter
        argument = email + ":" + random_number
        Result = subprocess.run(["python", "emailVerificationInput.py", argument], capture_output=True, text=True)
        if Result.returncode == 0:
            # save in database if and only if pin matched
            pin_matched = Result.stdout.strip()
            if pin_matched:
                conn = sqlite3.connect("app_database.db", timeout=20)
                c = conn.cursor()
                c.execute("DELETE FROM User WHERE UserID=?", (UserID,))
                conn.commit()
                c.close()
                conn.close()
                messagebox.showinfo("", "Your account has been deleted successfully")
                subprocess.Popen(["python", "signin.py"])
                main.destroy()
    
# Function to prompt for password
def prompt_password():
    password_dialog = tkinter.Toplevel()
    password_dialog.title("Authentication Check")
    password_dialog.iconbitmap(r'icons/001_first_aid_box_Dnj_icon.ico')
    
    # Get the screen width and height
    screen_width = password_dialog.winfo_screenwidth()
    screen_height = password_dialog.winfo_screenheight()
    
    # Calculate the x and y coordinates to center the frame
    x = (screen_width - 260) // 2 + 20 # Center horizontally
    y = (screen_height - 180) // 2 + 25 # Center vertically
    password_dialog.geometry(f"260x180+{x}+{y}")  # Set the geometry
    password_dialog.resizable(width=False, height=False)
    
    password_label = tkinter.Label(password_dialog, text="Enter your password:", font=("Arial", 12))
    password_label.place(relx=0.5, rely=0.28, anchor=tkinter.CENTER)

    password_var = tkinter.StringVar()
    password_entry = tkinter.Entry(password_dialog, show='*', textvariable=password_var, width=35)
    password_entry.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER, height=30)

    def submit_password():
        password_dialog.destroy()

    submit_button = tkinter.Button(password_dialog, text="Submit", font=("Arial", 13), command=submit_password, width=14)
    submit_button.place(relx=0.5, rely=0.72, anchor=tkinter.CENTER, height=32)

    password_dialog.grab_set()  # Make the dialog modal
    password_dialog.wait_window()  # Wait for the dialog to close
    
    return password_var.get()


# Function to check password and proceed accordingly
def check_password(frame):
    passDialogOutput = prompt_password()

    # Check if the password is not None
    if passDialogOutput != '':
        # Hash the password and compare it with the stored password
        if hash_password(passDialogOutput) == Password:
            show_frame(frame)
        else:
            # Incorrect password
            messagebox.showerror("Error", "Incorrect password!")
    else:
        messagebox.showerror("Error", "No password entered!")


# Function to toggle the visibility of frames and activate corresponding button
active_button = None
def show_frame(frame):
    global active_button
    for btn, frm in frames.items():
        if frm == frame:
            buttons[btn].configure(state="active", text_color="white")  # Activate and change text color
            active_button = btn  # Update active button
            frame.tkraise()
        else:
            buttons[btn].configure(state="normal", text_color="grey")  # Deactivate and change text color
            
    return active_button

         
file_path=None
def open_image():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tif *.tiff")])
    if file_path:
        checkIcon = Image.open("images/checkMark2.png")
        checkIcon_resized = customtkinter.CTkImage(light_image=checkIcon, dark_image=checkIcon, size=(32, 27))
        checkIconLabel.configure(image=checkIcon_resized)
        print("Selected file path:", file_path)  # Print the file path
    return file_path


def show_img_button(rows, frame_number):
    if frame_number <= len(rows):  # Check if the frame number corresponds to an existing patient
        file_path = rows[frame_number - 1][3]  
        national_ID = rows[frame_number - 1][2]  
        if file_path:
            os.startfile(file_path)
        else:
            print("File path not found for national ID:", national_ID)
    else:  
        print("No image available for new patients")
        

def modify_patient_button(rows, frame_number):
    modify_patient = tkinter.Toplevel()
    modify_patient.title("Modification")
    modify_patient.iconbitmap(r'icons/001_first_aid_box_Dnj_icon.ico')

    national_ID = rows[frame_number - 1][2]

    # Get the screen width and height
    screen_width = modify_patient.winfo_screenwidth()
    screen_height = modify_patient.winfo_screenheight()

    # Calculate the x and y coordinates to center the frame
    x = (screen_width - 440) // 2 + 30  # Center horizontally
    y = (screen_height - 390) // 2 + 25  # Center vertically
    modify_patient.geometry(f"440x390+{x}+{y}")  # Set the geometry
    modify_patient.resizable(width=False, height=False)

    conn = sqlite3.connect("app_database.db", timeout=20)
    c = conn.cursor()
    c.execute("SELECT Name FROM ischemic_stroke_patient WHERE NationalID=?", [(national_ID)])
    nameOfPatient = c.fetchone()[0]
    c.close()
    conn.close()


    original_name_label = tkinter.Label(modify_patient, text="Patient name:" + nameOfPatient, font=("Arial", 13))
    original_name_label.place(x=40, y=30)

    original_nationalID_label = tkinter.Label(modify_patient, text="National ID:" + str(national_ID), font=("Arial", 13))
    original_nationalID_label.place(x=40, y=52)
    
    label_in_modify = tkinter.Label(modify_patient, text="Choose what you need to modify", font=("Arial", 13))
    label_in_modify.place(relx=0.5, rely=0.27, anchor=tkinter.CENTER)
    
    name_label = tkinter.Label(modify_patient, text="Modify Name:" ,font=("Arial", 13))
    name_label.place(relx=0.2, rely=0.38, anchor=tkinter.CENTER)

    name_entry = tkinter.Entry(modify_patient, width=57)
    name_entry.place(relx=0.48, rely=0.47, anchor=tkinter.CENTER, height=30)

    nationalID_label = tkinter.Label(modify_patient, text="Modify National ID:", font=("Arial", 13))
    nationalID_label.place(relx=0.23, rely=0.61, anchor=tkinter.CENTER)

    nationalID_entry = tkinter.Entry(modify_patient, width=57)
    nationalID_entry.place(relx=0.48, rely=0.7, anchor=tkinter.CENTER, height=30)

    def submit():
        New_name = name_entry.get()  # Get the entered name
        New_nationalID = nationalID_entry.get().strip()  # Get the entered national ID, and remove any leading/trailing spaces
        
        
        # Check if both entries are empty
        if not New_name and not New_nationalID:
            messagebox.showwarning("No Changes", "No changes detected. Please enter data to modify.")
            return  # Return to exit the function if no changes are detected
        
        else:
            confirmedChangePassword = messagebox.askyesno("Confirm modifications", "Are you sure you want to change data?")
            if confirmedChangePassword:
    
                # Establish a connection and cursor
                conn = sqlite3.connect("app_database.db", timeout=20)
                c = conn.cursor()

                flag = 0
                # Check if the name entry is not empty
                if New_name:
                    c.execute("UPDATE ischemic_stroke_patient SET Name = ? WHERE NationalID = ?", (New_name, national_ID))
                    flag = 1
                # Check if the national ID entry is not empty
                if New_nationalID:
                    if not re.match(r'^\d{14}$', New_nationalID):
                        messagebox.showerror("Error", "National ID should be exactly 14 digits.")
                        return
                    else:
                        try:
                            c.execute("UPDATE ischemic_stroke_patient SET NationalID = ? WHERE NationalID = ?", (New_nationalID, national_ID))
                            flag = 1
                        except sqlite3.IntegrityError as e:
                            # Handle the case where the update would result in a duplicate NationalID
                            print("Error:", e)
                            messagebox.showerror("Error","Failed to update NationalID due to duplicate value.")
                
                if flag == 1:
                    modify_patient.destroy()
                    messagebox.showinfo("Success", "Changes have been saved")
          
            
                # Commit the transaction and close the connection
                conn.commit()
                conn.close()

                conn = sqlite3.connect("app_database.db", timeout=20)
                c = conn.cursor()
                c.execute("SELECT * FROM ischemic_stroke_patient")
                rows = c.fetchall()  # Update 'rows' with the modified data
                conn.close()

                # Call diagnosed with the updated 'rows'
                diagnosed(rows)

            

    submit_button = tkinter.Button(modify_patient, text="Submit", font=("Arial", 13), command=submit, width=14)
    submit_button.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER, height=32)

    modify_patient.grab_set()  # Make the dialog modal
    modify_patient.wait_window()  # Wait for the dialog to close



def rediagnose_patient_button(rows, frame_number):
   national_ID = rows[frame_number - 1][2]
   new_uploading_dialog = tkinter.Toplevel()
   new_uploading_dialog.title("New diagnosing")
   new_uploading_dialog.iconbitmap(r'icons/001_first_aid_box_Dnj_icon.ico')
    
   # Get the screen width and height
   screen_width = new_uploading_dialog.winfo_screenwidth()
   screen_height = new_uploading_dialog.winfo_screenheight()
    
   # Calculate the x and y coordinates to center the frame
   x = (screen_width - 310) // 2 + 20 # Center horizontally
   y = (screen_height - 210) // 2 + 25 # Center vertically
   new_uploading_dialog.geometry(f"310x210+{x}+{y}")  # Set the geometry
   new_uploading_dialog.resizable(width=False, height=False)
    
   upload_img_label = tkinter.Label(new_uploading_dialog, text="Upload Image", font=("Arial", 12))
   upload_img_label.place(relx=0.5, rely=0.21, anchor=tkinter.CENTER)

   upload_img_button = tkinter.Button(new_uploading_dialog, text="upload   ", font=("Arial", 12), width=23, cursor="hand2")
   upload_img_button.place(relx=0.5, rely=0.38, anchor=tkinter.CENTER, height=40)
   upload_img_button.bind("<Button-1>", lambda event: new_upload())
   
   # Add upload icon
   uploadIcon = Image.open("images/uploadIcon.png")
   uploadIcon_resized = customtkinter.CTkImage(light_image=uploadIcon, dark_image=uploadIcon, size=(15, 10))

   # label image for upload icon
   uploadIconLabel = customtkinter.CTkLabel(master=new_uploading_dialog, text="", image=uploadIcon_resized, cursor="hand2")
   uploadIconLabel.place(relx=0.63, rely=0.38, anchor=tkinter.CENTER)
   uploadIconLabel.bind("<Button-1>", lambda event: new_upload())
   
   checkIconLabel_newupload = customtkinter.CTkLabel(master=new_uploading_dialog, text="", bg_color='#eef6f6')
   checkIconLabel_newupload.place(x=220, y=65)
   
   global new_file_path
   new_file_path = None
   
   def new_upload():
       global new_file_path
       new_file_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tif *.tiff")])
       if new_file_path:
            checkIcon_newupload = Image.open("images/checkMark2.png")
            checkIcon_newupload_resized = customtkinter.CTkImage(light_image=checkIcon_newupload, dark_image=checkIcon_newupload, size=(26, 21))
            checkIconLabel_newupload.configure(image=checkIcon_newupload_resized)
       return new_file_path
   

   def rediagnose():
        global new_file_path
        if new_file_path:
            print(new_file_path)
            confirmedRediagnosis = messagebox.askyesno("Confirmation", "Are you sure you want to rediagnose?")
            if confirmedRediagnosis:
                messagebox.showinfo("Please wait", "This might take a couple of minutes!")
                predictionResult = subprocess.run(["python", "runDiagnosingModel.py", new_file_path], capture_output=True, text=True)
                diagnosis_prediction = predictionResult.stdout
                
                conn = sqlite3.connect("app_database.db", timeout=20)
                c = conn.cursor()
                
                # Get EmployeeID of diagnosing user
                c.execute("SELECT EmployeeID FROM User WHERE Email=?", (email,))
                DiagnosingID = c.fetchone()
                
                # Extract the single value from the tuple
                DiagnosingID = DiagnosingID[0] if DiagnosingID else None
                
                # Convert to int to be updated in database
                IntDiagnosingID = int(DiagnosingID)
                IntNationalID = int(national_ID)
                c.execute("UPDATE ischemic_stroke_patient SET BloodClotImg = ?, Diagnosis = ?, DateOfDiagnosis = datetime('now','localtime'), EmployeeID = ? WHERE NationalID = ?", (new_file_path, diagnosis_prediction,  IntDiagnosingID, IntNationalID))
                
                messagebox.showinfo("Success", f"Data saved successfully! \nPatient diagnosis: {diagnosis_prediction}") 
                new_uploading_dialog.destroy()   
                
                # Commit the transaction and close the connection
                conn.commit()
                conn.close()

                conn = sqlite3.connect("app_database.db", timeout=20)
                c = conn.cursor()
                c.execute("SELECT * FROM ischemic_stroke_patient")
                rows = c.fetchall()  # Update 'rows' with the modified data
                conn.close()

                # Call diagnosed with the updated 'rows'
                diagnosed(rows)
        else:        
            messagebox.showerror("Error", "Please upload a photo if you want to rediagnose!")
           

   rediagnose_button = tkinter.Button(new_uploading_dialog, text="rediagnose", font=("Arial", 13), width=14, cursor="hand2")
   rediagnose_button.place(relx=0.5, rely=0.78, anchor=tkinter.CENTER, height=32)
   rediagnose_button.bind("<Button-1>", lambda event: rediagnose())
   
   new_uploading_dialog.grab_set()  # Make the dialog modal
   new_uploading_dialog.wait_window()  # Wait for the dialog to close
    
  


def delete_patient_button(rows, frame_number):
    national_ID = rows[frame_number - 1][2] 
    confirmedDeletePatient = messagebox.askyesno("Deletion Confirmation", "Are you sure you want to permanently delete patient?")
    if confirmedDeletePatient:
        conn = sqlite3.connect("app_database.db", timeout=20)
        c = conn.cursor()
        c.execute("DELETE FROM ischemic_stroke_patient WHERE NationalID=?", (national_ID,))
        messagebox.showinfo("", "Patient has been deleted successfully")
        conn.commit()
        conn.close()
        
        conn = sqlite3.connect("app_database.db", timeout=20)
        c = conn.cursor()
        c.execute("SELECT * FROM ischemic_stroke_patient")
        rows = c.fetchall()  # Update 'rows' with the modified data
        conn.close()
        # Call diagnosed with the updated 'rows'
        diagnosed(rows)


def newDiagnose():
    Name = patientNameEntry.get()
    nationalId = nationalIdEntry.get()
    # Validate national ID
    if not re.match(r'^\d{14}$', nationalId):
        messagebox.showerror("Error", "National ID should be exactly 14 digits.")
        return
    
    if Name == "" or nationalId == "" or file_path == "":
        messagebox.showerror("Error", "All Fields Are Required")
    else:
        try:
            conn = sqlite3.connect("app_database.db", timeout=20)
            c = conn.cursor()
            # Check if the national ID already exists in the database
            c.execute("SELECT COUNT(*) FROM ischemic_stroke_patient WHERE NationalID=?", (nationalId,))
            count = c.fetchone()[0]
            if count > 0:
                messagebox.showerror("Error", "National ID already exists.")
                return
            c.execute("SELECT EmployeeID FROM User WHERE Email=?", (email,))
            ResultedRow = c.fetchone()
            # Extract the single value from the tuple
            IDdoctor_output = ResultedRow[0] if ResultedRow else None
            # Check if file_path is not empty
            if file_path:
                messagebox.showinfo("Please wait", "This might take a couple of minutes!")
                predictionResult = subprocess.run(["python", "runDiagnosingModel.py", file_path], capture_output=True, text=True)
                diagnosis_prediction = predictionResult.stdout
                c.execute("INSERT INTO ischemic_stroke_patient(Name, NationalID, BloodClotImg, Diagnosis, DateOfDiagnosis, EmployeeID) VALUES(?, ?, ?, ?, datetime('now','localtime'), ?)",
                          (Name, nationalId, file_path, diagnosis_prediction,  IDdoctor_output))
                messagebox.showinfo("Success", f"Data saved successfully! \nPatient diagnosis: {diagnosis_prediction}")      
                conn.commit()
                conn.close()
                clear()
                # Clear the checkIconLabel
                checkIconLabel.configure(image=None)
                # Fetch all patient data again from the database
                conn = sqlite3.connect('app_database.db')
                c = conn.cursor()
                c.execute("SELECT * FROM ischemic_stroke_patient")
                rows_modified = c.fetchall()
                conn.close()
                diagnosed(rows_modified)
            else:
                # User didn't upload a photo, show an error message
                messagebox.showerror("Error", "Please upload a photo.")
                
        except Exception as es:
            print("error", es)
            messagebox.showerror("Error", "Something went wrong! Try again")


# Function to get suggestions from the database
def get_suggestions(event=None):
    search_term = search_entry.get()
    conn = sqlite3.connect("app_database.db", timeout=20)
    c = conn.cursor()
    # Fetch suggestions from the database based on the search term
    c.execute("SELECT * FROM ischemic_stroke_patient WHERE Name LIKE ? OR NationalID LIKE ?", (f'%{search_term}%', f'%{search_term}%'))
    rows = c.fetchall()
    conn.close()
    diagnosed(rows)








#----------------Top and bottom Frames and their content ------------------#

# Calculate the heights for the top and bottom frames
total_height = main.winfo_screenheight()
top_frame_height = int(total_height * 0.07)  # 10% of the total height
bottom_frame_height = int(total_height * 0.93)  # 90% of the total height

# Create the top frame (header)
top_frame = customtkinter.CTkFrame(master=main, fg_color="#9bcaca")
top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.07)

# Create a label to act as the border at the bottom of the top frame
border_label = customtkinter.CTkLabel(master=top_frame, bg_color="#9bcaca", height=1, text="")
border_label.place(relx=0, rely=1, relwidth=1, anchor='w')


buttons = {}
buttons["Home"] = customtkinter.CTkButton(master=top_frame, text="Home", text_color="white",  font=('', 17, 'bold'), width=20, fg_color="#9bcaca", command=lambda: show_frame(home_frame))
buttons["Home"].place(x=35, y=15)

buttons["viewProfile"] = customtkinter.CTkButton(master=top_frame, text="View profile", text_color="white",  font=('', 17, 'bold'), width=20, fg_color="#9bcaca", command=lambda: check_password(viewprofile_frame))
buttons["viewProfile"].place(x=110, y=15)

buttons["diagnosedPatients"] = customtkinter.CTkButton(master=top_frame, text="Diagnosed patients", text_color="white",  font=('', 17, 'bold'), width=20, fg_color="#9bcaca", command=lambda: check_password(diagnosedPatients_frame))
buttons["diagnosedPatients"].place(x=230, y=15)

buttons["newPatientDiagnosis"] = customtkinter.CTkButton(master=top_frame, text="New patient diagnosis", text_color="white",  font=('', 17, 'bold'), width=20, fg_color="#9bcaca", command=lambda: check_password(newPatientDiagnosis_frame))
buttons["newPatientDiagnosis"].place(x=415, y=15)

signoutButton = customtkinter.CTkButton(master=top_frame, text="Sign out", text_color="black",  font=('', 18), width=150, height=33, fg_color="#79b9b9", cursor="hand2")
signoutButton.place(relx=0.9, rely=0.5, anchor=tkinter.CENTER)
signoutButton.bind("<Button-1>", lambda event: callbackToSignin("signin.py"))

# Create the bottom frame
bottom_frame = customtkinter.CTkFrame(master=main, fg_color="white")
bottom_frame.place(relx=0, rely=0.07, relwidth=1, relheight=0.93)









#------------------ Home frame and its content ------------------#

home_frame = customtkinter.CTkFrame(master=bottom_frame, fg_color="white")
home_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

left_frame = customtkinter.CTkFrame(master=home_frame, fg_color="white")
left_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Set relwidth to 0 to take up half of the screen

right_frame = customtkinter.CTkFrame(master=home_frame, fg_color="white")
right_frame.place(relx=0.35, rely=0, relwidth=1, relheight=1)  

base_home_right_frame = customtkinter.CTkFrame(master=right_frame, fg_color="white")
base_home_right_frame.place(relx=0.5, rely=0.5, relwidth=0.93, relheight=1, anchor=tkinter.CENTER)


photo_home_frame = customtkinter.CTkFrame(master=left_frame, fg_color="blue", width=560, height=320)
photo_home_frame.place(x=100, y=160)

# Load image for background
homeFrameCover = Image.open("images/homeCover2.png")

# Add image
homeFrameImg = customtkinter.CTkImage(light_image=homeFrameCover, dark_image=homeFrameCover, size=(300,290))

# Create background label
homeFrameLabelImg = customtkinter.CTkLabel(master=photo_home_frame, text="", image=homeFrameImg)
homeFrameLabelImg.pack(fill='both', expand=True)


# Words in right frame
photo_homewords_frame = customtkinter.CTkFrame(master=right_frame, fg_color="blue", width=700, height=320)
photo_homewords_frame.place(x=100, y=160)

# Load image for background
homeWordsFrameCover = Image.open("images/homewords.jpeg")

# Add image
homeWordsFrameImg = customtkinter.CTkImage(light_image=homeWordsFrameCover, dark_image=homeWordsFrameCover, size=(610,290))

# Create background label
homeWordsFrameLabelImg = customtkinter.CTkLabel(master=photo_homewords_frame, text="", image=homeWordsFrameImg)
homeWordsFrameLabelImg.pack(fill='both', expand=True)







#-------------------------View profile frame and its content ----------------------#

viewprofile_frame = customtkinter.CTkFrame(master=bottom_frame, fg_color="#fdfdfd")
viewprofile_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# Load image for background
viewprofileCover = Image.open("images/rm380-10.jpg")

# Add image
viewprofileImg = customtkinter.CTkImage(light_image=viewprofileCover, dark_image=viewprofileCover, size=(2000,800))

# Create background label
viewprofilelabelimg = customtkinter.CTkLabel(master=viewprofile_frame, text="", image=viewprofileImg)
viewprofilelabelimg.pack(fill='both', expand=True)

viewprofilebase_frame = customtkinter.CTkFrame(master=viewprofile_frame, width=520, height=560, fg_color="#fefefe", border_width=1)
viewprofilebase_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
viewprofilebase_frame.update_idletasks() 

# Create inside frame
viewprofileinside_frame = customtkinter.CTkFrame(master=viewprofilebase_frame, fg_color="#fdfdfd")
viewprofileinside_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor=tkinter.CENTER)

viewprofilelabel1 = customtkinter.CTkLabel(master=viewprofileinside_frame, text="Personal Information sheet", font=('Century Gothic', 20), text_color="black")
viewprofilelabel1.place(relx=0.5, rely=0.06, anchor=tkinter.CENTER)

IDvalue = customtkinter.CTkLabel(master=viewprofileinside_frame, text="Employee ID:  "+ str(EmployeeID), font=('Century Gothic', 15), text_color="black")
IDvalue.place(x=35, y=103)

nameValue = customtkinter.CTkLabel(master=viewprofileinside_frame, text="Name:  " + Name, font=('Century Gothic', 15), text_color="black")
nameValue.place(x=35, y=137)

nationalIDValue = customtkinter.CTkLabel(master=viewprofileinside_frame, text="National ID:  " + str(NationalID), font=('Century Gothic', 15), text_color="black")
nationalIDValue.place(x=35, y=165)

phoneNoValue = customtkinter.CTkLabel(master=viewprofileinside_frame, text="Phone Number:  " + str(PhoneNumber), font=('Century Gothic', 15), text_color="black")
phoneNoValue.place(x=35, y=195)

departmentValue = customtkinter.CTkLabel(master=viewprofileinside_frame, text="Department:   Laboratory Department", font=('Century Gothic', 15), text_color="black")
departmentValue.place(x=35, y=225)

emailValue = customtkinter.CTkLabel(master=viewprofileinside_frame, text="Email:  " + Email, font=('Century Gothic', 15), text_color="black")
emailValue.place(x=35, y=255)


viewprofilebutton1 = customtkinter.CTkButton(master=viewprofileinside_frame, text="Change Password", text_color="black",width=120, height=30, font=('', 12, 'bold'), fg_color="#d9d9d9")
viewprofilebutton1.place(x=35, y=301)
viewprofilebutton1.bind("<Button-1>", lambda event: change_password())

viewprofilebutton2 = customtkinter.CTkButton(master=viewprofileinside_frame, text="Delete Account", text_color="white",width=120, height=30, font=('', 12, 'bold'), fg_color="#ff3333")
viewprofilebutton2.place(x=175, y=301)
viewprofilebutton2.bind("<Button-1>", lambda event: delete_account())











#------------------ Diagnosed patients frame and its content ------------------#
 

# Connect to the SQLite database
conn = sqlite3.connect('app_database.db')  
c = conn.cursor()

# Execute a query to fetch data from a table
c.execute("SELECT * FROM ischemic_stroke_patient")  
rows = c.fetchall()  # Fetch all rows from the result set

# Close the cursor and connection
c.close()
conn.close()

diagnosedPatients_frame = customtkinter.CTkFrame(master=bottom_frame, fg_color="white")
diagnosedPatients_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

base_patients_frame = customtkinter.CTkFrame(master=diagnosedPatients_frame, fg_color="white")
base_patients_frame.place(relx=0.5, rely=0.5, relwidth=0.93, relheight=1, anchor=tkinter.CENTER)

# Create the search bar (Entry widget)
search_entry = customtkinter.CTkEntry(base_patients_frame, placeholder_text=" Search for name or national ID of patients ", font=('Arial', 12), width=400, height=35)
search_entry.place(relx=0.45, rely=0.1, anchor=tkinter.CENTER)


search_entry.bind('<KeyRelease>', get_suggestions)

# Create the search button
search_button = customtkinter.CTkButton(base_patients_frame, text="Search", font=("Helvetica", 15, 'bold'))
search_button.place(relx=0.69, rely=0.095, anchor=tkinter.CENTER)

# Create the new Tkinter frame below the search button and entry
new_frame = tkinter.Frame(master=base_patients_frame, bg="white")
new_frame.place(relx=0.5, rely=0.6, relwidth=0.9, relheight=0.7, anchor=tkinter.CENTER)

# Create a canvas
canvas = tkinter.Canvas(new_frame, bg="white")
canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

# Create a scrollbar
scrollbar = tkinter.Scrollbar(new_frame, orient=tkinter.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

# Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

# Create a frame inside the canvas to hold the mini frames
scrollable_frame = tkinter.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=scrollable_frame, anchor=tkinter.NW)

    
def diagnosed(rows):
    # Clear existing mini frames
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Define the number of rows and columns
    num_rows = len(rows)/3
    if isinstance(num_rows, float):
        num_rows = int(num_rows)
        num_rows +=1

    num_columns = 3

    # Calculate the gap between frames
    x_gap = 290
    y_gap = 220

    # Calculate positions
    positions = [(10 + x * x_gap, 10 + y * y_gap) for y in range(num_rows) for x in range(num_columns)]


    # Create mini frames and buttons
    mini_frames = []
    
    for row_index, row in enumerate(rows):
        if row_index >= len(positions):
            break  # Stop if there are no more positions to place frames
    
        x, y = positions[row_index]  # Get position for current row
    
        # Create mini frame
        mini_frame = tkinter.Frame(master=scrollable_frame, bg="white", bd=2, relief=tkinter.SOLID, width=290, height=200)
        mini_frame.grid(row=row_index // 3, column=row_index % 3, padx=25, pady=10)
    
        # Print data inside mini frame
        name_label = tkinter.Label(master=mini_frame, text="Name:  "+ row[1], font=('Century Gothic', 12), fg="black", bg="white")
        name_label.place(x=13, y=15)

        national_id_label = tkinter.Label(master=mini_frame, text="National ID:  " + str(row[2]), font=('Century Gothic', 12), fg="black", bg="white")
        national_id_label.place(x=13, y=40)
    
        diagnosis_label = tkinter.Label(master=mini_frame, text="Diagnosis Result:  " + row[4], font=('Century Gothic', 12), fg="black", bg="white")
        diagnosis_label.place(x=13, y=65)
    
        date_label = tkinter.Label(master=mini_frame, text="Date:  " + str(row[5]), font=('Century Gothic', 12), fg="black", bg="white")
        date_label.place(x=13, y=90)
        

        doctor_label = tkinter.Label(master=mini_frame, text="Employee ID:  " + str(row[6]), font=('Century Gothic', 12), fg="black", bg="white")
        doctor_label.place(x=13, y=115)
    
        # Add buttons to mini frame
        button1 = customtkinter.CTkButton(master=mini_frame, text="Image", width=8, command=lambda frame_number=row_index+1: show_img_button(rows,frame_number))
        button1.place(x=10, y=153)
    
        button2 = customtkinter.CTkButton(master=mini_frame, text="Modify", width=8, fg_color="green", command=lambda frame_number=row_index+1: modify_patient_button(rows,frame_number))
        button2.place(x=71, y=153)
    
        button3 = customtkinter.CTkButton(master=mini_frame, text="Rediagnose", width=12, fg_color="green", command=lambda frame_number=row_index+1: rediagnose_patient_button(rows,frame_number))
        button3.place(x=134, y=153)

        button4 = customtkinter.CTkButton(master=mini_frame, text="Delete", width=8, fg_color="#cc0000", command=lambda frame_number=row_index+1: delete_patient_button(rows,frame_number))
        button4.place(x=225, y=153)

        mini_frames.append(mini_frame)
    
diagnosed(rows)











#------------------ New patient diagnosis frame and its content ------------------#

newPatientDiagnosis_frame = customtkinter.CTkFrame(master=bottom_frame, fg_color="#fdfdfd")
newPatientDiagnosis_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# define variables
patientName = StringVar()
nationalID = StringVar()

# Load image for background
newPatientDiagnosisCover = Image.open("images/rm380-10.jpg")

# Add image
newPatientDiagnosisImg = customtkinter.CTkImage(light_image=newPatientDiagnosisCover, dark_image=newPatientDiagnosisCover, size=(2000,800))

# Create background label
labelimg = customtkinter.CTkLabel(master=newPatientDiagnosis_frame, text="", image=newPatientDiagnosisImg)
labelimg.pack(fill='both', expand=True)

base_frame = customtkinter.CTkFrame(master=newPatientDiagnosis_frame, width=520, height=460, fg_color="#eef6f6", border_width=2, corner_radius=10)
base_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
base_frame.update_idletasks() 
base_frame.configure(corner_radius=25)

# Create inside frame
inside_frame = customtkinter.CTkFrame(master=base_frame, fg_color="#eef6f6")
inside_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor=tkinter.CENTER)

label1 = customtkinter.CTkLabel(master=inside_frame, text="Enter data below to diagnose", font=('Century Gothic', 22), text_color="black")
label1.place(relx=0.5, rely=0.11, anchor=tkinter.CENTER)

patientNameLabel = customtkinter.CTkLabel(master=inside_frame, text="Enter patient name", font=('Century Gothic', 16), text_color="black")
patientNameLabel.place(x=35, y=111)

patientNameEntry = customtkinter.CTkEntry(master=inside_frame, width=400, height=43, textvariable=patientName)
patientNameEntry.place(x=35, y=136)

nationalIdLabel = customtkinter.CTkLabel(master=inside_frame, text="Enter patient national ID", font=('Century Gothic', 16), text_color="black")
nationalIdLabel.place(x=35, y=194)

nationalIdEntry = customtkinter.CTkEntry(master=inside_frame, width=400, height=43, textvariable=nationalID)
nationalIdEntry.place(x=35, y=220)

uploadLabel = customtkinter.CTkLabel(master=inside_frame, text="Upload patient pathology image", font=('Century Gothic', 16), text_color="black")
uploadLabel.place(x=35, y=280)


# Add upload icon
uploadIcon = Image.open("images/uploadIcon.png")
uploadIcon_resized = customtkinter.CTkImage(light_image=uploadIcon, dark_image=uploadIcon, size=(22, 18))

# label image for upload icon
uploadIconLabel = customtkinter.CTkLabel(master=inside_frame, text="", image=uploadIcon_resized, bg_color='#eef6f6', cursor="hand2")
uploadIconLabel.place(x=305, y=280)
uploadIconLabel.bind("<Button-1>", lambda event: open_image())


# label image for check mark icon
checkIconLabel = customtkinter.CTkLabel(master=inside_frame, text="", bg_color='#eef6f6')
checkIconLabel.place(x=380, y=280)

diagnoseButton = customtkinter.CTkButton(master=inside_frame, text="Diagnose", width=240, height=42, font=('', 18, 'bold'), corner_radius=6, command=newDiagnose)
diagnoseButton.place(relx=0.5, rely=0.86, anchor=tkinter.CENTER)










#----------------------- Mapping buttons to frames  ----------------------------#
frames = {"Home": home_frame, "viewProfile": viewprofile_frame, "diagnosedPatients": diagnosedPatients_frame, "newPatientDiagnosis": newPatientDiagnosis_frame}



# Initially show the home frame
show_frame(home_frame)

main.mainloop()