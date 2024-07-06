import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sys
from emailVerification import send_email, generate_random



#Retrieve arguments from command line
args = sys.argv[1].split(":")
recipient_email = args[0]
random_number = args[1]






#--------------------- Functions ---------------------#

def resend_email():
    global random_number
    random_number = generate_random(6)
    send_email(recipient_email, random_number)
 
    
def cancel():
    confirmed_cancel = messagebox.askyesno("Confirmation", "Are you sure you want to cancel?")
    if confirmed_cancel:
        dialog.destroy()
        frame.destroy()
        sys.exit(1)
    
def submit_pin(entry, dialog):
    pin = entry.get()
    print("Entered PIN in input_dialog:", pin)
    print("Random Number in input_dialog:", random_number)
    if pin == random_number:
        print("PIN is equal to random number")
        print(pin)  # Print the PIN to stdout with "PIN ="
        dialog.destroy()
        frame.destroy()
        sys.exit(0)
    elif pin.strip() and (pin != random_number):  
        # Check if the PIN is not empty and not equal to random_number
        messagebox.showerror("Error", "Incorrect PIN. Please try again.")
    elif pin.strip() == "": 
        # Display an error message for empty PIN
        messagebox.showerror("Error", "Please enter a PIN.")
    else:
        messagebox.showerror("Error", "Error occured.")
        
        
def update_timer(dialog, timer_label,  time_left = 60):
    # Update timer label
    timer_label.configure(text=f"    Resending new in: {time_left} seconds")
    if time_left == 0:
        # resend new email automatically
        resend_email()
        # Reset the timer
        time_left = 60
    else:
        time_left -= 1
    
    # Schedule the next update after 1 second
    dialog.after(1000, update_timer, dialog, timer_label, time_left)
    





#------------------ Frames and their content ------------------#

frame = ctk.CTk()  # Initialize customtkinter frame


# Get the screen width and height
screen_width = frame.winfo_screenwidth()
screen_height = frame.winfo_screenheight()

# Set the size of the dialog
dialog_width = 310 
dialog_height = 230  
x_offset = 150  # Adjust to move the dialog box more to the right

x = (screen_width - dialog_width) // 2 + x_offset
y = (screen_height - dialog_height) // 2

# Set frame properties
frame.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
frame.resizable(width=False, height=False)
frame.title("Verification check")
frame.iconbitmap(r'icons/001_first_aid_box_Dnj_icon.ico')

# Create the dialog frame inside parent frame 
dialog = ctk.CTkFrame(master=frame)
dialog.grid(row=0, column=0, sticky="nsew")  # Use grid to make the dialog frame fill the entire parent frame

# Ensure resizing of the dialog frame with the parent frame
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Add label
label = ctk.CTkLabel(dialog, text="Enter 6-digit Pin", font=('Arial', 15))
label.pack(pady=20)
    
# Add entry box
entry = ctk.CTkEntry(dialog, height=32)
entry.place(x=87, y=60)

# Add "Submit" button
submit_button = ctk.CTkButton(dialog, text="Submit", width=100, font=('Arial', 14, 'bold'), command=lambda: submit_pin(entry, dialog))
submit_button.place(x=42, y=115)

# Add "Cancel" button
cancel_button = ctk.CTkButton(dialog, text="Cancel", width=100,  font=('Arial', 14, 'bold'), command=cancel)
cancel_button.place(x=162, y=115)

# Add timer label
timer_label = ctk.CTkLabel(dialog, text="", font=('Arial', 12))
timer_label.place(x=12, y=160)

# Schedule the activation of "Resend" button every 1 minute
# Set initial time left to 60 seconds
update_timer(dialog, timer_label)

# Run the main event loop
frame.mainloop()