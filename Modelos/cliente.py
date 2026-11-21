from abc import ABC, abstractmethod
import re
from Modelos.excepciones import DatoInvalidoError, ParametroFaltanteError


class EntidadBase(ABC):
    """Clase abstracta general para entidades del sistema Software FJ."""

    def __init__(self, id_entidad: str, activo: bool = True):
        if not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ParametroFaltanteError(
                "El identificador de la entidad es obligatorio.",
                detalles={"campo": "id_entidad", "valor": id_entidad}
            )
        self._id_entidad = id_entidad.strip().upper()
        self._activo = bool(activo)

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @property
    def activo(self) -> bool:
        return self._activo

    def desactivar(self) -> None:
        self._activo = False

    def activar(self) -> None:
        self._activo = True

    @abstractmethod
    def resumen(self) -> str:
        """Retorna un resumen legible de la entidad."""
        pass


class Cliente(EntidadBase):
    """Representa un cliente de Software FJ con encapsulación y validaciones estrictas."""

    def __init__(
        self,
        id_cliente: str,
        nombre: str,
        correo: str,
        telefono: str,
        activo: bool = True
    ):
        super().__init__(id_cliente, activo=activo)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError(
                "El nombre del cliente no puede estar vacío.",
                detalles={"campo": "nombre", "cliente_id": self._id_entidad}
            )
        limpio = " ".join(valor.strip().split())
        if len(limpio) < 2 or not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", limpio):
            raise DatoInvalidoError(
                "El nombre del cliente contiene caracteres inválidos o es demasiado corto.",
                detalles={"campo": "nombre", "valor": valor}
            )
        self._nombre = limpio

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError(
                "El correo electrónico del cliente es obligatorio.",
                detalles={"campo": "correo", "cliente_id": self._id_entidad}
            )
        limpio = valor.strip().lower()
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", limpio):
            raise DatoInvalidoError(
                "El formato del correo electrónico no es válido.",
                detalles={"campo": "correo", "valor": valor}
            )
        self._correo = limpio

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError(
                "El teléfono del cliente es obligatorio.",
                detalles={"campo": "telefono", "cliente_id": self._id_entidad}
            )
        limpio = re.sub(r"[\s\-\(\)]", "", valor.strip())
        if not limpio.isdigit() or not (7 <= len(limpio) <= 15):
            raise DatoInvalidoError(
                "El teléfono debe contener entre 7 y 15 dígitos numéricos.",
                detalles={"campo": "telefono", "valor": valor}
            )
        self._telefono = limpio

    def resumen(self) -> str:
        estado = "Activo" if self._activo else "Inactivo"
        return (
            f"Cliente [{self._id_entidad}] - {self._nombre} | "
            f"Correo: {self._correo} | Tel: {self._telefono} | Estado: {estado}"
        )

    def __str__(self) -> str:
        return self.resumen()