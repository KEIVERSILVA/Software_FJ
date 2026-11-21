from abc import ABC, abstractmethod
from Modelos.cliente import EntidadBase
from Modelos.excepciones import (
    CalculoInconsistenteError,
    DatoInvalidoError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
)


class Servicio(EntidadBase):
    # Clase base abstracta para todos los servicios
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio, activo=disponible)
        if not nombre or not nombre.strip():
            raise ParametroFaltanteError("Falta el nombre del servicio.")
        if tarifa_base is None or tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor a cero.")

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    def cambiar_disponibilidad(self, estado: bool) -> None:
        # Cambia si el servicio se puede reservar o no
        self._disponible = bool(estado)

    def validar_parametros(self, duracion: int) -> None:
        # Verifica que el servicio esté disponible y la duración sea válida
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._nombre}' no está disponible.")
        if not isinstance(duracion, int) or duracion <= 0:
            raise DatoInvalidoError("La duración debe ser un número entero mayor a cero.")

    def calcular_costo(
        self,
        duracion: int,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
        extra: float = 0.0,
    ) -> float:
        # Calcula el costo total con descuento e impuesto opcionales
        self.validar_parametros(duracion)

        if descuento_pct < 0 or descuento_pct >= 100:
            raise CalculoInconsistenteError("El descuento debe estar entre 0 y 99.")
        if impuesto_pct < 0:
            raise CalculoInconsistenteError("El impuesto no puede ser negativo.")
        if extra < 0:
            raise CalculoInconsistenteError("El valor extra no puede ser negativo.")

        subtotal = (self._tarifa_base * duracion) + extra
        con_descuento = subtotal * (1 - descuento_pct / 100)
        total = con_descuento * (1 + impuesto_pct / 100)

        if total < 0:
            raise CalculoInconsistenteError("El total calculado no es válido.")

        return round(total, 2)

    @abstractmethod
    def describir(self) -> str:
        pass

    def resumen(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Servicio [{self._id_entidad}] {self._nombre} - Base: ${self._tarifa_base:,.2f} ({estado})"


class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor a cero.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion: int) -> None:
        super().validar_parametros(duracion)
        if duracion > 12:
            raise DatoInvalidoError("Una sala no se puede reservar por más de 12 horas seguidas.")

    def calcular_costo(self, duracion: int, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        # Si dura más de 4 horas, suma un recargo pequeño de aseo/logística
        recargo = 15000.0 if duracion > 4 else 0.0
        return super().calcular_costo(duracion, descuento_pct, impuesto_pct, extra=recargo)

    def describir(self) -> str:
        return f"Sala '{self._nombre}' (capacidad: {self.capacidad} personas)."


class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, modelo: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not modelo or not modelo.strip():
            raise ParametroFaltanteError("Falta el modelo del equipo.")
        self.modelo = modelo.strip()

    def validar_parametros(self, duracion: int) -> None:
        super().validar_parametros(duracion)
        if duracion > 30:
            raise DatoInvalidoError("El alquiler de equipo no puede superar los 30 días.")

    def calcular_costo(self, duracion: int, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        # Aplica seguro básico por día alquilado
        seguro = 5000.0 * duracion
        return super().calcular_costo(duracion, descuento_pct, impuesto_pct, extra=seguro)

    def describir(self) -> str:
        return f"Equipo '{self._nombre}' modelo '{self.modelo}'."


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not especialidad or not especialidad.strip():
            raise ParametroFaltanteError("Falta la especialidad de la asesoría.")
        self.especialidad = especialidad.strip()

    def calcular_costo(self, duracion: int, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        return super().calcular_costo(duracion, descuento_pct, impuesto_pct, extra=0.0)

    def describir(self) -> str:
        return f"Asesoría '{self._nombre}' en {self.especialidad}."