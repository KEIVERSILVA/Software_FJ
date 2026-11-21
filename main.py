from Modelos.cliente import Cliente
from Modelos.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from Modelos.reserva import Reserva
from Modelos.excepciones import ErrorSoftwareFJ, logger_sistema


class SistemaSoftwareFJ:
    # Gestiona las listas en memoria de clientes, servicios y reservas
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente: Cliente) -> None:
        self.clientes.append(cliente)
        logger_sistema.info(f"Cliente registrado: {cliente.id_entidad} - {cliente.nombre}")

    def registrar_servicio(self, servicio) -> None:
        self.servicios.append(servicio)
        logger_sistema.info(f"Servicio registrado: {servicio.id_entidad} - {servicio.nombre}")

    def registrar_reserva(self, reserva: Reserva) -> None:
        self.reservas.append(reserva)


def ejecutar_simulacion():
    sistema = SistemaSoftwareFJ()
    print("=== INICIANDO SIMULACION SISTEMA SOFTWARE FJ ===\n")

    # 1. Registro valido de cliente (try / except / else)
    try:
        c1 = Cliente("C001", "Laura Gomez", "laura@correo.com", "3001234567")
    except ErrorSoftwareFJ as e:
        print(f"[Op 1 - Error] {e}")
    else:
        sistema.registrar_cliente(c1)
        print(f"[Op 1 - OK] {c1.resumen()}")

    # 2. Registro valido de segundo cliente
    try:
        c2 = Cliente("C002", "Carlos Ruiz", "carlos@correo.com", "3109876543")
        sistema.registrar_cliente(c2)
        print(f"[Op 2 - OK] {c2.resumen()}")
    except ErrorSoftwareFJ as e:
        print(f"[Op 2 - Error] {e}")

    # 3. Registro invalido de cliente: correo mal escrito y telefono corto
    try:
        c_malo = Cliente("C003", "Pedro Perez", "correo_sin_arroba", "123")
        sistema.registrar_cliente(c_malo)
    except ErrorSoftwareFJ as e:
        print(f"[Op 3 - Controlado] Error al registrar cliente: {e}")

    # 4. Creacion valida de servicios especializados (polimorfismo)
    try:
        s1 = ReservaSala("S001", "Sala Juntas Norte", 50000, capacidad=10)
        s2 = AlquilerEquipo("S002", "Portatil Gamer", 40000, modelo="ASUS ROG")
        s3 = AsesoriaEspecializada("S003", "Consultoria Cloud", 80000, especialidad="AWS")
        sistema.registrar_servicio(s1)
        sistema.registrar_servicio(s2)
        sistema.registrar_servicio(s3)
        print("[Op 4 - OK] 3 servicios creados correctamente.")
    except ErrorSoftwareFJ as e:
        print(f"[Op 4 - Error] {e}")

    # 5. Creacion invalida de servicio: tarifa negativa
    try:
        s_malo = ReservaSala("S004", "Sala Fantasma", -20000, capacidad=5)
        sistema.registrar_servicio(s_malo)
    except ErrorSoftwareFJ as e:
        print(f"[Op 5 - Controlado] Error al crear servicio: {e}")

    # 6. Reserva exitosa con descuento e impuesto (try / except / else / finally)
    r1 = None
    try:
        r1 = Reserva("R001", c1, s1, duracion=6, descuento_pct=10, impuesto_pct=19)
    except ErrorSoftwareFJ as e:
        print(f"[Op 6 - Error] {e}")
    else:
        sistema.registrar_reserva(r1)
        print(f"[Op 6 - OK] {r1}")
    finally:
        print("[Op 6 - Info] Revision de creacion de reserva R001 finalizada.")

    # 7. Confirmar y procesar reserva R001 correctamente
    try:
        r1.confirmar()
        total_pagado = r1.procesar()
        print(f"[Op 7 - OK] Reserva R001 procesada. Total: ${total_pagado:,.2f}")
    except ErrorSoftwareFJ as e:
        print(f"[Op 7 - Error] {e}")

    # 8. Operacion no permitida: intentar cancelar una reserva ya procesada
    try:
        r1.cancelar()
    except ErrorSoftwareFJ as e:
        print(f"[Op 8 - Controlado] {e}")

    # 9. Reserva fallida: excede limite de horas de una sala (maximo 12)
    try:
        r_mala = Reserva("R002", c2, s1, duracion=15)
        sistema.registrar_reserva(r_mala)
    except ErrorSoftwareFJ as e:
        print(f"[Op 9 - Controlado] Reserva rechazada: {e}")

    # 10. Reserva exitosa de equipo y posterior cancelacion valida
    try:
        r3 = Reserva("R003", c2, s2, duracion=3, descuento_pct=5)
        sistema.registrar_reserva(r3)
        r3.cancelar()
        print(f"[Op 10 - OK] Reserva R003 creada y cancelada correctamente. Estado: {r3.estado}")
    except ErrorSoftwareFJ as e:
        print(f"[Op 10 - Error] {e}")

    # 11. Reserva fallida: servicio marcado como no disponible
    try:
        s3.cambiar_disponibilidad(False)
        r4 = Reserva("R004", c1, s3, duracion=2)
        sistema.registrar_reserva(r4)
    except ErrorSoftwareFJ as e:
        print(f"[Op 11 - Controlado] Servicio bloqueado: {e}")

    # 12. Calculo inconsistente: descuento mayor al permitido (120%)
    try:
        s2.calcular_costo(duracion=2, descuento_pct=120)
    except ErrorSoftwareFJ as e:
        print(f"[Op 12 - Controlado] Calculo rechazado: {e}")

    # Resumen final en memoria
    print("\n=== RESUMEN FINAL DEL SISTEMA ===")
    print(f"Clientes activos en memoria: {len(sistema.clientes)}")
    print(f"Servicios registrados en memoria: {len(sistema.servicios)}")
    print(f"Reservas registradas en memoria: {len(sistema.reservas)}")
    for res in sistema.reservas:
        print(f"  -> {res}")
    print("\nLogs guardados en 'sistema_software_fj.log'.")


if __name__ == "__main__":
    ejecutar_simulacion()