from abc import ABC, abstractmethod
from datetime import datetime
from domain.modelos import Producto, Usuario

class Movimiento(ABC):
    def __init__(self, cantidad: int, usuario: Usuario, detalle: str):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")
        self.cantidad = cantidad
        self.usuario = usuario
        self.detalle = detalle
        self.fecha = datetime.now()

    @abstractmethod
    def aplicar(self, producto: Producto):
        pass

class Entrada(Movimiento):
    def aplicar(self, producto: Producto):
        producto.existencia += self.cantidad
        producto.reevaluar_estado()

class Salida(Movimiento):
    def aplicar(self, producto: Producto):
        if self.cantidad > producto.existencia:
            raise ValueError("La cantidad supera el stock disponible.")
        producto.existencia -= self.cantidad
        producto.reevaluar_estado()

class RegistradorMovimiento(ABC):
    @abstractmethod
    def crear_movimiento(self, cantidad: int, usuario: Usuario, detalle: str) -> Movimiento:
        pass

class RegistradorEntrada(RegistradorMovimiento):
    def crear_movimiento(self, cantidad: int, usuario: Usuario, detalle: str) -> Movimiento:
        return Entrada(cantidad, usuario, detalle)

class RegistradorSalida(RegistradorMovimiento):
    def crear_movimiento(self, cantidad: int, usuario: Usuario, detalle: str) -> Movimiento:
        return Salida(cantidad, usuario, detalle)
