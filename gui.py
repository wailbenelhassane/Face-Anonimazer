import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
from main import process_image, process_video, process_webcam # Importar las funciones de procesamiento

# Crear ventana principal
root = TkinterDnD.Tk()
root.title("Image/Video Processing")
root.geometry("600x400")

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg"), ("Video Files", "*.mp4;*.avi;*.mov")]
    )
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def select_output_dir():
    dir_path = filedialog.askdirectory(title="Select Output Directory")
    if dir_path:
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, dir_path)

def process_files():
    file_path = file_entry.get()
    output_dir = output_dir_entry.get()
    blur_strength = int(blur_strength_entry.get())
    mode = mode_var.get()

    if not os.path.exists(file_path):
        messagebox.showerror("Error", "The selected file does not exist.")
        return

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    try:
        if mode == "image":
            output_path = process_image(file_path, output_dir, blur_strength)
        elif mode == "video":
            output_path = process_video(file_path, output_dir, blur_strength)
        else:
            messagebox.showerror("Error", "Webcam mode is not supported yet.")
            return

        messagebox.showinfo("Success", f"Processing completed. File saved at:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def on_drop(event):
    file_path = event.data
    if os.path.exists(file_path):
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
    else:
        messagebox.showerror("Error", "Invalid file dropped.")

# Interfaz
frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="Select Input File:").grid(row=0, column=0, sticky="e")
file_entry = tk.Entry(frame, width=40)
file_entry.grid(row=0, column=1, padx=10)
file_button = tk.Button(frame, text="Browse", command=select_file)
file_button.grid(row=0, column=2)

tk.Label(frame, text="Select Output Directory:").grid(row=1, column=0, sticky="e")
output_dir_entry = tk.Entry(frame, width=40)
output_dir_entry.grid(row=1, column=1, padx=10)
output_dir_button = tk.Button(frame, text="Browse", command=select_output_dir)
output_dir_button.grid(row=1, column=2)

tk.Label(frame, text="Blur Strength:").grid(row=2, column=0, sticky="e")
blur_strength_entry = tk.Entry(frame)
blur_strength_entry.grid(row=2, column=1, padx=10)
blur_strength_entry.insert(0, "40")

tk.Label(frame, text="Select Mode:").grid(row=3, column=0, sticky="e")
mode_var = tk.StringVar(value="image")
tk.Radiobutton(frame, text="Image", variable=mode_var, value="image").grid(row=3, column=1, sticky="w")
tk.Radiobutton(frame, text="Video", variable=mode_var, value="video").grid(row=3, column=2, sticky="w")

# Botón para iniciar la webcam en tiempo real
live_webcam_button = tk.Button(root, text="Live Webcam", command=lambda: process_webcam(int(blur_strength_entry.get())))
live_webcam_button.pack(pady=10)


drop_area = tk.Label(root, text="Drag and Drop File Here", relief="solid", width=40, height=5)
drop_area.pack(pady=20)
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', on_drop)

process_button = tk.Button(root, text="Process", command=process_files)
process_button.pack(pady=20)

root.mainloop()
