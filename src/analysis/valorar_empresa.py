import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "data" / "processed" / "estados_financieros_novacero_2023_2025.csv"
SALIDA = ROOT / "data" / "processed" / "valoracion_novacero.csv"
REPORTE = ROOT / "reports" / "valoracion_dividendos_control.md"

ANIOS = ["2023", "2024", "2025"]
COSTO_PATRIMONIO = 0.125
CRECIMIENTO_EXPLICITO = 0.03
CRECIMIENTO_TERMINAL = 0.02
PORCENTAJE_FCFE = 0.70
AJUSTE_INVENTARIOS = 0.10
AJUSTE_CUENTAS_COBRAR = 0.05


def cargar_base():
    with BASE.open(encoding="utf-8-sig") as archivo:
        filas = list(csv.DictReader(archivo))
    return {
        (fila["cuenta"], fila["anio"]): float(fila["valor"])
        for fila in filas
    }


def valor(base, cuenta, anio):
    return base[(cuenta, anio)]


def valorar(base):
    utilidades = [valor(base, "Utilidad neta", anio) for anio in ANIOS]
    utilidad_normalizada = sum(utilidades) / len(utilidades)
    fcfe_inicial = utilidad_normalizada * PORCENTAJE_FCFE

    flujos = []
    valor_presente_explicito = 0
    for anio in range(1, 6):
        fcfe = fcfe_inicial * ((1 + CRECIMIENTO_EXPLICITO) ** anio)
        valor_presente = fcfe / ((1 + COSTO_PATRIMONIO) ** anio)
        valor_presente_explicito += valor_presente
        flujos.append({
            "periodo": anio,
            "fcfe_proyectado": fcfe,
            "factor_descuento": 1 / ((1 + COSTO_PATRIMONIO) ** anio),
            "valor_presente": valor_presente,
        })

    fcfe_anio_5 = flujos[-1]["fcfe_proyectado"]
    valor_terminal = (
        fcfe_anio_5 * (1 + CRECIMIENTO_TERMINAL)
        / (COSTO_PATRIMONIO - CRECIMIENTO_TERMINAL)
    )
    valor_presente_terminal = valor_terminal / ((1 + COSTO_PATRIMONIO) ** 5)
    valor_fcfe = valor_presente_explicito + valor_presente_terminal

    patrimonio = valor(base, "Patrimonio", "2025")
    inventarios = valor(base, "Inventarios", "2025")
    cuentas_cobrar = valor(
        base, "Cuentas por cobrar no relacionadas", "2025"
    )
    ajuste_inventarios = inventarios * AJUSTE_INVENTARIOS
    ajuste_cartera = cuentas_cobrar * AJUSTE_CUENTAS_COBRAR
    valor_contable_ajustado = patrimonio - ajuste_inventarios - ajuste_cartera

    metricas = {
        "utilidad_neta_promedio_2023_2025": utilidad_normalizada,
        "fcfe_normalizado": fcfe_inicial,
        "valor_presente_flujos_explicitos": valor_presente_explicito,
        "valor_terminal": valor_terminal,
        "valor_presente_terminal": valor_presente_terminal,
        "valor_patrimonio_por_fcfe": valor_fcfe,
        "patrimonio_contable_2025": patrimonio,
        "ajuste_inventarios": ajuste_inventarios,
        "ajuste_cuentas_cobrar": ajuste_cartera,
        "valor_contable_ajustado": valor_contable_ajustado,
        "diferencia_metodos": valor_contable_ajustado - valor_fcfe,
    }
    return flujos, metricas


def guardar(flujos, metricas):
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with SALIDA.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["seccion", "concepto", "valor"])
        for fila in flujos:
            for concepto, dato in fila.items():
                escritor.writerow([f"proyeccion_anio_{fila['periodo']}", concepto, dato])
        for concepto, dato in metricas.items():
            escritor.writerow(["metricas", concepto, dato])


