# Diccionario de datos

## Propósito
Definir la estructura y el significado de los registros financieros que conforman la base de Novacero.

## Estructura del archivo
Cada registro representa una cuenta o partida para un año concreto y se guarda en formato largo con estas columnas:

- cuenta: nombre de la partida contable o financiera.
- codigo_contable: código contable asociado al valor cuando aplica; para cálculos derivados se usa "-".
- anio: año de la observación, 2023, 2024 o 2025.
- valor: cifra numérica, ya sea extraída directamente del PDF o calculada a partir de otras partidas.
- unidad: moneda o unidad de medida; en este estudio USD.
- pdf_fuente: nombre del archivo PDF original que sustentó la cifra.
- pagina: página del PDF que corresponde al valor reportado.
- tipo_dato: "extraído" para cifras que aparecen directamente en los PDF, o "calculado" para resultados derivados.
- formula: fórmula utilizada para el valor, ya sea el valor reportado en el PDF o la operación aritmética aplicada.
- estado_validacion: estado de revisión; en esta base se usa "validado" para todo registro.

## Cuentas incluidas
- Balance: activo corriente, activo no corriente, activo total, efectivo y equivalentes, cuentas por cobrar no relacionadas, inventarios, pasivo corriente, pasivo no corriente, pasivo total y patrimonio.
- Resultados: ingresos de actividades ordinarias, costo de ventas, utilidad bruta, otros ingresos, gastos totales, gastos de venta, gastos administrativos, gastos financieros, utilidad antes de impuestos, impuesto a la renta y utilidad neta.
- Flujo de efectivo: flujo de operación, flujo de inversión, flujo de financiamiento, variación neta de efectivo y saldo final de efectivo.
- Cálculos derivados: gastos operativos, utilidad operativa y variación neta de efectivo.

## Reglas de uso
- Cada cifra conserva trazabilidad al PDF original y a la página indicada.
- No se inventan valores; los cálculos derivados se realizan únicamente a partir de partidas verificadas.
- Las validaciones contables se ejecutan sobre los valores publicados en la base.
