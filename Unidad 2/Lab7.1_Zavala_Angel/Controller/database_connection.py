import psycopg2
from psycopg2.extras import RealDictCursor
from Controller.config import DB_CONFIG

class Database_connection:
    def __init__(self):
        self.config = DB_CONFIG

    def obtener_conexion(self):
        try:
            conexion = psycopg2.connect(**self.config)
            return conexion
        except Exception as e:
            print(f"Error al conectar con PostgreSQL: {e}")
            return None

    def ejecutar_consulta(self, query, params=()):
        conexion = self.obtener_conexion()
        if not conexion:
            return None

        cursor = conexion.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            return resultados
        except Exception as e:
            print(f"Error en la consulta SQL: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()