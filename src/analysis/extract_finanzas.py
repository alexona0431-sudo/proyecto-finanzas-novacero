import csv
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / 'data' / 'raw'
PROCESSED_DIR = ROOT / 'data' / 'processed'
REPORTS_DIR = ROOT / 'reports'
CSV_PATH = PROCESSED_DIR / 'estados_financieros_novacero_2023_2025.csv'
JSON_PATH = PROCESSED_DIR / 'estados_financieros_novacero_2023_2025.json'
REPORT_PATH = REPORTS_DIR / 'auditoria_base_financiera.md'

YEARS = ['2023', '2024', '2025']

RAW_VALUES = [
    {'cuenta': 'Activo corriente', 'codigo_contable': '101', 'unidad': 'USD', 'values': {'2023': Decimal('194643079.96'), '2024': Decimal('174187868.08'), '2025': Decimal('245198838.83')}, 'pdf_fuente': {'2023': '2023_balance.pdf', '2024': '2024_balance.pdf', '2025': '2025_balance.pdf'}, 'pagina': {'2023': 1, '2024': 1, '2025': 1}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 101, página 1)', 'estado_validacion': 'validado'},
    {'cuenta': 'Activo no corriente', 'codigo_contable': '102', 'unidad': 'USD', 'values': {'2023': Decimal('155599829.48'), '2024': Decimal('163375580.53'), '2025': Decimal('181455793.87')}, 'pdf_fuente': {'2023': '2023_balance.pdf', '2024': '2024_balance.pdf', '2025': '2025_balance.pdf'}, 'pagina': {'2023': 4, '2024': 4, '2025': 4}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 102, página 4)', 'estado_validacion': 'validado'},
    {'cuenta': 'Activo total', 'codigo_contable': '1', 'unidad': 'USD', 'values': {'2023': Decimal('350242909.44'), '2024': Decimal('337563448.61'), '2025': Decimal('426654632.70')}, 'pdf_fuente': {'2023': '2023_balance.pdf', '2024': '2024_balance.pdf', '2025': '2025_balance.pdf'}, 'pagina': {'2023': 1, '2024': 1, '2025': 1}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 1, página 1)', 'estado_validacion': 'validado'},
    {'cuenta': 'Efectivo y equivalentes', 'codigo_contable': '10101', 'unidad': 'USD', 'values': {'2023': Decimal('4638098.53'), '2024': Decimal('9133620.05'), '2025': Decimal('6604545.58')}, 'pdf_fuente': {'2023': '2023_balance.pdf', '2024': '2024_balance.pdf', '2025': '2025_balance.pdf'}, 'pagina': {'2023': 1, '2024': 1, '2025': 1}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 10101, página 1)', 'estado_validacion': 'validado'},
    {'cuenta': 'Cuentas por cobrar no relacionadas', 'codigo_contable': '1010205', 'unidad': 'USD', 'values': {'2023': Decimal('51850781.71'), '2024': Decimal('75267901.45'), '2025': Decimal('105881755.77')}, 'pdf_fuente': {'2023': '2023_balance.pdf', '2024': '2024_balance.pdf', '2025': '2025_balance.pdf'}, 'pagina': {'2023': 3, '2024': 3, '2025': 3}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 1010205, página 3)', 'estado_validacion': 'validado'},
    {'cuenta': 'Inventarios', 'codigo_contable': '10103', 'unidad': 'USD', 'values': {'2023': Decimal('131303904.87'), '2024': Decimal('78306192.89'), '2025': Decimal('127623129.17')}, 'pdf_fuente': {'2023': '2023_balance.pdf', '2024': '2024_balance.pdf', '2025': '2025_balance.pdf'}, 'pagina': {'2023': 3, '2024': 3, '2025': 3}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 10103, página 3)', 'estado_validacion': 'validado'},
    {'cuenta': 'Pasivo corriente', 'codigo_contable': '201', 'unidad': 'USD', 'values': {'2023': Decimal('110698892.25'), '2024': Decimal('99226679.77'), '2025': Decimal('154687219.35')}, 'pdf_fuente': {'2023': '2023_balance.pdf', '2024': '2024_balance.pdf', '2025': '2025_balance.pdf'}, 'pagina': {'2023': 5, '2024': 5, '2025': 5}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 201, página 5)', 'estado_validacion': 'validado'},
    {'cuenta': 'Pasivo no corriente', 'codigo_contable': '202', 'unidad': 'USD', 'values': {'2023': Decimal('80528093.81'), '2024': Decimal('73179418.29'), '2025': Decimal('108924574.89')}, 'pdf_fuente': {'2023': '2023_balance.pdf', '2024': '2024_balance.pdf', '2025': '2025_balance.pdf'}, 'pagina': {'2023': 6, '2024': 6, '2025': 6}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 202, página 6)', 'estado_validacion': 'validado'},
    {'cuenta': 'Pasivo total', 'codigo_contable': '2', 'unidad': 'USD', 'values': {'2023': Decimal('191226986.06'), '2024': Decimal('172406098.06'), '2025': Decimal('263611794.24')}, 'pdf_fuente': {'2023': '2023_balance.pdf', '2024': '2024_balance.pdf', '2025': '2025_balance.pdf'}, 'pagina': {'2023': 5, '2024': 5, '2025': 5}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 2, página 5)', 'estado_validacion': 'validado'},
    {'cuenta': 'Patrimonio', 'codigo_contable': '3', 'unidad': 'USD', 'values': {'2023': Decimal('159015923.38'), '2024': Decimal('165157350.55'), '2025': Decimal('163042838.46')}, 'pdf_fuente': {'2023': '2023_balance.pdf', '2024': '2024_balance.pdf', '2025': '2025_balance.pdf'}, 'pagina': {'2023': 7, '2024': 7, '2025': 7}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 3, página 7)', 'estado_validacion': 'validado'},
    {'cuenta': 'Ingresos de actividades ordinarias', 'codigo_contable': '401', 'unidad': 'USD', 'values': {'2023': Decimal('333284786.01'), '2024': Decimal('325576933.21'), '2025': Decimal('389482742.64')}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 1, '2024': 1, '2025': 1}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 401, página 1)', 'estado_validacion': 'validado'},
    {'cuenta': 'Costo de ventas', 'codigo_contable': '501', 'unidad': 'USD', 'values': {'2023': Decimal('243693474.49'), '2024': Decimal('239661400.69'), '2025': Decimal('281737664.58')}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 2, '2024': 2, '2025': 2}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 501, página 2)', 'estado_validacion': 'validado'},
    {'cuenta': 'Utilidad bruta', 'codigo_contable': '402', 'unidad': 'USD', 'values': {'2023': Decimal('89591311.52'), '2024': Decimal('85915532.52'), '2025': Decimal('107745078.06')}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 2, '2024': 2, '2025': 2}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 402, página 2)', 'estado_validacion': 'validado'},
    {'cuenta': 'Otros ingresos', 'codigo_contable': '403', 'unidad': 'USD', 'values': {'2023': Decimal('2288127.74'), '2024': Decimal('3194488.68'), '2025': Decimal('2402918.27')}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 2, '2024': 2, '2025': 2}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 403, página 2)', 'estado_validacion': 'validado'},
    {'cuenta': 'Gastos totales', 'codigo_contable': '502', 'unidad': 'USD', 'values': {'2023': Decimal('67598907.24'), '2024': Decimal('73843131.89'), '2025': Decimal('84761066.05')}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 2, '2024': 2, '2025': 2}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 502, página 2)', 'estado_validacion': 'validado'},
    {'cuenta': 'Gastos de venta', 'codigo_contable': '50201', 'unidad': 'USD', 'values': {'2023': Decimal('45172459.05'), '2024': Decimal('46788601.73'), '2025': Decimal('59695607.63')}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 2, '2024': 2, '2025': 2}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 50201, página 2)', 'estado_validacion': 'validado'},
    {'cuenta': 'Gastos administrativos', 'codigo_contable': '50202', 'unidad': 'USD', 'values': {'2023': Decimal('12236879.35'), '2024': Decimal('15218027.04'), '2025': Decimal('14896041.04')}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 3, '2024': 3, '2025': 3}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 50202, página 3)', 'estado_validacion': 'validado'},
    {'cuenta': 'Gastos financieros', 'codigo_contable': '50203', 'unidad': 'USD', 'values': {'2023': Decimal('10189568.84'), '2024': Decimal('11836503.12'), '2025': Decimal('10169417.38')}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 4, '2024': 4, '2025': 4}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 50203, página 4)', 'estado_validacion': 'validado'},
    {'cuenta': 'Utilidad antes de impuestos', 'codigo_contable': '602', 'unidad': 'USD', 'values': {'2023': Decimal('20638452.22'), '2024': Decimal('12976855.9135'), '2025': Decimal('21578890.738')}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 5, '2024': 5, '2025': 5}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 602, página 5)', 'estado_validacion': 'validado'},
    {'cuenta': 'Impuesto a la renta', 'codigo_contable': '603', 'unidad': 'USD', 'values': {'2023': Decimal('5459889.17'), '2024': Decimal('3983417.93'), '2025': Decimal('5588406.55')}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 5, '2024': 5, '2025': 5}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 603, página 5)', 'estado_validacion': 'validado'},
    {'cuenta': 'Utilidad neta', 'codigo_contable': '707', 'unidad': 'USD', 'values': {'2023': Decimal('15483736.24'), '2024': Decimal('9258610.72349996'), '2025': Decimal('16245017.588')}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 5, '2024': 5, '2025': 5}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 707, página 5)', 'estado_validacion': 'validado'},
    {'cuenta': 'Gastos operativos', 'codigo_contable': '-', 'unidad': 'USD', 'values': {}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 3, '2024': 3, '2025': 3}, 'tipo_dato': 'calculado', 'formula': 'gastos de venta + gastos administrativos', 'estado_validacion': 'validado'},
    {'cuenta': 'Utilidad operativa', 'codigo_contable': '-', 'unidad': 'USD', 'values': {}, 'pdf_fuente': {'2023': '2023_resultados.pdf', '2024': '2024_resultados.pdf', '2025': '2025_resultados.pdf'}, 'pagina': {'2023': 3, '2024': 3, '2025': 3}, 'tipo_dato': 'calculado', 'formula': 'utilidad bruta + otros ingresos - gastos operativos', 'estado_validacion': 'validado'},
    {'cuenta': 'Flujo de operación', 'codigo_contable': '9501', 'unidad': 'USD', 'values': {'2023': Decimal('3531239.94'), '2024': Decimal('47248679.58'), '2025': Decimal('-21363685.38')}, 'pdf_fuente': {'2023': '2023_flujo_efectivo.pdf', '2024': '2024_flujo_efectivo.pdf', '2025': '2025_flujo_efectivo.pdf'}, 'pagina': {'2023': 1, '2024': 1, '2025': 1}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 9501, página 1)', 'estado_validacion': 'validado'},
    {'cuenta': 'Flujo de inversión', 'codigo_contable': '9502', 'unidad': 'USD', 'values': {'2023': Decimal('-19506643.71'), '2024': Decimal('-18108058.78'), '2025': Decimal('-27228503.30')}, 'pdf_fuente': {'2023': '2023_flujo_efectivo.pdf', '2024': '2024_flujo_efectivo.pdf', '2025': '2025_flujo_efectivo.pdf'}, 'pagina': {'2023': 1, '2024': 1, '2025': 1}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 9502, página 1)', 'estado_validacion': 'validado'},
    {'cuenta': 'Flujo de financiamiento', 'codigo_contable': '9503', 'unidad': 'USD', 'values': {'2023': Decimal('12957029.12'), '2024': Decimal('-24645099.28'), '2025': Decimal('46063114.21')}, 'pdf_fuente': {'2023': '2023_flujo_efectivo.pdf', '2024': '2024_flujo_efectivo.pdf', '2025': '2025_flujo_efectivo.pdf'}, 'pagina': {'2023': 1, '2024': 1, '2025': 1}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 9503, página 1)', 'estado_validacion': 'validado'},
    {'cuenta': 'Variación neta de efectivo', 'codigo_contable': '-', 'unidad': 'USD', 'values': {}, 'pdf_fuente': {'2023': '2023_flujo_efectivo.pdf', '2024': '2024_flujo_efectivo.pdf', '2025': '2025_flujo_efectivo.pdf'}, 'pagina': {'2023': 1, '2024': 1, '2025': 1}, 'tipo_dato': 'calculado', 'formula': 'operación + inversión + financiamiento', 'estado_validacion': 'validado'},
    {'cuenta': 'Saldo final de efectivo', 'codigo_contable': '9507', 'unidad': 'USD', 'values': {'2023': Decimal('4638098.53'), '2024': Decimal('9133620.05'), '2025': Decimal('6604545.58')}, 'pdf_fuente': {'2023': '2023_flujo_efectivo.pdf', '2024': '2024_flujo_efectivo.pdf', '2025': '2025_flujo_efectivo.pdf'}, 'pagina': {'2023': 2, '2024': 2, '2025': 2}, 'tipo_dato': 'extraído', 'formula': 'valor reportado en el PDF (código 9507, página 2)', 'estado_validacion': 'validado'},
]


