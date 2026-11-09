"""Modelo: operaciones sobre la tabla products."""
from models.database_connection import Database_connection

TABLA = '"Database_OOP".products'


class ProductModel:

    def __init__(self):
        self.conexion_db = Database_connection()

    def obtener_todos(self):
        """Devuelve la lista de productos como diccionarios
        ([] si no hay filas, None si hubo error)."""
        return self.conexion_db.ejecutar_consulta(
            f"""
            SELECT id_producto, nombre, precio, stock
            FROM {TABLA}
            ORDER BY id_producto
            """
        )
