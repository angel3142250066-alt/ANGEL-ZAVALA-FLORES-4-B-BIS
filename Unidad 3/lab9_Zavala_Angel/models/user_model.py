"""Modelo: operaciones sobre la tabla users."""
import psycopg2

from models.database_connection import Database_connection

TABLA = '"Database_OOP".users'


class UserModel:

    def __init__(self):
        self.conexion_db = Database_connection()

    def registrar_usuario(self, nombre, email, password):
        """Devuelve 'ok', 'duplicado' o 'error'.
        El correo se guarda en la columna username."""
        conexion = self.conexion_db.obtener_conexion()

        if conexion is None:
            return "error"

        cursor = None

        try:
            cursor = conexion.cursor()

            consulta = f"""
                INSERT INTO {TABLA} (username, passw, nombre)
                VALUES (%s, %s, %s)
            """

            cursor.execute(consulta, (email, password, nombre))
            conexion.commit()

            return "ok"

        except psycopg2.errors.UniqueViolation:
            conexion.rollback()
            return "duplicado"

        except psycopg2.Error as error:
            conexion.rollback()
            print("Error al registrar usuario:", error)
            return "error"

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    def validar_usuario(self, email, password):
        """Devuelve (id_user, nombre) si las credenciales son correctas, si no None."""
        filas = self.conexion_db.ejecutar_consulta(
            f"""
            SELECT id_user, nombre
            FROM {TABLA}
            WHERE username = %s AND passw = %s
            """,
            (email, password)
        )

        if not filas:          # None (error) o [] (sin coincidencias)
            return None

        usuario = filas[0]
        return usuario["id_user"], usuario["nombre"]

    def cerrar(self):
        # Cada operación cierra su propia conexión.
        pass
