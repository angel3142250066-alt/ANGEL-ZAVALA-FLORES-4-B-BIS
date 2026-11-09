"""Controlador: lista de productos y exportación de reportes (polimorfismo)."""
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

        self.cargar_productos()

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
