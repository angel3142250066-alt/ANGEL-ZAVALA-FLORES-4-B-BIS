from exceptions import CantidadInvalida, StockInsuficiente

class Producto:
    def __init__(self, codigo, stock):
        self.codigo = codigo
        self.stock = stock
        
    def retirar(self, cantidad):
        # Validación de cantidad positiva
        if cantidad <= 0:
            raise CantidadInvalida("La cantidad a retirar debe ser mayor a cero.")
        
        # Validación de stock suficiente
        if cantidad > self.stock:
            raise StockInsuficiente("No hay suficiente stock disponible para este producto.")
        
        # Descuento del stock
        self.stock -= cantidad