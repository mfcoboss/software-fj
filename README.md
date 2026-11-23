# Software FJ — Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de la **Fase 4 – Componente práctico: Prácticas simuladas** del curso **Programación (213023)** de la UNAD.

Aplicación en Python orientada a objetos, **sin base de datos**, que gestiona clientes, servicios (salas, alquiler de equipos y asesorías) y reservas. El foco es el **manejo robusto de excepciones**: ningún error detiene la ejecución; todos quedan registrados en un archivo de logs.

## Cómo ejecutar

Requiere Python 3.10 o superior. No usa librerías externas.

```bash
python main.py
```

El programa simula 30 operaciones (válidas e inválidas) y escribe los eventos en `logs/software_fj.log`.

## Estructura

```
software_fj/
├── main.py                 # Simulación de operaciones (punto de entrada)
├── sistema/
│   ├── entidad.py          # Clase abstracta Entidad (id, fecha, describir, validar)
│   ├── cliente.py          # Cliente con encapsulación y validaciones
│   ├── servicios.py        # Servicio (abstracta) + ReservaSala, AlquilerEquipo, Asesoria
│   ├── reserva.py          # Reserva: confirmar, cancelar, procesar
│   ├── gestor.py           # Listas internas de clientes, servicios y reservas
│   ├── excepciones.py      # Jerarquía de excepciones personalizadas
│   └── logger.py           # Configuración del archivo de logs
└── logs/                   # Se crea al ejecutar
```

## Requisitos del Anexo 3 y dónde se cumplen

| Requisito | Implementación |
|---|---|
| Clase abstracta de entidades generales | `Entidad` (ABC) en `entidad.py` |
| Cliente con validaciones y encapsulación | Atributos privados `__nombre`, `__documento`… con `@property` y setters que validan |
| Servicio abstracto + 3 especializados | `Servicio` → `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| Polimorfismo y métodos sobrescritos | `_costo_base()`, `validar_parametros()`, `describir()` en cada subclase |
| Métodos sobrecargados | `calcular_costo(d)`, `calcular_costo(d, impuesto)`, `calcular_costo(d, impuesto, descuento)` |
| Reserva con confirmación, cancelación y procesamiento | `Reserva.confirmar()`, `cancelar()`, `procesar()` |
| Excepciones personalizadas | 8 clases en `excepciones.py`, todas heredan de `SoftwareFJError` |
| `try/except` | `Reserva.__init__`, `ejecutar_operacion()` |
| `try/except/else/finally` | `Reserva.procesar()` y `ejecutar_operacion()` |
| Encadenamiento de excepciones | `raise ReservaInvalidaError(...) from e` |
| Archivo de logs | `logs/software_fj.log` |
| Mínimo 10 operaciones | 30 operaciones en `main.py` |
| Sin base de datos | Toda la información vive en listas dentro de `GestorSoftwareFJ` |

## Códigos de error

| Código | Excepción | Cuándo ocurre |
|---|---|---|
| FJ-100 | `DatoInvalidoError` | Formato o rango inválido |
| FJ-101 | `ParametroFaltanteError` | Falta un dato obligatorio |
| FJ-200 | `ClienteDuplicadoError` | Documento ya registrado |
| FJ-300 | `ServicioNoDisponibleError` | Servicio inexistente o deshabilitado |
| FJ-400 | `ReservaInvalidaError` | Datos de reserva incorrectos |
| FJ-401 | `OperacionNoPermitidaError` | Transición de estado no válida |
| FJ-500 | `CalculoInconsistenteError` | Costo calculado incoherente |

## Ciclo de vida de una reserva

```
PENDIENTE ──confirmar──► CONFIRMADA ──procesar──► PROCESADA
    │                         │
    └────────cancelar─────────┴──► CANCELADA
```
