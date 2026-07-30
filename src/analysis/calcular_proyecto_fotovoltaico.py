import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUPUESTOS = ROOT / "data" / "project" / "supuestos_fotovoltaico.csv"
SALIDA_FLUJO = ROOT / "data" / "processed" / "flujo_caja_fotovoltaico.csv"
SALIDA_METRICAS = ROOT / "data" / "processed" / "metricas_inversion_fotovoltaico.csv"
REPORTE = ROOT / "reports" / "ingenieria_economica.md"


def cargar_supuestos():
    with SUPUESTOS.open(encoding="utf-8-sig") as archivo:
        return {fila["parametro"]: float(fila["valor"]) for fila in csv.DictReader(archivo)}


def van(tasa, flujos):
    return sum(flujo / ((1 + tasa) ** periodo) for periodo, flujo in enumerate(flujos))


def tir(flujos):
    inferior, superior = -0.99, 2.0
    if van(inferior, flujos) * van(superior, flujos) > 0:
        return None
    for _ in range(250):
        medio = (inferior + superior) / 2
        if van(inferior, flujos) * van(medio, flujos) <= 0:
            superior = medio
        else:
            inferior = medio
    return (inferior + superior) / 2


def periodo_recuperacion(flujos, tasa=None):
    acumulado = flujos[0]
    if acumulado >= 0:
        return 0.0
    for anio in range(1, len(flujos)):
        flujo = flujos[anio]
        if tasa is not None:
            flujo /= (1 + tasa) ** anio
        anterior = acumulado
        acumulado += flujo
        if acumulado >= 0 and flujo != 0:
            return (anio - 1) + abs(anterior) / flujo
    return None


def anualidad(prestamo, tasa, plazo):
    return prestamo * tasa / (1 - (1 + tasa) ** (-plazo))


def construir_modelo(s):
    vida = int(s["vida_util"])
    capex = s["inversion_inicial"]
    residual = capex * s["valor_residual"]
    depreciacion = (capex - residual) / vida
    deuda = capex * s["porcentaje_credito"]
    aporte = capex * s["porcentaje_recursos_propios"]
    tasa_deuda = s["tasa_credito"]
    plazo = int(s["plazo_credito"])
    cuota = anualidad(deuda, tasa_deuda, plazo)
    saldo_deuda = deuda

    flujo_proyecto = [-capex]
    flujo_propios = [-capex]
    flujo_credito = [-aporte]
    beneficios = [0.0]
    costos = [capex]
    registros = []

    registros.append({
        "anio": 0, "generacion_kwh": 0, "ahorro_energia": 0,
        "mantenimiento": 0, "depreciacion": 0, "interes": 0,
        "amortizacion": 0, "cuota_credito": 0, "impuesto_proyecto": 0,
        "flujo_proyecto": -capex, "flujo_recursos_propios": -capex,
        "flujo_con_credito": -aporte,
    })

    for anio in range(1, vida + 1):
        generacion = (
            s["generacion_primer_anio"]
            * ((1 - s["degradacion_paneles"]) ** (anio - 1))
        )
        tarifa = s["tarifa_energia"] * ((1 + s["crecimiento_tarifa"]) ** (anio - 1))
        ahorro = generacion * s["porcentaje_autoconsumo"] * tarifa
        mantenimiento = (
            capex * s["operacion_mantenimiento"]
            * ((1 + s["inflacion_mantenimiento"]) ** (anio - 1))
        )
        reemplazo = (
            capex * s["costo_reemplazo_inversor"]
            if anio == int(s["reemplazo_inversor_anio"]) else 0
        )
        valor_residual = residual if anio == vida else 0
        ebit = ahorro - mantenimiento - depreciacion
        impuesto_proyecto = max(0, ebit * s["tasa_impuesto_renta"])
        fcf = ahorro - mantenimiento - impuesto_proyecto - reemplazo + valor_residual

        if anio <= plazo:
            interes = saldo_deuda * tasa_deuda
            amortizacion = cuota - interes
            saldo_deuda = max(0, saldo_deuda - amortizacion)
            impuesto_credito = max(
                0, (ebit - interes) * s["tasa_impuesto_renta"]
            )
            flujo_deuda = (
                ahorro - mantenimiento - impuesto_credito
                - cuota - reemplazo + valor_residual
            )
        else:
            interes = amortizacion = 0
            impuesto_credito = impuesto_proyecto
            flujo_deuda = fcf

        flujo_proyecto.append(fcf)
        flujo_propios.append(fcf)
        flujo_credito.append(flujo_deuda)
        beneficios.append(ahorro + valor_residual)
        costos.append(mantenimiento + impuesto_proyecto + reemplazo)

        registros.append({
            "anio": anio,
            "generacion_kwh": generacion,
            "ahorro_energia": ahorro,
            "mantenimiento": mantenimiento,
            "depreciacion": depreciacion,
            "interes": interes,
            "amortizacion": amortizacion,
            "cuota_credito": cuota if anio <= plazo else 0,
            "impuesto_proyecto": impuesto_proyecto,
            "flujo_proyecto": fcf,
            "flujo_recursos_propios": fcf,
            "flujo_con_credito": flujo_deuda,
        })

    return registros, flujo_proyecto, flujo_propios, flujo_credito, beneficios, costos


