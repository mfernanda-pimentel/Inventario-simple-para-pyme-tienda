from datetime import datetime
from typing import List
from domain.modelos import Producto, EstadoProducto

class ReporteReabastecimiento:
    def __init__(self):
        self.encabezado: str = ""
        self.lineas: List[str] = []
        self.resumen: str = ""

    def mostrar(self) -> str:
        if not self.lineas:
            return f"{self.encabezado}\nNo hay productos por reabastecer.\n{self.resumen}".strip()
        cuerpo = "\n".join(self.lineas)
        return f"{self.encabezado}\n{cuerpo}\n{self.resumen}".strip()

class ReporteBuilder:
    def __init__(self):
        self._reporte = ReporteReabastecimiento()

    def agregar_encabezado(self):
        self._reporte.encabezado = f"--- REPORTE DE REABASTECIMIENTO ({datetime.now().strftime('%Y-%m-%d')}) ---"
        return self

    def agregar_linea(self, producto: Producto):
        if producto.estado in [EstadoProducto.CRITICO, EstadoProducto.AGOTADO]:
            sugerido = producto.stock_optimo - producto.existencia
            linea = f"Producto: {producto.nombre} | Código: {producto.codigo} | Estado: {producto.estado.value} | Stock Actual: {producto.existencia} | Cantidad Sugerida: {sugerido}"
            self._reporte.lineas.append(linea)
        return self

    def agregar_resumen(self, total_criticos: int):
        self._reporte.resumen = f"Total productos a reabastecer: {total_criticos}"
        return self

    def build(self) -> ReporteReabastecimiento:
        return self._reporte
