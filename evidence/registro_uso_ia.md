# Registro del uso de inteligencia artificial

## 1. Objetivo

Utilizar inteligencia artificial como apoyo para organizar agentes especializados, procesar datos financieros verificables, construir modelos reproducibles, revisar errores y desarrollar un dashboard que permita evaluar una ampliación fotovoltaica de 1.000 kWp en la planta Lasso de Novacero.

## 2. Registro de tareas

| Etapa | Agente responsable | Tarea asignada | Producto | Validación humana |
| --- | --- | --- | --- | --- |
| Coordinación | Coordinador | Dividir el proyecto según la rúbrica y ordenar las actividades | Plan de trabajo y estructura del repositorio | Se verificó que incluyera todos los productos solicitados |
| Investigación | Investigador económico | Consultar BCE, INEC, ARCONEL, Superintendencia y fuentes de Novacero | Análisis económico, sectorial y energético | Se conservaron únicamente fuentes oficiales o institucionales |
| Datos | Analista de datos | Extraer y organizar estados financieros 2023-2025 | CSV, JSON y diccionario | Se compararon cuentas y valores con nueve PDF originales |
| Auditoría | Riesgo y auditoría | Verificar igualdades contables y detectar inconsistencias | Reporte de auditoría | Se ejecutaron 18 comprobaciones automáticas |
| Finanzas | Analista financiero | Calcular liquidez, deuda, rentabilidad, eficiencia, cobertura y DuPont | Indicadores y diagnóstico | Se revisaron fórmulas, unidades y evolución anual |
| Ingeniería económica | Ingeniería económica | Construir flujos y calcular VAN, TIR, B/C y recuperación | Flujo y reporte de inversión | Se aceptó el VAN negativo porque era coherente con los supuestos |
| Financiamiento | Analista financiero | Comparar recursos propios, crédito y no invertir; calcular WACC | Comparación financiera | La tasa del crédito se identificó como referencia del BCE |
| Riesgo | Riesgo y auditoría | Construir escenarios, sensibilidad, equilibrio y matriz de riesgos | Reporte de riesgo | Se comprobó la coherencia entre escenarios y recomendación |
| Valoración | Valoración | Aplicar FCFE y valor contable ajustado | Valoración empresarial | Los supuestos fueron identificados como académicos |
| Visualización | Visualización | Construir el dashboard interactivo | Dashboard Next.js | Se revisó visualmente y se comprobó su compilación |
| Despliegue | Coordinador | Publicar el repositorio y el dashboard | GitHub y Vercel | Se abrió el enlace público y se comprobó el estado de producción |

## 3. Respuestas aceptadas

- La estructura multiagente con ocho agentes especializados.
- La extracción de los estados financieros después de la auditoría independiente.
- Los 33 indicadores del diagnóstico financiero.
- Los 27 indicadores de eficiencia, cobertura y DuPont.
- Los resultados de ingeniería económica que mostraron VAN negativo en el escenario base.
- Los escenarios optimista, base y pesimista.
- La valoración mediante FCFE y valor contable ajustado.
- El diseño del dashboard después de verificar su contenido y funcionamiento.

## 4. Respuestas corregidas

### Nombre de una cuenta

El código buscaba `Cuentas por cobrar`, pero la base utilizaba `Cuentas por cobrar no relacionadas`. Se corrigió el alias antes de generar los indicadores de eficiencia.

### Codificación de caracteres

Una edición con PowerShell produjo textos como `MetodologÃa`. El archivo fue reemplazado por una versión UTF-8 correcta y el reporte volvió a generarse.

### Ejecución de npm

PowerShell bloqueó `npm.ps1` por su política de ejecución. Se utilizó `npm.cmd`, evitando modificar la configuración de seguridad del equipo.

### Definición del desafío

La Memoria de Sostenibilidad 2025 menciona que Novacero ya implementó una planta fotovoltaica. Por ello, el desafío se corrigió y se presentó como evaluación de una ampliación o sistema adicional de 1.000 kWp en Lasso.

### Contenido del dashboard

La primera versión no mostraba explícitamente indicadores macroeconómicos ni el flujo de caja proyectado. Ambos elementos fueron incorporados antes del despliegue.

## 5. Respuestas rechazadas

- La primera extracción automática que dejó partidas incompletas o sin trazabilidad suficiente.
- Cualquier valor que no pudiera verificarse en los PDF originales.
- La idea de presentar los supuestos técnicos del sistema fotovoltaico como datos reales de Novacero.
- La recomendación de invertir solo por razones ambientales sin comprobar VAN, TIR y riesgo.
- La posibilidad de forzar el resultado para obtener un VAN positivo.

## 6. Errores identificados durante el proceso

- Falta de espacio durante la primera instalación de dependencias.
- Bloqueo de scripts de npm en PowerShell.
- Error `KeyError` por cuentas calculadas sin valores almacenados.
- Error de serialización de valores `Decimal` en JSON.
- Diferencias entre nombres de cuentas contables.
- Problemas de codificación UTF-8.
- Necesidad de distinguir datos reales, datos calculados y supuestos académicos.
- Necesidad de reformular el proyecto como ampliación fotovoltaica.

## 7. Validaciones realizadas

- Activo corriente + activo no corriente = activo total.
- Pasivo corriente + pasivo no corriente = pasivo total.
- Pasivo total + patrimonio = activo total.
- Ventas - costo de ventas = utilidad bruta.
- Gastos de venta + administrativos + financieros = gastos totales.
- Flujo de operación + inversión + financiamiento = variación neta de efectivo.
- Comparación de VAN y TIR con la tasa de descuento.
- Confirmación de puntos de equilibrio mediante sensibilidad.
- Compilación de producción del dashboard en Next.js.
- Confirmación del despliegue público en Vercel.

## 8. Resultado

La IA se utilizó como herramienta de apoyo y no como sustituto del criterio del estudiante. Las decisiones finales se basaron en datos verificados, cálculos reproducibles, revisión humana y reconocimiento explícito de las limitaciones.
