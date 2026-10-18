from typing import Optional
from domain.modelos import Producto

class ProductoBuilder:
    def __init__(self, producto_base: Optional[Producto] = None):
        if producto_base:
            self._codigo = producto_base.codigo
            self._nombre = producto_base.nombre
            self._categoria = producto_base.categoria
            self._existencia = producto_base.existencia
            self._stock_minimo = producto_base.stock_minimo
            self._stock_optimo = producto_base.stock_optimo
        else:
            self._codigo = ""
            self._nombre = ""
            self._categoria = "General"
            self._existencia = 0
            self._stock_minimo = 0
            self._stock_optimo = 1

    def con_codigo(self, codigo: str):
        self._codigo = codigo
        return self

    def con_nombre(self, nombre: str):
        self._nombre = nombre
        return self

    def con_categoria(self, categoria: str):
        self._categoria = categoria
        return self

    def con_existencia(self, existencia: int):
        self._existencia = existencia
        return self

    def con_stock_minimo(self, stock_minimo: int):
        self._stock_minimo = stock_minimo
        return self

    def con_stock_optimo(self, stock_optimo: int):
        self._stock_optimo = stock_optimo
        return self

    def build(self) -> Producto:
        if self._stock_minimo < 0:
            raise ValueError("El stock mínimo debe ser mayor o igual a cero.")
        if self._stock_optimo <= self._stock_minimo:
            raise ValueError("El stock óptimo debe ser mayor que el mínimo.")
        if self._existencia < 0:
            raise ValueError("El stock no puede ser negativo.")
        
        return Producto(
            codigo=self._codigo,
            nombre=self._nombre,
            categoria=self._categoria,
            existencia=self._existencia,
            stock_minimo=self._stock_minimo,
            stock_optimo=self._stock_optimo
        )
