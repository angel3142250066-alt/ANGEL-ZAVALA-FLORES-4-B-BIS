"""Vista: ventana de registro de usuarios."""
import tkinter as tk
from tkinter import messagebox


class RegisterView:

    def __init__(self, root):
        self.ventana = tk.Toplevel(root)

        # PERSONALIZAR 1: título de la ventana
        self.ventana.title("Registro de nuevos usuarios")

        # PERSONALIZAR 2: dimensiones
        self.ventana.geometry("440x470")

        # PERSONALIZAR 3: color de fondo
        self.ventana.configure(bg="#EBF5FB")

        self.ventana.resizable(False, False)

        # Mantiene la ventana asociada a la principal
        self.ventana.transient(root)
        self.ventana.grab_set()

        # PERSONALIZAR 4: título
        self.titulo = tk.Label(
            self.ventana,
            text="CREAR CUENTA",
            font=("Verdana", 19, "bold"),
            bg="#EBF5FB",
            fg="#1B4F72"
        )
        self.titulo.pack(pady=18)

        # PERSONALIZAR 5: etiquetas
        etiqueta = {"bg": "#EBF5FB", "fg": "#154360", "font": ("Verdana", 10, "bold")}

        self.lbl_nombre = tk.Label(self.ventana, text="Nombre completo:", **etiqueta)
        self.lbl_nombre.pack()

        self.entry_nombre = tk.Entry(self.ventana, width=34, font=("Verdana", 10))
        self.entry_nombre.pack(pady=4)

        self.lbl_email = tk.Label(self.ventana, text="Correo electrónico:", **etiqueta)
        self.lbl_email.pack()

        self.entry_email = tk.Entry(self.ventana, width=34, font=("Verdana", 10))
        self.entry_email.pack(pady=4)

        self.lbl_password = tk.Label(self.ventana, text="Contraseña:", **etiqueta)
        self.lbl_password.pack()

        self.entry_password = tk.Entry(self.ventana, width=34, show="*", font=("Verdana", 10))
        self.entry_password.pack(pady=4)

        self.lbl_confirmar = tk.Label(self.ventana, text="Confirmar contraseña:", **etiqueta)
        self.lbl_confirmar.pack()

        self.entry_confirmar = tk.Entry(self.ventana, width=34, show="*", font=("Verdana", 10))
        self.entry_confirmar.pack(pady=4)

        # PERSONALIZAR 6: botón guardar
        self.btn_guardar = tk.Button(
            self.ventana,
            text="Guardar registro",
            width=24,
            bg="#2E86C1",
            fg="white",
            font=("Verdana", 10, "bold"),
            cursor="hand2"
        )
        self.btn_guardar.pack(pady=12)

        self.btn_cancelar = tk.Button(
            self.ventana,
            text="Cancelar",
            width=24,
            command=self.cerrar,
            cursor="hand2"
        )
        self.btn_cancelar.pack()

        self.entry_nombre.focus_set()

    def obtener_datos(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get()
        confirmar = self.entry_confirmar.get()
        return nombre, email, password, confirmar

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "error":
            messagebox.showerror(titulo, mensaje, parent=self.ventana)
        else:
            messagebox.showinfo(titulo, mensaje, parent=self.ventana)

    def cerrar(self):
        self.ventana.destroy()
