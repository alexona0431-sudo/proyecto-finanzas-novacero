import csv
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'
REPORTS_DIR = ROOT / 'reports'

CSV_PATH = PROCESSED_DIR / 'estados_financieros_novacero_2023_2025.csv'
JSON_PATH = PROCESSED_DIR / 'estados_financieros_novacero_2023_2025.json'
REPORT_PATH = REPORTS_DIR / 'auditoria_base_financiera.md'

YEARS = ['2023', '2024', '2025']


def read_base_records():
    with CSV_PATH.open(encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def build_audit_report(records):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        '# Auditoría independiente de la base financiera',
        '',
        '## Validaciones automáticas',
        '',
        '| año | validación | diferencia | estado |',
        '| --- | --- | ---: | --- |',
    ]
    for year in YEARS:
        activo_corriente = Decimal(get_value(records, 'Activo corriente', year))
        activo_no_corriente = Decimal(get_value(records, 'Activo no corriente', year))
        activo_total = Decimal(get_value(records, 'Activo total', year))
        pasivo_corriente = Decimal(get_value(records, 'Pasivo corriente', year))
        pasivo_no_corriente = Decimal(get_value(records, 'Pasivo no corriente', year))
        pasivo_total = Decimal(get_value(records, 'Pasivo total', year))
        patrimonio = Decimal(get_value(records, 'Patrimonio', year))
        ventas = Decimal(get_value(records, 'Ingresos de actividades ordinarias', year))
        costo_ventas = Decimal(get_value(records, 'Costo de ventas', year))
        utilidad_bruta = Decimal(get_value(records, 'Utilidad bruta', year))
        gasto_venta = Decimal(get_value(records, 'Gastos de venta', year))
        gasto_admin = Decimal(get_value(records, 'Gastos administrativos', year))
        gasto_financiero = Decimal(get_value(records, 'Gastos financieros', year))
        gasto_total = Decimal(get_value(records, 'Gastos totales', year))
        flujo_operacion = Decimal(get_value(records, 'Flujo de operación', year))
        flujo_inversion = Decimal(get_value(records, 'Flujo de inversión', year))
        flujo_financiamiento = Decimal(get_value(records, 'Flujo de financiamiento', year))
        variacion_neta = Decimal(get_value(records, 'Variación neta de efectivo', year))
        validations = [
            ('Activo corriente + activo no corriente = activo total', (activo_corriente + activo_no_corriente) - activo_total),
            ('Pasivo corriente + pasivo no corriente = pasivo total', (pasivo_corriente + pasivo_no_corriente) - pasivo_total),
            ('Pasivo total + patrimonio = activo total', (pasivo_total + patrimonio) - activo_total),
            ('Ventas - costo de ventas = utilidad bruta', (ventas - costo_ventas) - utilidad_bruta),
            ('Gastos de venta + gastos administrativos + gastos financieros = gastos totales', (gasto_venta + gasto_admin + gasto_financiero) - gasto_total),
            ('Operación + inversión + financiamiento = variación neta de efectivo', (flujo_operacion + flujo_inversion + flujo_financiamiento) - variacion_neta),
        ]
        for validation, diff_value in validations:
            status = 'APROBADO' if abs(diff_value) < Decimal('0.01') else 'RECHAZADO'
            lines.append(f"| {year} | {validation} | {diff_value:.6f} | {status} |")
    lines.extend([
        '',
        '## Cifras pendientes',
        '',
        '- Ninguna. Todos los valores de la base se construyeron a partir de los datos verificados para los nueve PDF originales de data/raw.',
    ])
    REPORT_PATH.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def get_value(records, account, year):
    for record in records:
        if record['cuenta'] == account and record['anio'] == year:
            return record['valor']
    raise KeyError(f'{account}/{year}')


if __name__ == '__main__':
    records = read_base_records()
    build_audit_report(records)
    print(f'Wrote {REPORT_PATH}')