def calcular_metricas(s, proyecto, propios, credito, beneficios, costos):
    tasa_base = s["tasa_descuento_base"]
    costo_patrimonio = s["costo_patrimonio"]
    wacc = (
        s["porcentaje_recursos_propios"] * costo_patrimonio
        + s["porcentaje_credito"] * s["tasa_credito"]
        * (1 - s["tasa_impuesto_renta"])
    )
    pv_beneficios = sum(
        valor / ((1 + tasa_base) ** anio)
        for anio, valor in enumerate(beneficios)
    )
    pv_costos = sum(
        valor / ((1 + tasa_base) ** anio)
        for anio, valor in enumerate(costos)
    )

    metricas = {
        "WACC": wacc,
        "VAN proyecto al 10%": van(tasa_base, proyecto),
        "TIR proyecto": tir(proyecto),
        "Beneficio costo": pv_beneficios / pv_costos,
        "Payback simple": periodo_recuperacion(proyecto),
        "Payback descontado": periodo_recuperacion(proyecto, tasa_base),
        "VAN recursos propios": van(costo_patrimonio, propios),
        "VAN con crédito": van(costo_patrimonio, credito),
        "TIR recursos propios": tir(propios),
        "TIR con crédito": tir(credito),
        "VAN no invertir": 0.0,
    }
    return metricas


def guardar(registros, metricas):
    SALIDA_FLUJO.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA_FLUJO.open("w", newline="", encoding="utf-8") as archivo:
        campos = list(registros[0].keys())
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)

    with SALIDA_METRICAS.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["metrica", "valor"])
        for nombre, valor in metricas.items():
            escritor.writerow([nombre, "" if valor is None else f"{valor:.6f}"])


def crear_reporte(s, metricas):
    def dinero(valor):
        return f"${valor:,.2f}"

    def porcentaje(valor):
        return "No calculable" if valor is None else f"{valor * 100:.2f}%"

    def anios(valor):
        return "No recuperado" if valor is None else f"{valor:.2f} años"

    decision = (
        "ACEPTAR el proyecto"
        if metricas["VAN proyecto al 10%"] > 0
        and metricas["TIR proyecto"] > s["tasa_descuento_base"]
        else "RECHAZAR o rediseñar el proyecto"
    )
    lineas = [
        "# Evaluación de ingeniería económica del sistema fotovoltaico",
        "",
        "## Alcance y supuestos",
        "",
        f"- Potencia: {s['potencia_instalada']:,.0f} kWp.",
        f"- Inversión inicial: {dinero(s['inversion_inicial'])}.",
        f"- Horizonte: {int(s['vida_util'])} años.",
        f"- Tasa de descuento conservadora: {s['tasa_descuento_base']*100:.2f}%.",
        f"- Tasa del crédito: {s['tasa_credito']*100:.2f}%.",
        "- Los datos no públicos se identifican como supuestos académicos.",
        "- El capital de trabajo incremental se supone igual a cero porque el proyecto genera ahorro energético y no ventas adicionales.",
        "",
        "## Resultados principales",
        "",
        "| Indicador | Resultado |",
        "| --- | ---: |",
        f"| WACC | {porcentaje(metricas['WACC'])} |",
        f"| VAN del proyecto | {dinero(metricas['VAN proyecto al 10%'])} |",
        f"| TIR del proyecto | {porcentaje(metricas['TIR proyecto'])} |",
        f"| Relación beneficio/costo | {metricas['Beneficio costo']:.3f} |",
        f"| Recuperación simple | {anios(metricas['Payback simple'])} |",
        f"| Recuperación descontada | {anios(metricas['Payback descontado'])} |",
        "",
        "## Comparación de alternativas",
        "",
        "| Alternativa | VAN para el inversionista | TIR |",
        "| --- | ---: | ---: |",
        f"| Recursos propios | {dinero(metricas['VAN recursos propios'])} | {porcentaje(metricas['TIR recursos propios'])} |",
        f"| Crédito bancario | {dinero(metricas['VAN con crédito'])} | {porcentaje(metricas['TIR con crédito'])} |",
        "| No invertir | $0.00 | 0.00% |",
        "",
        "## Decisión preliminar",
        "",
        f"Con los supuestos del escenario base se recomienda **{decision}**.",
        "Esta conclusión deberá confirmarse mediante escenarios y sensibilidad antes de emitir la recomendación final.",
        "",
        "## Limitaciones",
        "",
        "- La potencia y el costo requieren una cotización técnica real.",
        "- El porcentaje de autoconsumo debe validarse con facturas y curvas de carga de Novacero.",
        "- La tarifa debe ajustarse al nivel de voltaje real del suministro.",
        "- El modelo supone depreciación lineal y no incorpora incentivos tributarios especiales.",
    ]
    REPORTE.parent.mkdir(parents=True, exist_ok=True)
    REPORTE.write_text("\n".join(lineas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    supuestos = cargar_supuestos()
    datos = construir_modelo(supuestos)
    registros, proyecto, propios, credito, beneficios, costos = datos
    metricas = calcular_metricas(
        supuestos, proyecto, propios, credito, beneficios, costos
    )
    guardar(registros, metricas)
    crear_reporte(supuestos, metricas)
    print(f"Flujo generado: {SALIDA_FLUJO}")
    print(f"Métricas generadas: {SALIDA_METRICAS}")
    print(f"Reporte generado: {REPORTE}")
    print(f"VAN proyecto: {metricas['VAN proyecto al 10%']:.2f}")
    print(f"TIR proyecto: {metricas['TIR proyecto']*100:.2f}%")
