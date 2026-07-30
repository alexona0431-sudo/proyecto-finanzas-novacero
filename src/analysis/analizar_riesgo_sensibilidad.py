import copy
import csv
from pathlib import Path

from calcular_proyecto_fotovoltaico import (
    cargar_supuestos,
    construir_modelo,
    periodo_recuperacion,
    tir,
    van,
)

ROOT = Path(__file__).resolve().parents[2]
SALIDA_ESCENARIOS = ROOT / "data" / "processed" / "escenarios_fotovoltaico.csv"
SALIDA_SENSIBILIDAD = ROOT / "data" / "processed" / "sensibilidad_fotovoltaico.csv"
REPORTE = ROOT / "reports" / "riesgo_sensibilidad.md"


def evaluar(s):
    _, proyecto, _, _, beneficios, costos = construir_modelo(s)
    tasa = s["tasa_descuento_base"]
    pv_beneficios = sum(v / ((1 + tasa) ** i) for i, v in enumerate(beneficios))
    pv_costos = sum(v / ((1 + tasa) ** i) for i, v in enumerate(costos))
    return {
        "van": van(tasa, proyecto),
        "tir": tir(proyecto),
        "beneficio_costo": pv_beneficios / pv_costos,
        "payback": periodo_recuperacion(proyecto),
        "payback_descontado": periodo_recuperacion(proyecto, tasa),
    }


def escenarios(base):
    configuraciones = []

    optimista = copy.deepcopy(base)
    optimista["inversion_inicial"] *= 0.90
    optimista["generacion_primer_anio"] *= 1.10
    optimista["tarifa_energia"] *= 1.10
    optimista["porcentaje_autoconsumo"] = 0.95
    optimista["tasa_descuento_base"] = 0.08
    configuraciones.append(("Optimista", optimista))

    configuraciones.append(("Base", copy.deepcopy(base)))

    pesimista = copy.deepcopy(base)
    pesimista["inversion_inicial"] *= 1.10
    pesimista["generacion_primer_anio"] *= 0.90
    pesimista["tarifa_energia"] *= 0.90
    pesimista["porcentaje_autoconsumo"] = 0.80
    pesimista["tasa_descuento_base"] = 0.12
    configuraciones.append(("Pesimista", pesimista))

    filas = []
    for nombre, supuestos in configuraciones:
        resultado = evaluar(supuestos)
        filas.append({
            "escenario": nombre,
            "inversion_inicial": supuestos["inversion_inicial"],
            "generacion_primer_anio": supuestos["generacion_primer_anio"],
            "tarifa_energia": supuestos["tarifa_energia"],
            "autoconsumo": supuestos["porcentaje_autoconsumo"],
            "tasa_descuento": supuestos["tasa_descuento_base"],
            **resultado,
        })
    return filas


def sensibilidad(base):
    filas = []
    casos = {
        "inversion_inicial": [-0.20, -0.10, 0, 0.10, 0.20],
        "generacion_primer_anio": [-0.20, -0.10, 0, 0.10, 0.20],
        "tarifa_energia": [-0.20, -0.10, 0, 0.10, 0.20],
        "porcentaje_autoconsumo": [-0.10, -0.05, 0, 0.05, 0.10],
    }
    for variable, cambios in casos.items():
        for cambio in cambios:
            s = copy.deepcopy(base)
            if variable == "porcentaje_autoconsumo":
                s[variable] = min(1.0, max(0.0, base[variable] + cambio))
                valor_variable = s[variable]
            else:
                s[variable] = base[variable] * (1 + cambio)
                valor_variable = s[variable]
            resultado = evaluar(s)
            filas.append({
                "variable": variable,
                "cambio": cambio,
                "valor_variable": valor_variable,
                "van": resultado["van"],
                "tir": resultado["tir"],
            })

    for tasa in [0.08, 0.10, 0.12, 0.14]:
        s = copy.deepcopy(base)
        s["tasa_descuento_base"] = tasa
        resultado = evaluar(s)
        filas.append({
            "variable": "tasa_descuento_base",
            "cambio": tasa - base["tasa_descuento_base"],
            "valor_variable": tasa,
            "van": resultado["van"],
            "tir": resultado["tir"],
        })
    return filas


