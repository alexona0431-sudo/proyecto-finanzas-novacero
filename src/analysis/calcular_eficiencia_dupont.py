import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "data" / "processed" / "estados_financieros_novacero_2023_2025.csv"
SALIDA = ROOT / "data" / "processed" / "eficiencia_dupont_2023_2025.csv"
REPORTE = ROOT / "reports" / "eficiencia_dupont.md"
ANIOS = ["2023", "2024", "2025"]

ALIAS = {
    "ventas": ["Ingresos de actividades ordinarias", "Ingresos por ventas"],
    "costo_ventas": ["Costo de ventas"],
    "cuentas_cobrar": ["Cuentas por cobrar no relacionadas", "Cuentas por cobrar"],
    "inventarios": ["Inventarios"],
    "activo_total": ["Activo total"],
    "patrimonio": ["Patrimonio"],
    "utilidad_neta": ["Utilidad neta"],
    "utilidad_operativa": ["Utilidad operativa"],
    "gastos_financieros": ["Gastos financieros"],
}


def numero(valor):
    if valor is None or str(valor).strip() == "":
        return None
    return float(str(valor).replace(",", "").strip())


def cargar_base():
    with BASE.open(encoding="utf-8-sig", newline="") as archivo:
        filas = list(csv.DictReader(archivo))

    datos = {}
    if filas and "anio" in filas[0] and "valor" in filas[0]:
        for fila in filas:
            valor = numero(fila.get("valor"))
            if valor is not None:
                datos[(fila["cuenta"].strip(), str(fila["anio"]).strip())] = valor
    else:
        for fila in filas:
            cuenta = fila["cuenta"].strip()
            for anio in ANIOS:
                valor = numero(fila.get(anio))
                if valor is not None:
                    datos[(cuenta, anio)] = valor
    return datos


def obtener(datos, clave, anio):
    for cuenta in ALIAS[clave]:
        if (cuenta, anio) in datos:
            return datos[(cuenta, anio)]
    nombres = " o ".join(ALIAS[clave])
    raise KeyError(f"Falta {nombres} para {anio}")


def promedio_saldo(datos, clave, anio):
    actual = obtener(datos, clave, anio)
    if anio == "2023":
        return actual, "saldo final (no se dispone de 2022)"
    anterior = obtener(datos, clave, str(int(anio) - 1))
    return (anterior + actual) / 2, "saldo promedio"


def dividir(numerador, denominador):
    return numerador / denominador if denominador else 0.0


def calcular(datos):
    resultados = []
    for anio in ANIOS:
        ventas = obtener(datos, "ventas", anio)
        costo = obtener(datos, "costo_ventas", anio)
        utilidad_neta = obtener(datos, "utilidad_neta", anio)
        utilidad_operativa = obtener(datos, "utilidad_operativa", anio)
        gastos_financieros = obtener(datos, "gastos_financieros", anio)

        cartera, criterio = promedio_saldo(datos, "cuentas_cobrar", anio)
        inventario, _ = promedio_saldo(datos, "inventarios", anio)
        activos, _ = promedio_saldo(datos, "activo_total", anio)
        patrimonio, _ = promedio_saldo(datos, "patrimonio", anio)

        rotacion_cartera = dividir(ventas, cartera)
        rotacion_inventarios = dividir(costo, inventario)
        rotacion_activos = dividir(ventas, activos)
        margen_neto = dividir(utilidad_neta, ventas)
        multiplicador_capital = dividir(activos, patrimonio)
        roe_dupont = margen_neto * rotacion_activos * multiplicador_capital

        indicadores = [
            ("Rotación de cuentas por cobrar", rotacion_cartera, "veces", criterio),
            ("Periodo medio de cobro", dividir(365, rotacion_cartera), "días", criterio),
            ("Rotación de inventarios", rotacion_inventarios, "veces", criterio),
            ("Periodo medio de inventario", dividir(365, rotacion_inventarios), "días", criterio),
            ("Rotación de activos", rotacion_activos, "veces", criterio),
            ("Cobertura de intereses", dividir(utilidad_operativa, gastos_financieros), "veces", "utilidad operativa / gastos financieros"),
            ("Margen neto DuPont", margen_neto * 100, "%", "utilidad neta / ventas"),
            ("Multiplicador del capital", multiplicador_capital, "veces", criterio),
            ("ROE DuPont", roe_dupont * 100, "%", "margen neto × rotación de activos × multiplicador del capital"),
        ]
        for indicador, valor, unidad, formula in indicadores:
            resultados.append(
                {"anio": anio, "indicador": indicador, "valor": round(valor, 4), "unidad": unidad, "criterio": formula}
            )
    return resultados


