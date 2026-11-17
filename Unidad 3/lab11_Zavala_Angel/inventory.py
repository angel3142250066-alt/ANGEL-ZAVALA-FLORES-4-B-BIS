from products import Producto
from exceptions import ProductoNoEncontrado

class Inventario:
    def __init__(self):
        # Diccionario de productos: clave (código) -> valor (instancia de Producto)
        self.productos = {
            "P01": Producto("P01", 5),
            "P02": Producto("P02", 10),
            "P03": Producto("P03", 8)
        }
    
    def retirar(self, codigo, cantidad):
        # Validación de existencia en el diccionario
        if codigo not in self.productos:
            raise ProductoNoEncontrado(f"El producto con código '{codigo}' no existe.")
        
        # Delegación al objeto producto
        self.productos[codigo].retirar(cantidad)