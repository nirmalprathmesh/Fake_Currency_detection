import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from predict import predict_note_and_authenticity


currency_names = {
    "10": "₹10 Note",
    "20": "₹20 Note",
    "50": "₹50 Note",
    "100": "₹100 Note",
    "200": "₹200 Note",
    "500": "₹500 Note",
    "2000": "₹2000 Note"
}


window = tk.Tk()
window.title("Currency Detection System")
window.geometry("600x450")
window.configure(bg="white")


title = tk.Label(window, text="Currency Detection System", font=("Arial",20,"bold"), bg="white")
title.pack(pady=15)


image_label = tk.Label(window, bg="white")
image_label.pack(pady=10)


result_label = tk.Label(window, text="Upload a currency image", font=("Arial",16,"bold"), bg="white")
result_label.pack(pady=10)


def upload_image():

    file_path = filedialog.askopenfilename(filetypes=[("Image Files","*.jpg *.png *.jpeg")])

    if not file_path:
        return

    img = Image.open(file_path)
    img = img.resize((350,150))

    img_tk = ImageTk.PhotoImage(img)

    image_label.config(image=img_tk)
    image_label.image = img_tk

    denomination, authenticity = predict_note_and_authenticity(file_path)

    display_note = currency_names.get(str(denomination), "Unknown")

    result_label.config(text=f"Detected: {display_note} - {authenticity.upper()}")


upload_button = tk.Button(window, text="Upload Currency Image", font=("Arial",12), command=upload_image)
upload_button.pack(pady=20)


window.mainloop()