def valor_resultado(resultados, indicador, anio):
    for fila in resultados:
        if fila["indicador"] == indicador and fila["anio"] == anio:
            return fila["valor"]
    raise KeyError(f"{indicador}/{anio}")


def guardar_csv(resultados):
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["anio", "indicador", "valor", "unidad", "criterio"])
        escritor.writeheader()
        escritor.writerows(resultados)


def crear_reporte(resultados):
    REPORTE.parent.mkdir(parents=True, exist_ok=True)
    indicadores = [
        "Rotación de cuentas por cobrar",
        "Periodo medio de cobro",
        "Rotación de inventarios",
        "Periodo medio de inventario",
        "Rotación de activos",
        "Cobertura de intereses",
        "Margen neto DuPont",
        "Multiplicador del capital",
        "ROE DuPont",
    ]
    unidades = {fila["indicador"]: fila["unidad"] for fila in resultados}
    lineas = [
        "# Eficiencia, cobertura de intereses y sistema DuPont",
        "",
        "## Metodología",
        "",
        "- Para 2024 y 2025 se utilizaron saldos promedio de inicio y cierre.",
        "- Para 2023 se utilizaron saldos de cierre porque la base no contiene cifras de 2022.",
        "- El ROE DuPont se calcula como margen neto × rotación de activos × multiplicador del capital.",
        "",
        "## Resultados",
        "",
        "| Indicador | 2023 | 2024 | 2025 | Unidad |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for indicador in indicadores:
        valores = [valor_resultado(resultados, indicador, anio) for anio in ANIOS]
        lineas.append(
            f"| {indicador} | {valores[0]:.2f} | {valores[1]:.2f} | {valores[2]:.2f} | {unidades[indicador]} |"
        )

    cobertura_2025 = valor_resultado(resultados, "Cobertura de intereses", "2025")
    rotacion_activos_2025 = valor_resultado(resultados, "Rotación de activos", "2025")
    roe_2024 = valor_resultado(resultados, "ROE DuPont", "2024")
    roe_2025 = valor_resultado(resultados, "ROE DuPont", "2025")
    lineas.extend(
        [
            "",
            "## Interpretación",
            "",
            f"- En 2025 la empresa generó aproximadamente ${cobertura_2025:.2f} de utilidad operativa por cada dólar de gasto financiero.",
            f"- La rotación de activos de 2025 fue {rotacion_activos_2025:.2f} veces; este indicador muestra la capacidad de los activos para generar ventas.",
            f"- El ROE DuPont pasó de {roe_2024:.2f}% en 2024 a {roe_2025:.2f}% en 2025.",
            "- La descomposición DuPont permite distinguir si la rentabilidad proviene del margen, de la eficiencia de los activos o del apalancamiento.",
            "- Estos resultados deben interpretarse junto con el aumento del endeudamiento y el flujo operativo negativo observado en 2025.",
            "",
            "## Limitación",
            "",
            "La comparación de 2023 usa saldos finales en lugar de promedios porque no se incorporaron cifras de 2022. No se inventaron saldos iniciales.",
        ]
    )
    REPORTE.write_text("\n".join(lineas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    base = cargar_base()
    resultados = calcular(base)
    guardar_csv(resultados)
    crear_reporte(resultados)
    print(f"Generados {len(resultados)} indicadores")
    print(f"CSV: {SALIDA}")
    print(f"Reporte: {REPORTE}")
