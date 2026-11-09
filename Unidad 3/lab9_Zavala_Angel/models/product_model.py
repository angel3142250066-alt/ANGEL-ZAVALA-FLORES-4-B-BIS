"""Modelo: operaciones sobre la tabla products."""
import psycopg2

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

    def registrar_producto(self, nombre, precio, stock):
        """Inserta un producto. Devuelve 'ok' o 'error'."""
        conexion = self.conexion_db.obtener_conexion()

        if conexion is None:
            return "error"

        cursor = None

        try:
            cursor = conexion.cursor()
            cursor.execute(
                f"""
                INSERT INTO {TABLA} (nombre, precio, stock)
                VALUES (%s, %s, %s)
                """,
                (nombre, precio, stock)
            )
            conexion.commit()
            return "ok"

        except psycopg2.Error as error:
            conexion.rollback()
            print("Error al registrar producto:", error)
            return "error"

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()