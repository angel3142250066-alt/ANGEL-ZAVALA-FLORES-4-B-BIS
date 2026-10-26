"""Modelo: conexión genérica a PostgreSQL."""
import psycopg2
from psycopg2.extras import RealDictCursor

from config import DB_CONFIG


class Database_connection:
    def __init__(self):
        self.config = DB_CONFIG

    def obtener_conexion(self):
        """Devuelve una conexión nueva o None si falla."""
        try:
            return psycopg2.connect(**self.config)
        except Exception as e:
            print(f"Error al conectar con PostgreSQL: {e}")
            return None

    def ejecutar_consulta(self, query, params=()):
        """SELECT: devuelve lista de diccionarios ([] si no hay filas, None si hay error)."""
        conexion = self.obtener_conexion()
        if not conexion:
            return None

        cursor = conexion.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en la consulta SQL: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()

    def probar_conexion(self):
        """Prueba rápida: devuelve True si la conexión y un SELECT funcionan."""
        resultado = self.ejecutar_consulta("SELECT 1 AS ok")
        return bool(resultado) and resultado[0]["ok"] == 1


if __name__ == "__main__":
    # Ejecutar desde la raíz del proyecto:  python -m models.database_connection
    db = Database_connection()
    if db.probar_conexion():
        print("Conexión correcta con PostgreSQL")
        usuarios = db.ejecutar_consulta('SELECT id_user, username, nombre FROM "Database_OOP".users')
        print("Usuarios:", usuarios)
    else:
        print("No se pudo conectar. Revisa config.py")
