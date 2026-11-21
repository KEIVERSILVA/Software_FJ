from Modelos.cliente import Cliente
from Modelos.servicio import Servicio
from Modelos.excepciones import (
    CalculoInconsistenteError,
    DatoInvalidoError,
    ErrorSoftwareFJ,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    logger_sistema,
)


class Reserva:
    # Gestiona una reserva uniendo cliente, servicio, duracion y estado
    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: int,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
    ):
        if not id_reserva or not isinstance(id_reserva, str) or not id_reserva.strip():
            raise ParametroFaltanteError("El ID de la reserva es obligatorio.")
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Debe asignarse un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Debe asignarse un servicio válido.")
        if not cliente.activo:
            raise ReservaInvalidaError("No se puede crear una reserva para un cliente inactivo.")

        try:
            # Valida parametros y calcula el costo inicial
            costo = servicio.calcular_costo(
                duracion,
                descuento_pct=descuento_pct,
                impuesto_pct=impuesto_pct,
            )
        except ErrorSoftwareFJ as exc:
            raise ReservaInvalidaError(
                f"No se pudo crear la reserva '{id_reserva.strip().upper()}': {exc.mensaje}"
            ) from exc

        self._id_reserva = id_reserva.strip().upper()
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._descuento_pct = descuento_pct
        self._impuesto_pct = impuesto_pct
        self._total = costo
        self._estado = "PENDIENTE"
        logger_sistema.info(f"Reserva {self._id_reserva} creada en estado PENDIENTE.")

    @property
    def id_reserva(self) -> str:
        return self._id_reserva

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def total(self) -> float:
        return self._total

    def confirmar(self) -> None:
        # Confirma la reserva solo si esta pendiente
        if self._estado == "CANCELADA":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva {self._id_reserva} porque está cancelada."
            )
        if self._estado == "PROCESADA":
            raise OperacionNoPermitidaError(
                f"La reserva {self._id_reserva} ya fue procesada."
            )
        if self._estado == "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"La reserva {self._id_reserva} ya está confirmada."
            )

        self._estado = "CONFIRMADA"
        logger_sistema.info(f"Reserva {self._id_reserva} confirmada.")

    def procesar(self) -> float:
        # Procesa la reserva confirmada y recalcula el total final
        if self._estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden procesar reservas confirmadas. Estado actual: {self._estado}."
            )

        try:
            self._total = self._servicio.calcular_costo(
                self._duracion,
                descuento_pct=self._descuento_pct,
                impuesto_pct=self._impuesto_pct,
            )
            if self._total <= 0:
                raise CalculoInconsistenteError("El total de la reserva debe ser mayor a cero.")
        except ErrorSoftwareFJ as exc:
            raise ReservaInvalidaError(
                f"Error al procesar la reserva {self._id_reserva}."
            ) from exc

        self._estado = "PROCESADA"
        logger_sistema.info(f"Reserva {self._id_reserva} procesada por ${self._total:,.2f}.")
        return self._total

    def cancelar(self) -> None:
        # Cancela la reserva si aun no ha sido procesada
        if self._estado == "PROCESADA":
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva {self._id_reserva} porque ya fue procesada."
            )
        if self._estado == "CANCELADA":
            raise OperacionNoPermitidaError(
                f"La reserva {self._id_reserva} ya estaba cancelada."
            )

        self._estado = "CANCELADA"
        logger_sistema.info(f"Reserva {self._id_reserva} cancelada.")

    def __str__(self) -> str:
        return (
            f"Reserva [{self._id_reserva}] | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} | "
            f"Total: ${self._total:,.2f} | Estado: {self._estado}"
        )