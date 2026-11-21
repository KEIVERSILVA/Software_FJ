import logging
import os
from datetime import datetime


def configurar_logger(nombre_archivo: str = "sistema_software_fj.log") -> logging.Logger:
    """Configura y devuelve un logger que guarda eventos y errores en un archivo de texto."""
    logger = logging.getLogger("SoftwareFJLogger")
    logger.setLevel(logging.INFO)

    # Evita duplicar handlers si se llama más de una vez
    if not logger.handlers:
        ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_log = os.path.join(ruta_base, nombre_archivo)

        file_handler = logging.FileHandler(ruta_log, mode="a", encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


logger_sistema = configurar_logger()


class ErrorSoftwareFJ(Exception):
    """Excepción base del sistema de gestión de Software FJ."""

    def __init__(self, mensaje: str, codigo: str = "ERR_GENERAL", detalles: dict | None = None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo
        self.detalles = detalles or {}
        self.fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.registrar_en_log()

    def registrar_en_log(self) -> None:
        detalle_str = f" | Detalles: {self.detalles}" if self.detalles else ""
        logger_sistema.error(f"[{self.codigo}] {self.mensaje}{detalle_str}")

    def __str__(self) -> str:
        return f"[{self.codigo}] {self.mensaje}"


class DatoInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un dato ingresado no cumple el formato o regla esperada."""

    def __init__(self, mensaje: str, detalles: dict | None = None):
        super().__init__(mensaje, codigo="ERR_DATO_INVALIDO", detalles=detalles)


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un parámetro obligatorio o está vacío."""

    def __init__(self, mensaje: str, detalles: dict | None = None):
        super().__init__(mensaje, codigo="ERR_PARAMETRO_FALTANTE", detalles=detalles)


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta realizar una acción prohibida por el estado actual."""

    def __init__(self, mensaje: str, detalles: dict | None = None):
        super().__init__(mensaje, codigo="ERR_OPERACION_NO_PERMITIDA", detalles=detalles)


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando el servicio solicitado no está disponible."""

    def __init__(self, mensaje: str, detalles: dict | None = None):
        super().__init__(mensaje, codigo="ERR_SERVICIO_NO_DISPONIBLE", detalles=detalles)


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando hay un error en la creación, confirmación, procesamiento o cancelación de una reserva."""

    def __init__(self, mensaje: str, detalles: dict | None = None):
        super().__init__(mensaje, codigo="ERR_RESERVA_INVALIDA", detalles=detalles)


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando ocurre un error o inconsistencia en cálculos de costos, descuentos o impuestos."""

    def __init__(self, mensaje: str, detalles: dict | None = None):
        super().__init__(mensaje, codigo="ERR_CALCULO_INCONSISTENTE", detalles=detalles)