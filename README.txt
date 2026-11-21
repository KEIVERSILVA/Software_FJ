====================================================================
SISTEMA INTEGRAL DE GESTION DE CLIENTES, SERVICIOS Y RESERVAS
Empresa: Software FJ
Curso: Programacion (Codigo: 213023) - UNAD
Fase 4 - Programacion Orientada a Objetos y Manejo de Excepciones
====================================================================

1. DESCRIPCION DEL PROYECTO
Aplicacion de consola desarrollada en Python bajo el paradigma de Programacion Orientada a Objetos (POO). Permite gestionar clientes, servicios (salas, equipos y asesorias) y reservas en memoria sin uso de bases de datos, garantizando estabilidad ante errores mediante excepciones personalizadas y registro de eventos en archivo de logs.

2. ESTRUCTURA DEL PROYECTO
Software_FJ/
├── main.py                      # Ejecucion principal y simulacion de 12 operaciones
├── README.txt                   # Documentacion general del proyecto
├── sistema_software_fj.log      # Archivo generado con el registro de eventos y errores
└── Modelos/
    ├── cliente.py               # Clase abstracta EntidadBase y clase Cliente
    ├── servicio.py              # Clase abstracta Servicio y 3 servicios especializados
    ├── reserva.py               # Clase Reserva (creacion, confirmacion, proceso y cancelacion)
    └── excepciones.py           # Excepciones personalizadas y configuracion del logger

3. CONCEPTOS APLICADOS
- Abstraccion y Herencia: Clases abstractas EntidadBase y Servicio, heredadas por Cliente, ReservaSala, AlquilerEquipo y AsesoriaEspecializada.
- Polimorfismo y Sobrescritura: Implementacion personalizada de calcular_costo(), validar_parametros() y describir() en cada tipo de servicio.
- Encapsulacion: Uso de atributos privados y propiedades (@property y setters) con validaciones estrictas.
- Manejo Avanzado de Excepciones: Excepciones propias (DatoInvalidoError, ParametroFaltanteError, OperacionNoPermitidaError, ServicioNoDisponibleError, ReservaInvalidaError, CalculoInconsistenteError), bloques try/except/else/finally y encadenamiento (raise ... from ...).

4. REQUISITOS Y EJECUCION
- Requisitos: Python 3.10 o superior (solo librerias estandar).
- Ejecucion desde la carpeta raiz del proyecto:
  python main.py