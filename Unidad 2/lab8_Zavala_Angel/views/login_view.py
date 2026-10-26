"""Vista: ventana de inicio de sesión."""
import tkinter as tk
from tkinter import messagebox


class LoginView:

    def __init__(self, root):
        self.root = root

        # PERSONALIZAR 1: título de la ventana
        self.root.title("Sistema de acceso - Lab 8")

        # PERSONALIZAR 2: tamaño de la ventana
        self.root.geometry("440x380")

        # PERSONALIZAR 3: color de fondo
        self.root.configure(bg="#FDF2E9")

        self.root.resizable(False, False)

        # PERSONALIZAR 4: título (texto, fuente y colores)
        self.titulo = tk.Label(
            root,
            text="INICIAR SESION",
            font=("Verdana", 20, "bold"),
            bg="#FDF2E9",
            fg="#873600"
        )
        self.titulo.pack(pady=20)

        # PERSONALIZAR 5: etiquetas
        self.lbl_email = tk.Label(
            root,
            text="Usuario o correo electrónico:",
            font=("Verdana", 10, "bold"),
            bg="#FDF2E9",
            fg="#6E2C00"
        )
        self.lbl_email.pack()

        # PERSONALIZAR 6: campos de entrada
        self.entry_email = tk.Entry(
            root,
            width=32,
            font=("Verdana", 11),
            relief="solid",
            bd=1
        )
        self.entry_email.pack(pady=5)

        self.lbl_password = tk.Label(
            root,
            text="Contraseña:",
            font=("Verdana", 10, "bold"),
            bg="#FDF2E9",
            fg="#6E2C00"
        )
        self.lbl_password.pack()

        # show="*" oculta los caracteres al escribir
        self.entry_password = tk.Entry(
            root,
            width=32,
            font=("Verdana", 11),
            show="*",
            relief="solid",
            bd=1
        )
        self.entry_password.pack(pady=5)

        # PERSONALIZAR 7: botón de login
        self.btn_login = tk.Button(
            root,
            text="Entrar",
            width=22,
            bg="#D35400",
            fg="white",
            font=("Verdana", 11, "bold"),
            cursor="hand2"
        )
        self.btn_login.pack(pady=15)

        # PERSONALIZAR 8: botón para abrir el registro
        self.btn_register = tk.Button(
            root,
            text="Registrarme",
            width=22,
            bg="#1E8449",
            fg="white",
            font=("Verdana", 10, "bold"),
            cursor="hand2"
        )
        self.btn_register.pack()

    def obtener_datos(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get()
        return email, password

    def limpiar_campos(self):
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "error":
            messagebox.showerror(titulo, mensaje, parent=self.root)
        else:
            messagebox.showinfo(titulo, mensaje, parent=self.root)
