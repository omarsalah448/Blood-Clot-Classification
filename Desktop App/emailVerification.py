import emailCredentials   # Import email credentials
import smtplib
from tkinter import messagebox
import random


# Fixed subject
fixed_subject = "Medical Application Security Check"

# Generating 6 digit random number
def generate_random(length):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    
def send_email(recipient, random_number):
    try:
        # Your email credentials
        sender_email = emailCredentials.email
        sender_password = emailCredentials.password

        # Compose the email message with subject and message
        email_message = f"Subject: {fixed_subject}\n\nYour exclusive verification code - {random_number}. Keep it safe and secure!"

        # Establish a secure connection with the Gmail SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)

        # Send the email with fixed subject and message
        server.sendmail(sender_email, recipient, email_message)

        # Close the connection
        server.quit()

    except smtplib.SMTPAuthenticationError:
        messagebox.showerror("Error", "Failed to authenticate")
    except smtplib.SMTPException as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")