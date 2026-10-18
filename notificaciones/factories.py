from abc import ABC, abstractmethod
from domain.modelos import Alerta

class Notificacion(ABC):
    @abstractmethod
    def enviar(self, alerta: Alerta) -> bool:
        pass

class NotificacionCorreo(Notificacion):
    def enviar(self, alerta: Alerta) -> bool:
        alerta.canal_envio = "Correo electrónico"
        return True

class NotificacionSMS(Notificacion):
    def enviar(self, alerta: Alerta) -> bool:
        alerta.canal_envio = "SMS"
        return True

class NotificacionPanel(Notificacion):
    def enviar(self, alerta: Alerta) -> bool:
        alerta.canal_envio = "Panel de control"
        return True

class NotificadorAlertas(ABC):
    @abstractmethod
    def crear_notificacion(self) -> Notificacion:
        pass

    def despachar(self, alerta: Alerta) -> bool:
        notificador = self.crear_notificacion()
        exito = notificador.enviar(alerta)
        alerta.resultado = "exitoso" if exito else "fallido"
        return exito

class NotificadorCorreo(NotificadorAlertas):
    def crear_notificacion(self) -> Notificacion:
        return NotificacionCorreo()

class NotificadorSMS(NotificadorAlertas):
    def crear_notificacion(self) -> Notificacion:
        return NotificacionSMS()

class NotificadorPanel(NotificadorAlertas):
    def crear_notificacion(self) -> Notificacion:
        return NotificacionPanel()
