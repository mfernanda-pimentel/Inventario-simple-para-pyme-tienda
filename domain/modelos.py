from enum import Enum
from datetime import datetime

class Rol(Enum):
    ADMINISTRADOR = "Administrador"
    VENDEDOR = "Vendedor"
    ENCARGADO_COMPRAS = "Encargado de compras"

class Usuario:
    def __init__(self, nombre: str, rol: Rol):
        self.nombre = nombre
        self.rol = rol

class EstadoProducto(Enum):
    NORMAL = "Normal"
    CRITICO = "Crítico"
    AGOTADO = "Agotado"

class Producto:
    def __init__(self, codigo: str, nombre: str, categoria: str, existencia: int, stock_minimo: int, stock_optimo: int):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.existencia = existencia
        self.stock_minimo = stock_minimo
        self.stock_optimo = stock_optimo
        self.estado = EstadoProducto.NORMAL
        self.reevaluar_estado()

    def reevaluar_estado(self):
        if self.existencia == 0:
            self.estado = EstadoProducto.AGOTADO
        elif self.existencia <= self.stock_minimo:
            self.estado = EstadoProducto.CRITICO
        else:
            self.estado = EstadoProducto.NORMAL

class Alerta:
    def __init__(self, producto: Producto):
        self.producto = producto
        self.fecha = datetime.now()
        self.estado_producto = producto.estado
        self.canal_envio = ""
        self.resultado = "Pendiente"
