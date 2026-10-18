# Patrón Singleton para configuración global
class ConfiguracionSistema:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConfiguracionSistema, cls).__new__(cls)
            cls._instancia.canal_notificacion_defecto = "CORREO"
            cls._instancia.servidor_correo = "smtp.tienda.com"
        return cls._instancia