def buscar_equilibrio(base, variable, inferior, superior):
    for _ in range(100):
        medio = (inferior + superior) / 2
        s = copy.deepcopy(base)
        s[variable] = medio
        resultado = evaluar(s)["van"]
        if variable == "inversion_inicial":
            if resultado > 0:
                inferior = medio
            else:
                superior = medio
        else:
            if resultado > 0:
                superior = medio
            else:
                inferior = medio
    return (inferior + superior) / 2


def guardar_csv(ruta, filas):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0].keys()))
        escritor.writeheader()
        escritor.writerows(filas)


def crear_reporte(base, filas_escenarios, filas_sensibilidad):
    tarifa_equilibrio = buscar_equilibrio(base, "tarifa_energia", 0.03, 0.20)
    capex_equilibrio = buscar_equilibrio(base, "inversion_inicial", 300000, 1200000)
    autoconsumo_equilibrio = buscar_equilibrio(
        base, "porcentaje_autoconsumo", 0.50, 1.00
    )

    lineas = [
        "# Riesgo y sensibilidad del proyecto fotovoltaico",
        "",
        "## Escenarios",
        "",
        "| Escenario | VAN | TIR | B/C | Payback simple | Payback descontado |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for f in filas_escenarios:
        pd = (
            "No recuperado"
            if f["payback_descontado"] is None
            else f"{f['payback_descontado']:.2f} años"
        )
        ps = "No recuperado" if f["payback"] is None else f"{f['payback']:.2f} años"
        lineas.append(
            f"| {f['escenario']} | ${f['van']:,.2f} | "
            f"{f['tir']*100:.2f}% | {f['beneficio_costo']:.3f} | {ps} | {pd} |"
        )

    lineas.extend([
        "",
        "Los escenarios son ejercicios de estrés y no representan pronósticos garantizados.",
        "",
        "## Puntos de equilibrio",
        "",
        f"- Tarifa mínima aproximada para VAN igual a cero: ${tarifa_equilibrio:.4f}/kWh.",
        f"- Inversión máxima aproximada para VAN igual a cero: ${capex_equilibrio:,.2f}.",
        f"- Autoconsumo mínimo aproximado para VAN igual a cero: {autoconsumo_equilibrio*100:.2f}%.",
        "",
        "## Interpretación de sensibilidad",
        "",
        "- El VAN es especialmente sensible al costo inicial, la tarifa evitada y la generación.",
        "- Una cotización inferior al supuesto base puede convertir el proyecto en viable.",
        "- Una reducción de la generación o del autoconsumo deteriora rápidamente la rentabilidad.",
        "- Una tasa de descuento mayor reduce el VAN y aumenta la exigencia financiera.",
        "",
        "## Matriz de riesgos",
        "",
        "| Riesgo | Probabilidad | Impacto | Tratamiento |",
        "| --- | --- | --- | --- |",
        "| Generación inferior a la estimada | Media | Alto | Estudio solar y garantías de rendimiento |",
        "| Sobrecosto de instalación | Media | Alto | Cotizaciones comparables y contrato a precio fijo |",
        "| Menor autoconsumo | Media | Alto | Analizar curvas horarias de carga |",
        "| Cambio de tarifa eléctrica | Media | Alto | Sensibilidad y revisión anual |",
        "| Falla o reemplazo del inversor | Media | Medio | Garantía y fondo de reposición |",
        "| Aumento de la tasa del crédito | Baja | Medio | Negociar tasa fija |",
        "| Retrasos regulatorios o técnicos | Baja | Medio | Cronograma y permisos previos |",
        "",
        "## Conclusión de riesgo",
        "",
        "El escenario base no cumple la rentabilidad mínima, pero el proyecto puede volverse viable mediante una reducción de la inversión, una mayor tarifa evitada o un mayor nivel de autoconsumo. La decisión final debe condicionarse a obtener una cotización real y validar el consumo eléctrico horario de Novacero.",
    ])
    REPORTE.parent.mkdir(parents=True, exist_ok=True)
    REPORTE.write_text("\n".join(lineas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    supuestos = cargar_supuestos()
    filas_escenarios = escenarios(supuestos)
    filas_sensibilidad = sensibilidad(supuestos)
    guardar_csv(SALIDA_ESCENARIOS, filas_escenarios)
    guardar_csv(SALIDA_SENSIBILIDAD, filas_sensibilidad)
    crear_reporte(supuestos, filas_escenarios, filas_sensibilidad)
    print(f"Escenarios: {SALIDA_ESCENARIOS}")
    print(f"Sensibilidad: {SALIDA_SENSIBILIDAD}")
    print(f"Reporte: {REPORTE}")
