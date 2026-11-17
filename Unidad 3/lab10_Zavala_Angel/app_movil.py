"""Lab 10 - Lógica de backend para una aplicación móvil (POO)."""

class SuscripcionExpiradaError(Exception):
    """Se lanza al ejecutar una operación restringida sin membresía activa."""


class PuntosInsuficientesError(Exception):
    """Se lanza cuando una transacción excede el saldo de gemas disponible."""


class PerfilMovil:
    def __init__(self, username: str, gemas: int = 50,
                 racha_dias: int = 1, notificaciones_activas: bool = True):
        if gemas < 0:
            raise ValueError("Las gemas no pueden ser negativas.")
        self.username = username
        self.gemas = gemas
        self.racha_dias = racha_dias
        self.notificaciones_activas = notificaciones_activas

    def ganar_gemas(self, cantidad: int) -> int:
        """Suma gemas al saldo. La cantidad debe ser estrictamente positiva."""
        if cantidad <= 0:
            raise ValueError("La cantidad a ganar debe ser mayor que cero.")
        self.gemas += cantidad
        return self.gemas

    def gastar_gemas(self, cantidad: int) -> int:
        """Resta gemas del saldo tras verificar valor positivo y fondos."""
        if cantidad <= 0:
            raise ValueError("La cantidad a gastar debe ser mayor que cero.")
        if cantidad > self.gemas:
            raise PuntosInsuficientesError(
                f"Saldo insuficiente: tienes {self.gemas} y necesitas {cantidad}."
            )
        self.gemas -= cantidad
        return self.gemas


class PerfilPro(PerfilMovil):
    def __init__(self, username: str, meses_suscripcion: int, gemas: int = 50,
                 racha_dias: int = 1, notificaciones_activas: bool = True):
        if meses_suscripcion <= 0:
            raise ValueError("Los meses de suscripción deben ser mayores que cero.")
        super().__init__(username, gemas, racha_dias, notificaciones_activas)
        self.meses_suscripcion = meses_suscripcion
        self.es_pro = True

    def descargar_contenido_offline(self) -> str:
        """Confirma la descarga si la suscripción sigue vigente.

        Si los meses llegaron a 0, desactiva es_pro y lanza
        SuscripcionExpiradaError.
        """
        if self.meses_suscripcion <= 0:
            self.es_pro = False
            raise SuscripcionExpiradaError(
                f"La suscripción de {self.username} ha expirado."
            )
        return f"Contenido offline descargado correctamente para {self.username}."
