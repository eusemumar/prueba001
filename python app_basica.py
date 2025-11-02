import tkinter as tk

# Crear ventana
ventana = tk.Tk()
ventana.title("Mi primera app en Python")
ventana.geometry("300x200")

# Crear etiqueta y botón
etiqueta = tk.Label(ventana, text="¡Hola, Eusebio!", font=("Arial", 14))
etiqueta.pack(pady=20)

def saludar():
    etiqueta.config(text="¡Bienvenido a Python GUI!")

boton = tk.Button(ventana, text="Saludar", command=saludar)
boton.pack(pady=10)

# Ejecutar app
ventana.mainloop()
