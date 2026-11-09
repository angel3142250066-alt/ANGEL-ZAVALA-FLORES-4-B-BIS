"""Módulo de exportación: jerarquía de clases para generar reportes de productos.

Las librerías de formato (csv, json, fpdf) se usan ÚNICAMENTE en este archivo.
El Controlador solo instancia la clase hija y llama a .exportar().
"""
import csv
import json

from fpdf import FPDF

# Columnas de la tabla "Database_OOP".products, en orden
COLUMNAS = ("id_producto", "nombre", "precio", "stock")


class Exportador:
    """Clase base (interfaz). Las clases hijas deben sobrescribir exportar()."""

    def exportar(self, datos, ruta_archivo):
        """Método que debe ser sobrescrito por las clases hijas"""
        raise NotImplementedError("Este método debe ser implementado por la subclase.")

    @staticmethod
    def _normalizar(datos):
        """Convierte cada fila a dict con tipos simples (acepta dicts o tuplas)."""
        filas = []
        for fila in datos:
            if not isinstance(fila, dict):
                fila = dict(zip(COLUMNAS, fila))
            filas.append({
                "id_producto": int(fila["id_producto"]),
                "nombre": str(fila["nombre"]),
                "precio": float(fila["precio"]),   # Decimal -> float
                "stock": int(fila["stock"]),
            })
        return filas


class ExportadorTXT(Exportador):
    def exportar(self, datos, ruta_archivo):
        with open(ruta_archivo, "w", encoding="utf-8") as file:
            file.write("--- REPORTE DE PRODUCTOS ---\n")
            for p in self._normalizar(datos):
                file.write(
                    f"ID: {p['id_producto']} | Nombre: {p['nombre']} | "
                    f"Precio: ${p['precio']:.2f} | Stock: {p['stock']}\n"
                )
        print(f"Archivo TXT generado en: {ruta_archivo}")


class ExportadorCSV(Exportador):
    def exportar(self, datos, ruta_archivo):
        with open(ruta_archivo, "w", newline="", encoding="utf-8-sig") as file:
            escritor = csv.writer(file)
            escritor.writerow(["ID", "Nombre", "Precio", "Stock"])
            for p in self._normalizar(datos):
                escritor.writerow([p["id_producto"], p["nombre"], f"{p['precio']:.2f}", p["stock"]])
        print(f"Archivo CSV generado en: {ruta_archivo}")


class ExportadorJSON(Exportador):
    def exportar(self, datos, ruta_archivo):
        with open(ruta_archivo, "w", encoding="utf-8") as file:
            json.dump(self._normalizar(datos), file, ensure_ascii=False, indent=4)
        print(f"Archivo JSON generado en: {ruta_archivo}")


class ExportadorPDF(Exportador):
    @staticmethod
    def _seguro(texto):
        """fpdf clásico solo admite latin-1 (acentos y ñ sí; emojis o € no)."""
        return texto.encode("latin-1", "replace").decode("latin-1")

    def exportar(self, datos, ruta_archivo):
        pdf = FPDF()
        pdf.add_page()

        # Título
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, txt="Reporte de Inventario de Productos", ln=True, align="C")
        pdf.ln(10)

        # Encabezados de tabla
        pdf.set_font("Arial", "B", 12)
        pdf.cell(20, 10, txt="ID", border=1, align="C")
        pdf.cell(90, 10, txt="Nombre", border=1)
        pdf.cell(40, 10, txt="Precio", border=1, align="R")
        pdf.cell(40, 10, txt="Stock", border=1, ln=True, align="R")

        # Cuerpo
        pdf.set_font("Arial", size=12)
        for p in self._normalizar(datos):
            pdf.cell(20, 10, txt=str(p["id_producto"]), border=1, align="C")
            pdf.cell(90, 10, txt=self._seguro(p["nombre"]), border=1)
            pdf.cell(40, 10, txt=f"${p['precio']:.2f}", border=1, align="R")
            pdf.cell(40, 10, txt=str(p["stock"]), border=1, ln=True, align="R")

        pdf.output(ruta_archivo)
        print(f"Archivo PDF generado en: {ruta_archivo}")
