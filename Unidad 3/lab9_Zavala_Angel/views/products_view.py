"""Vista: ventana de productos con exportación de reportes."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# formato -> (extensión, descripción para el diálogo de guardado)
FORMATOS = {
    "CSV": (".csv", "Archivo CSV"),
    "TXT": (".txt", "Archivo de texto"),
    "JSON": (".json", "Archivo JSON"),
    "PDF": (".pdf", "Documento PDF"),
}


class ProductsView:

    def __init__(self, root):
        self.ventana = tk.Toplevel(root)

        self.ventana.title("Inventario de productos")
        self.ventana.geometry("620x440")
        self.ventana.configure(bg="#FDF2E9")
        self.ventana.resizable(False, False)

        self.titulo = tk.Label(
            self.ventana,
            text="INVENTARIO DE PRODUCTOS",
            font=("Verdana", 16, "bold"),
            bg="#FDF2E9",
            fg="#873600"
        )
        self.titulo.pack(pady=14)

        # --- Área de controles: formato + botón exportar ---
        self.marco_controles = tk.Frame(self.ventana, bg="#FDF2E9")
        self.marco_controles.pack(pady=6)

        self.lbl_formato = tk.Label(
            self.marco_controles,
            text="Formato:",
            font=("Verdana", 10, "bold"),
            bg="#FDF2E9",
            fg="#873600"
        )
        self.lbl_formato.pack(side="left", padx=(0, 6))

        self.combo_formato = ttk.Combobox(
            self.marco_controles,
            values=list(FORMATOS.keys()),
            state="readonly",
            width=8,
            font=("Verdana", 10)
        )
        self.combo_formato.current(0)
        self.combo_formato.pack(side="left", padx=(0, 12))

        self.btn_exportar = tk.Button(
            self.marco_controles,
            text="Exportar Reporte",
            bg="#CA6F1E",
            fg="white",
            font=("Verdana", 10, "bold"),
            cursor="hand2"
        )
        self.btn_exportar.pack(side="left")

        # --- Tabla de productos ---
        self.marco_tabla = tk.Frame(self.ventana, bg="#FDF2E9")
        self.marco_tabla.pack(fill="both", expand=True, padx=16, pady=12)

        columnas = ("id", "nombre", "precio", "stock")
        self.tabla = ttk.Treeview(
            self.marco_tabla, columns=columnas, show="headings", height=10
        )
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("nombre", width=280)
        self.tabla.column("precio", width=110, anchor="e")
        self.tabla.column("stock", width=90, anchor="e")

        scroll = ttk.Scrollbar(
            self.marco_tabla, orient="vertical", command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    # ---------- Métodos que usa el Controlador ----------
    def obtener_formato(self):
        """Devuelve el formato elegido en el Combobox ('CSV', 'TXT', ...)."""
        return self.combo_formato.get()

    def cargar_tabla(self, productos):
        """Llena el Treeview con la lista de productos (diccionarios)."""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for p in productos:
            self.tabla.insert(
                "",
                "end",
                values=(
                    p["id_producto"],
                    p["nombre"],
                    f"${float(p['precio']):.2f}",
                    p["stock"],
                )
            )

    def pedir_ruta_archivo(self, formato):
        """Abre el diálogo 'Guardar como'. Devuelve la ruta o '' si se cancela."""
        extension, descripcion = FORMATOS[formato]
        return filedialog.asksaveasfilename(
            parent=self.ventana,
            title=f"Guardar reporte {formato}",
            defaultextension=extension,
            initialfile=f"reporte_productos{extension}",
            filetypes=[(descripcion, f"*{extension}")]
        )

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "error":
            messagebox.showerror(titulo, mensaje, parent=self.ventana)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje, parent=self.ventana)
        else:
            messagebox.showinfo(titulo, mensaje, parent=self.ventana)
