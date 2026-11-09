"""Controlador: lista de productos y exportación de reportes (polimorfismo)."""
import math

from exporters import (
    ExportadorCSV,
    ExportadorTXT,
    ExportadorJSON,
    ExportadorPDF,
)


class ProductController:

    # formato elegido en la Vista -> clase hija que sabe generarlo
    EXPORTADORES = {
        "CSV": ExportadorCSV,
        "TXT": ExportadorTXT,
        "JSON": ExportadorJSON,
        "PDF": ExportadorPDF,
    }

    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

        # El botón envía al método el formato seleccionado en el Combobox.
        self.vista.btn_exportar.config(
            command=lambda: self.generar_reporte(self.vista.obtener_formato())
        )

        self.vista.btn_agregar.config(command=self.agregar_producto)

        self.cargar_productos()

    def agregar_producto(self):
        nombre, precio_txt, stock_txt = self.vista.obtener_datos_producto()

        if not nombre or not precio_txt or not stock_txt:
            self.vista.mostrar_mensaje(
                "Campos vacíos",
                "Nombre, precio y stock son obligatorios.",
                "error"
            )
            return

        if len(nombre) > 100:
            self.vista.mostrar_mensaje(
                "Nombre muy largo",
                "El nombre puede tener máximo 100 caracteres.",
                "error"
            )
            return

        try:
            precio = float(precio_txt)
            if not math.isfinite(precio) or precio < 0:
                raise ValueError
        except ValueError:
            self.vista.mostrar_mensaje(
                "Precio inválido",
                "Ingresa un precio numérico mayor o igual a 0 (ej. 18.50).",
                "error"
            )
            return

        try:
            stock = int(stock_txt)
            if stock < 0:
                raise ValueError
        except ValueError:
            self.vista.mostrar_mensaje(
                "Stock inválido",
                "Ingresa un stock entero mayor o igual a 0.",
                "error"
            )
            return

        resultado = self.modelo.registrar_producto(nombre, precio, stock)

        if resultado == "ok":
            self.vista.mostrar_mensaje(
                "Producto agregado",
                f"'{nombre}' se registró correctamente."
            )
            self.vista.limpiar_formulario()
            self.cargar_productos()
        else:
            self.vista.mostrar_mensaje(
                "Error",
                "No fue posible registrar el producto. "
                "Verifica la conexión con PostgreSQL.",
                "error"
            )

    def cargar_productos(self):
        productos = self.modelo.obtener_todos()

        if productos is None:
            self.vista.mostrar_mensaje(
                "Error",
                "No fue posible consultar los productos. "
                "Verifica la conexión con PostgreSQL.",
                "error"
            )
            return

        self.vista.cargar_tabla(productos)

    def generar_reporte(self, formato):
        clase_exportador = self.EXPORTADORES.get(formato)

        if clase_exportador is None:
            self.vista.mostrar_mensaje(
                "Formato inválido",
                "Selecciona un formato de la lista.",
                "error"
            )
            return

        # Lista actual de productos desde el Modelo
        datos = self.modelo.obtener_todos()

        if datos is None:
            self.vista.mostrar_mensaje(
                "Error",
                "No fue posible consultar los productos.",
                "error"
            )
            return

        if not datos:
            self.vista.mostrar_mensaje(
                "Sin datos",
                "No hay productos para exportar.",
                "warning"
            )
            return

        ruta = self.vista.pedir_ruta_archivo(formato)

        if not ruta:        # el usuario canceló el diálogo
            return

        # Polimorfismo: solo se instancia la clase hija elegida y se llama
        # a .exportar() sin importar cuál sea el formato.
        exportador = clase_exportador()

        try:
            exportador.exportar(datos, ruta)
        except Exception as error:
            self.vista.mostrar_mensaje(
                "Error al exportar",
                f"No se pudo generar el archivo {formato}:\n{error}",
                "error"
            )
            return

        self.vista.mostrar_mensaje(
            "Exportación exitosa",
            f"Reporte {formato} guardado en:\n{ruta}"
        )