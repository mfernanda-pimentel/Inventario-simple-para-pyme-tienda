from typing import List
from domain.modelos import Usuario, Rol, Producto, EstadoProducto, Alerta
from domain.builders import ProductoBuilder
from movimientos.factories import RegistradorMovimiento, RegistradorEntrada, RegistradorSalida
from notificaciones.factories import NotificadorCorreo
from reportes.builder_reporte import ReporteBuilder, ReporteReabastecimiento

class ServicioInventario:
    def __init__(self):
        self.productos = {}
        self.historial_alertas: List[Alerta] = []

    def registrar_producto(self, usuario: Usuario, builder: ProductoBuilder) -> Producto:
        if usuario.rol != Rol.ADMINISTRADOR:
            raise PermissionError("Solo el Administrador puede registrar o gestionar productos.")
        
        producto = builder.build()
        if producto.codigo in self.productos:
            raise ValueError(f"Ya existe un producto con código {producto.codigo}")
        
        self.productos[producto.codigo] = producto
        
        if producto.estado in [EstadoProducto.CRITICO, EstadoProducto.AGOTADO]:
            self._generar_alerta(producto)
            
        return producto

    def registrar_movimiento(self, usuario: Usuario, codigo: str, cantidad: int, registrador: RegistradorMovimiento, detalle: str):
        if isinstance(registrador, RegistradorEntrada) and usuario.rol not in [Rol.ADMINISTRADOR, Rol.ENCARGADO_COMPRAS]:
            raise PermissionError("El rol no tiene permisos para registrar entradas.")
        if isinstance(registrador, RegistradorSalida) and usuario.rol not in [Rol.ADMINISTRADOR, Rol.VENDEDOR]:
            raise PermissionError("El rol no tiene permisos para registrar salidas.")

        producto = self.productos.get(codigo)
        if not producto:
            raise ValueError("El producto no existe.")

        estado_previo = producto.estado
        movimiento = registrador.crear_movimiento(cantidad, usuario, detalle)
        movimiento.aplicar(producto)

        if estado_previo == EstadoProducto.NORMAL and producto.estado in [EstadoProducto.CRITICO, EstadoProducto.AGOTADO]:
            self._generar_alerta(producto)

    def _generar_alerta(self, producto: Producto):
        alerta = Alerta(producto)
        notificador = NotificadorCorreo()
        notificador.despachar(alerta)
        self.historial_alertas.append(alerta)

    def generar_reporte_reabastecimiento(self) -> ReporteReabastecimiento:
        builder = ReporteBuilder()
        builder.agregar_encabezado()
        
        criticos = [p for p in self.productos.values() if p.estado in [EstadoProducto.CRITICO, EstadoProducto.AGOTADO]]
        for prod in self.productos.values():
            builder.agregar_linea(prod)
            
        builder.agregar_resumen(len(criticos))
        return builder.build()
