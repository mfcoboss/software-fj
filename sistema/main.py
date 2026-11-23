"""
main.py
-------
Simulación de operaciones del Sistema Integral de Gestión Software FJ.

Ejecuta más de 10 operaciones (válidas e inválidas). Cada una se aísla con
ejecutar_operacion(), de modo que un error NUNCA detiene el programa:
se informa en pantalla, se registra en logs/software_fj.log y se continúa.

Ejecutar:  python main.py
"""

from sistema.gestor import GestorSoftwareFJ
from sistema.servicios import ReservaSala, AlquilerEquipo, Asesoria
from sistema.excepciones import SoftwareFJError
from sistema.logger import obtener_logger, RUTA_LOG

log = obtener_logger()
# Contadores para el resumen final
resultados = {"exitosas": 0, "fallidas": 0}


def ejecutar_operacion(numero, descripcion, funcion):
    """Ejecuta una operación aislada y controla cualquier error que ocurra."""
    print(f"\n[{numero:02d}] {descripcion}")
    try:
        resultado = funcion()
    except SoftwareFJError as e:
        # Errores esperados del dominio: se registran como ERROR
        resultados["fallidas"] += 1
        causa = f" | causa: {e.__cause__}" if e.__cause__ else ""
        print(f"     ✗ {e}{causa}")
        log.error(f"Op {numero} '{descripcion}' -> {e}{causa}")
        return None
    except Exception as e:  # noqa: BLE001
        # Errores imprevistos: se registran con traza completa, pero el sistema sigue
        resultados["fallidas"] += 1
        print(f"     ✗ Error inesperado: {type(e).__name__}: {e}")
        log.exception(f"Op {numero} '{descripcion}' -> error inesperado")
        return None
    else:
        # Solo si no hubo excepción
        resultados["exitosas"] += 1
        print(f"     ✓ {resultado}")
        return resultado
    finally:
        # Siempre se ejecuta: marca el fin de la operación en el log
        log.debug(f"Op {numero} finalizada")


