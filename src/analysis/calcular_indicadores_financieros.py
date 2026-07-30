import csv
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "data" / "processed" / "estados_financieros_novacero_2023_2025.csv"
SALIDA = ROOT / "data" / "processed" / "indicadores_financieros_2023_2025.csv"
REPORTE = ROOT / "reports" / "diagnostico_financiero.md"

ANIOS = ["2023", "2024", "2025"]


def cargar_base():
    with BASE.open(encoding="utf-8") as archivo:
        registros = list(csv.DictReader(archivo))

    return {
        (fila["cuenta"], fila["anio"]): Decimal(fila["valor"])
        for fila in registros
    }


def valor(base, cuenta, anio):
    return base[(cuenta, anio)]


def porcentaje(numero):
    return numero * Decimal("100")


def calcular(base):
    resultados = []

    for anio in ANIOS:
        activo_corriente = valor(base, "Activo corriente", anio)
        inventarios = valor(base, "Inventarios", anio)
        efectivo = valor(base, "Efectivo y equivalentes", anio)
        activo_total = valor(base, "Activo total", anio)
        pasivo_corriente = valor(base, "Pasivo corriente", anio)
        pasivo_total = valor(base, "Pasivo total", anio)
        patrimonio = valor(base, "Patrimonio", anio)
        ventas = valor(base, "Ingresos de actividades ordinarias", anio)
        utilidad_bruta = valor(base, "Utilidad bruta", anio)
        utilidad_operativa = valor(base, "Utilidad operativa", anio)
        utilidad_neta = valor(base, "Utilidad neta", anio)
        flujo_operacion = valor(base, "Flujo de operación", anio)

        indicadores = [
            ("Liquidez corriente", activo_corriente / pasivo_corriente,
             "veces", "Activo corriente / Pasivo corriente"),
            ("Prueba ácida", (activo_corriente - inventarios) / pasivo_corriente,
             "veces", "(Activo corriente - Inventarios) / Pasivo corriente"),
            ("Razón de efectivo", efectivo / pasivo_corriente,
             "veces", "Efectivo / Pasivo corriente"),
            ("Nivel de endeudamiento", porcentaje(pasivo_total / activo_total),
             "%", "Pasivo total / Activo total"),
            ("Deuda sobre patrimonio", pasivo_total / patrimonio,
             "veces", "Pasivo total / Patrimonio"),
            ("Margen bruto", porcentaje(utilidad_bruta / ventas),
             "%", "Utilidad bruta / Ventas"),
            ("Margen operativo", porcentaje(utilidad_operativa / ventas),
             "%", "Utilidad operativa / Ventas"),
            ("Margen neto", porcentaje(utilidad_neta / ventas),
             "%", "Utilidad neta / Ventas"),
            ("ROA", porcentaje(utilidad_neta / activo_total),
             "%", "Utilidad neta / Activo total"),
            ("ROE", porcentaje(utilidad_neta / patrimonio),
             "%", "Utilidad neta / Patrimonio"),
            ("Cobertura del pasivo corriente con flujo operativo",
             flujo_operacion / pasivo_corriente,
             "veces", "Flujo de operación / Pasivo corriente"),
        ]

        for indicador, resultado, unidad, formula in indicadores:
            resultados.append({
                "anio": anio,
                "indicador": indicador,
                "valor": f"{resultado:.6f}",
                "unidad": unidad,
                "formula": formula,
            })

    return resultados


def guardar_csv(resultados):
    SALIDA.parent.mkdir(parents=True, exist_ok=True)

    with SALIDA.open("w", newline="", encoding="utf-8") as archivo:
        columnas = ["anio", "indicador", "valor", "unidad", "formula"]
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(resultados)


def buscar(resultados, indicador, anio):
    for fila in resultados:
        if fila["indicador"] == indicador and fila["anio"] == anio:
            return Decimal(fila["valor"])
    raise KeyError(f"{indicador}/{anio}")


def crear_reporte(resultados):
    lineas = [
        "# Diagnóstico financiero de Novacero S.A. 2023-2025",
        "",
        "## Supuestos metodológicos",
        "",
        "- Las cifras se expresan en dólares estadounidenses.",
        "- Los indicadores utilizan saldos de cierre para mantener el mismo criterio en los tres años.",
        "- Los datos provienen de los estados financieros presentados ante la Superintendencia de Compañías.",
        "- No se utilizaron datos simulados en este diagnóstico histórico.",
        "",
        "## Indicadores financieros",
        "",
        "| Indicador | 2023 | 2024 | 2025 | Unidad |",
        "| --- | ---: | ---: | ---: | --- |",
    ]

    nombres = list(dict.fromkeys(fila["indicador"] for fila in resultados))

    for nombre in nombres:
        valores = [buscar(resultados, nombre, anio) for anio in ANIOS]
        unidad = next(
            fila["unidad"] for fila in resultados
            if fila["indicador"] == nombre
        )
        lineas.append(
            f"| {nombre} | {valores[0]:.2f} | {valores[1]:.2f} | "
            f"{valores[2]:.2f} | {unidad} |"
        )

    lineas.extend([
        "",
        "## Interpretación",
        "",
        "- La liquidez corriente se mantuvo por encima de 1 durante los tres años, aunque disminuyó de 1,76 en 2023 a 1,59 en 2025.",
        "- La prueba ácida fue inferior a 1, lo que evidencia dependencia de los inventarios para cubrir obligaciones corrientes.",
        "- El nivel de endeudamiento aumentó hasta aproximadamente 61,79 % en 2025.",
        "- El margen neto cayó en 2024 y se recuperó parcialmente en 2025.",
        "- La rentabilidad sobre los activos y el patrimonio se debilitó en 2024 y mejoró en 2025.",
        "- El flujo operativo fue negativo en 2025, situación que requiere atención porque la operación no generó efectivo durante ese año.",
        "- El aumento del financiamiento en 2025 ayudó a compensar los flujos negativos de operación e inversión.",
        "",
        "## Conclusión preliminar",
        "",
        "Novacero mantiene capacidad para cubrir sus obligaciones corrientes, pero presenta una mayor presión financiera en 2025. El crecimiento del pasivo, la reducción de la liquidez y el flujo operativo negativo muestran que una nueva inversión deberá evaluarse mediante escenarios conservadores y una estructura de financiamiento que no incremente excesivamente el riesgo.",
    ])

    REPORTE.parent.mkdir(parents=True, exist_ok=True)
    REPORTE.write_text("\n".join(lineas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    base = cargar_base()
    indicadores = calcular(base)
    guardar_csv(indicadores)
    crear_reporte(indicadores)

    print(f"Generados {len(indicadores)} indicadores")
    print(f"CSV: {SALIDA}")
    print(f"Reporte: {REPORTE}")