from domain.modelos import Usuario, Rol, EstadoProducto
from domain.builders import ProductoBuilder
from movimientos.factories import RegistradorSalida, RegistradorEntrada
from servicios.servicio_inventario import ServicioInventario

def ejecutar_pruebas():
    admin = Usuario("Carlos (Admin)", Rol.ADMINISTRADOR)
    vendedor = Usuario("Ana (Vendedora)", Rol.VENDEDOR)
    compras = Usuario("Luis (Compras)", Rol.ENCARGADO_COMPRAS)

    servicio = ServicioInventario()

    print("--- 1. Pruebas de Registro ---")
    builder = ProductoBuilder().con_codigo("CAF-500").con_nombre("Café").con_existencia(20).con_stock_minimo(5).con_stock_optimo(40)
    prod = servicio.registrar_producto(admin, builder)
    print(f"Producto creado: {prod.nombre}, Estado: {prod.estado.value}")

    print("\n--- 2. Prueba de Salida (Entra en estado Crítico) ---")
    builder_leche = ProductoBuilder().con_codigo("LEC-100").con_nombre("Leche").con_existencia(6).con_stock_minimo(5).con_stock_optimo(30)
    servicio.registrar_producto(admin, builder_leche)
    
    servicio.registrar_movimiento(vendedor, "LEC-100", 2, RegistradorSalida(), "Venta")
    print(f"Estado tras venta: {servicio.productos['LEC-100'].estado.value}")

    print("\n--- 3. Generar Reporte ---")
    reporte = servicio.generar_reporte_reabastecimiento()
    print(reporte.mostrar())

if __name__ == "__main__":
    ejecutar_pruebas()
