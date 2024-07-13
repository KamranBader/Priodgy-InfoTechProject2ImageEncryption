import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import cv2
import numpy as np

# Initialize tkinter window
window = tk.Tk()
window.geometry("1000x800")
window.title("Kami's Project - Image Encryption Decryption")

# Set background color to black and text color to green
window.configure(bg="black")

# Global variables
x = None
eimg = None
image_encrypted = None
key = None
panelA = None  # Initialize panelA as global variable
panelB = None  # Initialize panelB as global variable

# Function to open an image file
def open_img():
    global x, panelA, panelB, eimg
    x = filedialog.askopenfilename(title='Open', filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if x:
        try:
            img = Image.open(x)
            eimg = img.copy()  # Keep a reference to the original image
            img = img.resize((400, 400))  # Resize image for display
            img = ImageTk.PhotoImage(img)
            
            if panelA is None or panelB is None:
                panelA = Label(image_frame, image=img, borderwidth=2, relief="solid", width=400, height=400)
                panelA.image = img
                panelA.grid(row=0, column=0, padx=10, pady=10)
                
                panelB = Label(image_frame, image=img, borderwidth=2, relief="solid", width=400, height=400)
                panelB.image = img
                panelB.grid(row=0, column=1, padx=10, pady=10)
            else:
                panelA.configure(image=img)
                panelB.configure(image=img)
                panelA.image = img
                panelB.image = img
        except Exception as e:
            messagebox.showerror("Error", f"Error opening image: {str(e)}")
    else:
        messagebox.showwarning("Warning", "No image selected.")

# Function to encrypt an image
def encrypt_image(file_path):
    global image_encrypted, key
    try:
        image_input = cv2.imread(file_path, 0)
        if image_input is not None:
            (x1, y) = image_input.shape
            image_input = image_input.astype(float) / 255.0
            mu, sigma = 0, 0.1
            key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
            image_encrypted = image_input / key
            cv2.imwrite('image_encrypted.jpg', image_encrypted * 255)
            img_encrypted = Image.open('image_encrypted.jpg')
            img_encrypted = img_encrypted.resize((400, 400))  # Resize encrypted image for display
            img_encrypted = ImageTk.PhotoImage(img_encrypted)
            panelB.configure(image=img_encrypted)
            panelB.image = img_encrypted
            messagebox.showinfo("Encrypt Status", "Image Encrypted successfully.")
        else:
            messagebox.showwarning("Warning", "Failed to read image.")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {str(e)}")

# Function to decrypt an image
def decrypt_image():
    global image_encrypted, key
    try:
        if image_encrypted is not None and key is not None:
            image_output = image_encrypted * key
            image_output *= 255.0
            cv2.imwrite('image_output.jpg', image_output)
            img_decrypted = Image.open('image_output.jpg')
            img_decrypted = img_decrypted.resize((400, 400))  # Resize decrypted image for display
            img_decrypted = ImageTk.PhotoImage(img_decrypted)
            panelB.configure(image=img_decrypted)
            panelB.image = img_decrypted
            messagebox.showinfo("Decrypt Status", "Image decrypted successfully.")
        else:
            messagebox.showwarning("Warning", "Image not encrypted yet.")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {str(e)}")

# Function to handle window exit
def exit_window():
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# Top Label for Project Title
title_label = tk.Label(window, text="Kami's Project", fg="green", bg="black", font=("Courier", 24, "bold"))
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# Create a frame for image display
image_frame = Frame(window, width=800, height=400, bg="black")
image_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

# Button for opening image
choose_button = Button(window, text="Choose", command=open_img, font=("Arial", 20), bg="orange", fg="blue", borderwidth=3, relief="raised")
choose_button.grid(row=2, column=0, padx=10, pady=10)

# Button for encrypting image
encrypt_button = Button(window, text="Encrypt", command=lambda: encrypt_image(x), font=("Arial", 20), bg="light green", fg="blue", borderwidth=3, relief="raised")
encrypt_button.grid(row=2, column=1, padx=10, pady=10)

# Button for decrypting image
decrypt_button = Button(window, text="Decrypt", command=decrypt_image, font=("Arial", 20), bg="orange", fg="blue", borderwidth=3, relief="raised")
decrypt_button.grid(row=2, column=2, padx=10, pady=10)

# Button to exit the window
exit_button = Button(window, text="EXIT", command=exit_window, font=("Arial", 20), bg="red", fg="blue", borderwidth=3, relief="raised")
exit_button.grid(row=2, column=3, padx=10, pady=10)

# Main loop to run the tkinter window
window.protocol("WM_DELETE_WINDOW", exit_window)
window.mainloop()