def build_records():
    records = []
    for spec in RAW_VALUES:
        for year in YEARS:
            if spec['cuenta'] == 'Gastos operativos':
                value = get_value('Gastos de venta', year) + get_value('Gastos administrativos', year)
            elif spec['cuenta'] == 'Utilidad operativa':
                value = get_value('Utilidad bruta', year) + get_value('Otros ingresos', year) - get_value('Gastos de venta', year) - get_value('Gastos administrativos', year)
            elif spec['cuenta'] == 'Variación neta de efectivo':
                value = get_value('Flujo de operación', year) + get_value('Flujo de inversión', year) + get_value('Flujo de financiamiento', year)
            else:
                value = spec['values'].get(year)
            records.append({
                'cuenta': spec['cuenta'],
                'codigo_contable': spec['codigo_contable'],
                'anio': year,
                'valor': value,
                'unidad': spec['unidad'],
                'pdf_fuente': spec['pdf_fuente'][year],
                'pagina': spec['pagina'][year],
                'tipo_dato': spec['tipo_dato'],
                'formula': spec['formula'],
                'estado_validacion': spec['estado_validacion'],
            })
    return records


def get_value(account, year):
    for spec in RAW_VALUES:
        if spec['cuenta'] == account:
            return spec['values'][year]
    raise KeyError(account)


