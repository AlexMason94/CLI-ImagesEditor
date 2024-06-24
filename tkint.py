import tkinter as tk
from tkinter import filedialog

def seleccionar_carpeta(prompt):
    print(prompt)
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    carpeta_destino = filedialog.askdirectory()
    root.destroy()
    return carpeta_destino

print(seleccionar_carpeta("Por favor, selecciona una carpeta de destino:"))