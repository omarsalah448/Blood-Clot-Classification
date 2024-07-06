import tkinter as tk
from tkinter import messagebox
import sys
from diagnosingModelUtils import ClotModelSingle, process_image, predict

file_path = sys.argv[1]

def main():
    image_path = file_path
    model_path = "center_id_7_epoch_8_target_0.594.h5"

    # Display a messagebox to inform the user to wait
    messagebox.showinfo("Please Wait", "Processing the image. Please wait...")

    result = predict(image_path, model_path)
    print(result) 

if __name__ == "__main__":
    main()