def crear_reporte(metricas):
    def usd(numero):
        return f"${numero:,.2f}"

    lineas = [
        "# Valoración empresarial, dividendos y control corporativo",
        "",
        "## Alcance",
        "",
        "La valoración es una estimación académica construida con la información financiera pública disponible. No constituye una oferta de compra, venta ni una tasación profesional.",
        "",
        "## Método principal: flujo de caja al accionista (FCFE)",
        "",
        f"- Utilidad neta promedio 2023-2025: {usd(metricas['utilidad_neta_promedio_2023_2025'])}.",
        f"- FCFE normalizado: 70% de la utilidad promedio = {usd(metricas['fcfe_normalizado'])}.",
        "- El 30% restante se considera reinversión necesaria.",
        f"- Crecimiento explícito: {CRECIMIENTO_EXPLICITO*100:.2f}% anual durante cinco años.",
        f"- Costo del patrimonio: {COSTO_PATRIMONIO*100:.2f}%.",
        f"- Crecimiento terminal: {CRECIMIENTO_TERMINAL*100:.2f}%.",
        f"- Valor patrimonial estimado por FCFE: **{usd(metricas['valor_patrimonio_por_fcfe'])}**.",
        "",
        "## Método de contraste: valor contable ajustado",
        "",
        f"- Patrimonio contable 2025: {usd(metricas['patrimonio_contable_2025'])}.",
        f"- Ajuste conservador de 10% sobre inventarios: -{usd(metricas['ajuste_inventarios'])}.",
        f"- Ajuste conservador de 5% sobre cuentas por cobrar: -{usd(metricas['ajuste_cuentas_cobrar'])}.",
        f"- Valor contable ajustado: **{usd(metricas['valor_contable_ajustado'])}**.",
        "",
        "## Comparación e interpretación",
        "",
        f"La diferencia entre los métodos es {usd(metricas['diferencia_metodos'])}. El valor contable ajustado supera al valor obtenido por FCFE porque Novacero es una empresa industrial intensiva en activos y el método de flujos incorpora una visión conservadora de su capacidad reciente para generar efectivo.",
        "",
        "No se utilizó un precio bursátil observado porque en las fuentes revisadas no se identificó una cotización pública de acciones de Novacero. Por ello, los resultados representan valores estimados y no precios de mercado.",
        "",
        "## Dividendos y reinversión",
        "",
        "Los documentos utilizados no permiten confirmar una política pública de dividendos. Para fines del proyecto se propone retener inicialmente el 70% de las utilidades y distribuir como máximo el 30%, sujeto a las siguientes condiciones:",
        "",
        "- Flujo operativo positivo.",
        "- Liquidez corriente superior a 1,50.",
        "- Cumplimiento de obligaciones financieras.",
        "- Financiamiento asegurado para inversiones prioritarias.",
        "- Aprobación formal de accionistas y administradores.",
        "",
        "Debido al flujo operativo negativo de 2025 y al mayor endeudamiento, se recomienda priorizar liquidez, reducción de deuda y proyectos con VAN positivo antes de aumentar dividendos.",
        "",
        "## Control corporativo",
        "",
        "Novacero es una sociedad anónima ecuatoriana. Su historia institucional señala que desde 1994 pertenece a accionistas nacionales. La separación entre accionistas y administradores puede generar problemas de agencia cuando las decisiones de inversión no cuentan con metas, responsables y controles verificables.",
        "",
        "### Riesgos de control",
        "",
        "- Concentración de decisiones de inversión.",
        "- Conflictos de interés con proveedores o contratistas.",
        "- Selección de proyectos sin evaluación financiera suficiente.",
        "- Información asimétrica entre administradores y accionistas.",
        "- Falta de seguimiento posterior a la inversión.",
        "",
        "### Propuestas de mejora",
        "",
        "- Crear un comité de inversiones que revise VAN, TIR, WACC y riesgos.",
        "- Exigir al menos tres cotizaciones para inversiones importantes.",
        "- Mantener auditoría financiera y técnica independiente.",
        "- Aplicar el Código de Conducta y la política de conflictos de interés.",
        "- Presentar indicadores trimestrales a accionistas y administradores.",
        "- Comparar los resultados reales de cada proyecto con sus proyecciones.",
        "",
        "## Fuentes institucionales",
        "",
        "- Estados financieros de Novacero presentados ante la Superintendencia de Compañías.",
        "- Historia institucional: https://www.novacero.com/nuestra-historia/",
        "- Código de Conducta y Ética: https://www.novacero.com/codigo-de-conducta/",
        "",
        "## Limitaciones",
        "",
        "- No se dispone de una proyección oficial de flujos de Novacero.",
        "- El FCFE normalizado y las tasas de crecimiento son supuestos académicos.",
        "- Los ajustes de inventarios y cartera son escenarios conservadores y no deterioros contables confirmados.",
        "- La valoración deberá actualizarse si se obtiene información de deuda financiera, dividendos y planes estratégicos.",
    ]
    REPORTE.parent.mkdir(parents=True, exist_ok=True)
    REPORTE.write_text("\n".join(lineas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    base = cargar_base()
    flujos, metricas = valorar(base)
    guardar(flujos, metricas)
    crear_reporte(metricas)
    print(f"Valoración: {SALIDA}")
    print(f"Reporte: {REPORTE}")
    print(f"Valor FCFE: {metricas['valor_patrimonio_por_fcfe']:.2f}")
    print(f"Valor contable ajustado: {metricas['valor_contable_ajustado']:.2f}")