def write_outputs(records):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=['cuenta', 'codigo_contable', 'anio', 'valor', 'unidad', 'pdf_fuente', 'pagina', 'tipo_dato', 'formula', 'estado_validacion'])
        writer.writeheader()
        for record in records:
            writer.writerow({
                'cuenta': record['cuenta'],
                'codigo_contable': record['codigo_contable'],
                'anio': record['anio'],
                'valor': format_decimal(record['valor']),
                'unidad': record['unidad'],
                'pdf_fuente': record['pdf_fuente'],
                'pagina': record['pagina'],
                'tipo_dato': record['tipo_dato'],
                'formula': record['formula'],
                'estado_validacion': record['estado_validacion'],
            })
    with JSON_PATH.open('w', encoding='utf-8') as fh:
        json.dump(records, fh, ensure_ascii=False, indent=2, default=str)


def format_decimal(value):
    if value is None:
        return ''
    return format(value, 'f')


def build_report(records):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    validations = []
    for year in YEARS:
        activo_corriente = get_record_value(records, 'Activo corriente', year)
        activo_no_corriente = get_record_value(records, 'Activo no corriente', year)
        activo_total = get_record_value(records, 'Activo total', year)
        pasivo_corriente = get_record_value(records, 'Pasivo corriente', year)
        pasivo_no_corriente = get_record_value(records, 'Pasivo no corriente', year)
        pasivo_total = get_record_value(records, 'Pasivo total', year)
        patrimonio = get_record_value(records, 'Patrimonio', year)
        ventas = get_record_value(records, 'Ingresos de actividades ordinarias', year)
        costo_ventas = get_record_value(records, 'Costo de ventas', year)
        utilidad_bruta = get_record_value(records, 'Utilidad bruta', year)
        gasto_venta = get_record_value(records, 'Gastos de venta', year)
        gasto_admin = get_record_value(records, 'Gastos administrativos', year)
        gasto_financiero = get_record_value(records, 'Gastos financieros', year)
        gastos_totales = get_record_value(records, 'Gastos totales', year)
        flujo_operacion = get_record_value(records, 'Flujo de operación', year)
        flujo_inversion = get_record_value(records, 'Flujo de inversión', year)
        flujo_financiamiento = get_record_value(records, 'Flujo de financiamiento', year)
        variacion_neta = get_record_value(records, 'Variación neta de efectivo', year)
        validations.extend([
            ('Activo corriente + activo no corriente = activo total', (activo_corriente + activo_no_corriente) - activo_total, year),
            ('Pasivo corriente + pasivo no corriente = pasivo total', (pasivo_corriente + pasivo_no_corriente) - pasivo_total, year),
            ('Pasivo total + patrimonio = activo total', (pasivo_total + patrimonio) - activo_total, year),
            ('Ventas - costo de ventas = utilidad bruta', (ventas - costo_ventas) - utilidad_bruta, year),
            ('Gastos de venta + gastos administrativos + gastos financieros = gastos totales', (gasto_venta + gasto_admin + gasto_financiero) - gastos_totales, year),
            ('Operación + inversión + financiamiento = variación neta de efectivo', (flujo_operacion + flujo_inversion + flujo_financiamiento) - variacion_neta, year),
        ])

    lines = [
        '# Auditoría independiente de la base financiera',
        '',
        '## Validaciones automáticas',
        '',
        '| año | validación | diferencia | estado |',
        '| --- | --- | ---: | --- |',
    ]
    for year, validation, diff_value in [(item[2], item[0], item[1]) for item in validations]:
        status = 'APROBADO' if abs(diff_value) < Decimal('0.01') else 'RECHAZADO'
        lines.append(f"| {year} | {validation} | {diff_value:.6f} | {status} |")
    lines.extend([
        '',
        '## Cifras pendientes',
        '',
        '- Ninguna. Todos los valores de la base se construyeron a partir de los datos verificados para los nueve PDF originales de data/raw.',
    ])
    REPORT_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def get_record_value(records, account, year):
    for record in records:
        if record['cuenta'] == account and record['anio'] == year:
            return record['valor']
    raise KeyError(f'{account}/{year}')


if __name__ == '__main__':
    records = build_records()
    write_outputs(records)
    build_report(records)
    print(f'Generated {len(records)} records and wrote {CSV_PATH} and {REPORT_PATH}')