def main():
    log.info("===== Inicio de simulación Software FJ =====")
    g = GestorSoftwareFJ()
    n = iter(range(1, 100))  # Numerador automático de operaciones

    # ---------- CLIENTES ----------
    ana = ejecutar_operacion(next(n), "Registrar cliente válido (Ana Gómez)",
        lambda: g.registrar_cliente("Ana Gómez", "1012345678", "ana.gomez@correo.com", "3001234567"))
    luis = ejecutar_operacion(next(n), "Registrar cliente válido (Luis Pérez)",
        lambda: g.registrar_cliente("Luis Pérez", "80123456", "luis@empresa.co", "3109876543"))
    ejecutar_operacion(next(n), "Registrar cliente con email inválido",
        lambda: g.registrar_cliente("Carlos Ruiz", "52123456", "carlos-sin-arroba", "3201112233"))
    ejecutar_operacion(next(n), "Registrar cliente sin nombre (parámetro faltante)",
        lambda: g.registrar_cliente("", "52123499", "x@y.com", "3201112233"))
    ejecutar_operacion(next(n), "Registrar cliente con documento duplicado",
        lambda: g.registrar_cliente("Ana Duplicada", "1012345678", "otra@correo.com", "3001234500"))

    # ---------- SERVICIOS ----------
    ejecutar_operacion(next(n), "Crear servicio: Sala Andes (30 personas)",
        lambda: g.agregar_servicio(ReservaSala("Sala Andes", 80000, 30)))
    ejecutar_operacion(next(n), "Crear servicio: Alquiler de portátiles x5",
        lambda: g.agregar_servicio(AlquilerEquipo("Portátiles", 45000, 5)))
    ejecutar_operacion(next(n), "Crear servicio: Asesoría en ciberseguridad (experto)",
        lambda: g.agregar_servicio(Asesoria("Ciberseguridad", 120000, "experto")))
    ejecutar_operacion(next(n), "Crear servicio con tarifa negativa",
        lambda: g.agregar_servicio(ReservaSala("Sala Fantasma", -5000, 10)))
    ejecutar_operacion(next(n), "Crear asesoría con nivel inexistente",
        lambda: g.agregar_servicio(Asesoria("Cloud", 100000, "maestro")))
    proyector = ejecutar_operacion(next(n), "Crear servicio Proyector (luego se deshabilita)",
        lambda: g.agregar_servicio(AlquilerEquipo("Proyector", 60000, 1)))
    if proyector:
        proyector.cambiar_disponibilidad(False)

    # ---------- RESERVAS ----------
    r1 = ejecutar_operacion(next(n), "Reserva válida: Ana -> Sala Andes 4 h",
        lambda: g.crear_reserva(ana, "Sala Andes", 4))
    ejecutar_operacion(next(n), "Confirmar reserva de Ana", lambda: (r1.confirmar(), r1)[1])
    ejecutar_operacion(next(n), "Procesar reserva de Ana con IVA 19 % (sobrecarga 2 parámetros)",
        lambda: f"Total: ${r1.procesar(0.19):,.0f}")

    r2 = ejecutar_operacion(next(n), "Reserva válida: Luis -> Portátiles 10 días",
        lambda: g.crear_reserva(luis, "Portátiles", 10))
    ejecutar_operacion(next(n), "Confirmar y procesar con IVA + 15 % descuento (sobrecarga 3 parámetros)",
        lambda: (r2.confirmar(), f"Total: ${r2.procesar(0.19, 0.15):,.0f}")[1])

    ejecutar_operacion(next(n), "Reserva con duración fuera de rango (asesoría 20 h)",
        lambda: g.crear_reserva(luis, "Ciberseguridad", 20))
    ejecutar_operacion(next(n), "Reserva de servicio inexistente (Sala Pacífico)",
        lambda: g.crear_reserva(ana, "Sala Pacífico", 2))
    ejecutar_operacion(next(n), "Reserva de servicio no disponible (Proyector)",
        lambda: g.crear_reserva(ana, "Proyector", 2))
    ejecutar_operacion(next(n), "Reserva con cliente inválido (texto en vez de objeto)",
        lambda: g.crear_reserva("Pedro", "Sala Andes", 2))

    r3 = ejecutar_operacion(next(n), "Reserva válida: Ana -> Ciberseguridad 3 h",
        lambda: g.crear_reserva(ana, "Ciberseguridad", 3))
    ejecutar_operacion(next(n), "Cancelar reserva de asesoría", lambda: (r3.cancelar(), r3)[1])
    ejecutar_operacion(next(n), "Cancelar otra vez la misma reserva (operación no permitida)",
        lambda: r3.cancelar())
    ejecutar_operacion(next(n), "Procesar una reserva cancelada (operación no permitida)",
        lambda: r3.procesar())

    r4 = ejecutar_operacion(next(n), "Reserva válida: Luis -> Sala Andes 2 h",
        lambda: g.crear_reserva(luis, "Sala Andes", 2))
    ejecutar_operacion(next(n), "Procesar con descuento inválido de 150 %",
        lambda: (r4.confirmar(), r4.procesar(0.19, 1.5))[1])
    ejecutar_operacion(next(n), "Cálculo directo con costo base (sobrecarga 1 parámetro)",
        lambda: f"Costo base asesoría 2 h: ${g.buscar_servicio('Ciberseguridad').calcular_costo(2):,.0f}")
    ejecutar_operacion(next(n), "Reserva con tipo incorrecto en duración ('dos')",
        lambda: g.crear_reserva(ana, "Sala Andes", "dos"))
    # r_fallida es None porque la reserva nunca se creó: provoca AttributeError
    r_fallida = ejecutar_operacion(next(n), "Reserva de Luis -> Ciberseguridad 0 h (inválida)",
        lambda: g.crear_reserva(luis, "Ciberseguridad", 0))
    ejecutar_operacion(next(n), "Error imprevisto: confirmar una reserva que no existe (None)",
        lambda: r_fallida.confirmar())

    # ---------- RESUMEN ----------
    print("\n" + "=" * 70)
    print("RESUMEN DEL SISTEMA")
    print("=" * 70)
    print(g.resumen())
    print(f"\nOperaciones exitosas: {resultados['exitosas']} | fallidas controladas: {resultados['fallidas']}")
    print(f"El sistema terminó sin interrupciones. Log: {RUTA_LOG}")
    log.info(f"===== Fin de simulación: {resultados} =====")


if __name__ == "__main__":
    main()
