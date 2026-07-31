# Análisis económico y financiero de Novacero

Proyecto integrador de análisis económico, finanzas corporativas e ingeniería económica desarrollado mediante una arquitectura multiagente.

## Enlaces públicos

- **Dashboard:** [https://proyecto-finanzas-novacero.vercel.app](https://proyecto-finanzas-novacero.vercel.app)
- **Repositorio:** [https://github.com/alexona0431-sudo/proyecto-finanzas-novacero](https://github.com/alexona0431-sudo/proyecto-finanzas-novacero)

## Desafío

Evaluar si es económica y financieramente viable ampliar la capacidad de generación fotovoltaica de Novacero mediante un sistema adicional de 1.000 kWp en la planta Lasso, comparando tres alternativas:

1. Financiar la inversión con recursos propios.
2. Utilizar 30 % de recursos propios y 70 % de crédito bancario.
3. No realizar la inversión.

La evaluación utiliza información financiera pública de 2023, 2024 y 2025. Los datos técnicos que no están disponibles públicamente se identifican expresamente como supuestos académicos.

## Resultado principal

El escenario base presenta:

| Indicador | Resultado |
| --- | ---: |
| Inversión inicial | USD 850.000 |
| VAN del proyecto | USD -66.057,81 |
| TIR | 8,91 % |
| Relación beneficio/costo | 0,943 |
| Recuperación simple | 10,07 años |
| Recuperación descontada | No recuperado |
| WACC | 7,38 % |

La recomendación es **no ejecutar todavía el diseño base**. Se propone negociar, validar y rediseñar el proyecto antes de invertir. La evaluación deberá actualizarse con cotizaciones, facturas eléctricas y curvas horarias reales.

## Condiciones aproximadas de equilibrio

- Inversión máxima: USD 785.851,61.
- Tarifa evitada mínima: USD 0,0919 por kWh.
- Autoconsumo mínimo: 97,35 %.

## Contenido del análisis

- Entorno económico, sectorial y energético.
- Estados financieros 2023-2025.
- Análisis horizontal, razones financieras e interpretación.
- Liquidez, endeudamiento, eficiencia y rentabilidad.
- Cobertura de intereses y sistema DuPont.
- Flujo de caja proyectado a 20 años.
- Financiamiento propio y bancario.
- Costo de deuda, costo del patrimonio y WACC.
- VAN, TIR, beneficio/costo y recuperación.
- Escenarios optimista, base y pesimista.
- Sensibilidad y puntos de equilibrio.
- Matriz de riesgos.
- Valoración mediante FCFE.
- Valor contable ajustado como contraste.
- Dividendos, reinversión y control corporativo.
- Recomendación ejecutiva.

## Fuentes

- Superintendencia de Compañías, Valores y Seguros.
- Banco Central del Ecuador.
- Instituto Nacional de Estadística y Censos.
- Agencia de Regulación y Control de Electricidad.
- Servicio de Rentas Internas.
- Información institucional y memorias de sostenibilidad de Novacero.

Los PDF financieros originales se conservan en `data/raw/`. La base procesada incluye trazabilidad por cuenta, año, documento y página.

## Arquitectura multiagente

| Agente | Responsabilidad |
| --- | --- |
| Coordinador | Divide el problema, integra resultados y revisa la rúbrica |
| Investigación económica | Analiza el entorno macroeconómico, sectorial y energético |
| Datos | Extrae, limpia, documenta y valida las bases |
| Financiero | Calcula razones, flujos, financiamiento y WACC |
| Ingeniería económica | Calcula VAN, TIR, B/C, recuperación y sensibilidad |
| Valoración | Estima el valor empresarial mediante dos métodos |
| Riesgo y auditoría | Revisa supuestos, cálculos, diferencias y riesgos |
| Visualización | Construye y verifica el dashboard |

Las reglas de coordinación y validación se documentan en `AGENTS.md`. Las instrucciones específicas de cada agente se encuentran en `agents/`.

## Estructura principal

```text
proyecto-finanzas-novacero/
├── README.md
├── AGENTS.md
├── agents/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── project/
│   └── diccionario_datos.md
├── docs/
├── evidence/
├── notebooks/
├── prompts/
├── reports/
├── src/
│   ├── analysis/
│   ├── app/
│   ├── dashboard/
│   └── models/
└── tests/
```

## Requisitos

- Node.js 20 o superior.
- npm.
- Python 3.10 o superior.
- Git.

## Instalación

Clone el repositorio:

```bash
git clone https://github.com/alexona0431-sudo/proyecto-finanzas-novacero.git
cd proyecto-finanzas-novacero
```

Instale las dependencias de Python:

```bash
python -m pip install -r requirements.txt
```

Instale las dependencias del dashboard:

```bash
npm install
```

En PowerShell con ejecución de scripts restringida puede utilizarse:

```powershell
npm.cmd install
```

## Reproducción de los cálculos

Ejecute los scripts en este orden:

```bash
python src/analysis/extract_finanzas.py
python src/analysis/auditar_base_financiera.py
python src/analysis/calcular_indicadores_financieros.py
python src/analysis/calcular_eficiencia_dupont.py
python src/analysis/calcular_proyecto_fotovoltaico.py
python src/analysis/analizar_riesgo_sensibilidad.py
python src/analysis/valorar_empresa.py
```

Los resultados se generan en:

- `data/processed/`: bases, indicadores, flujos, escenarios y valoración.
- `reports/`: auditoría, diagnóstico, ingeniería económica, riesgos y valoración.

## Ejecución del dashboard

```bash
npm run dev
```

En PowerShell:

```powershell
npm.cmd run dev
```

Abra [http://localhost:3000](http://localhost:3000).

Para comprobar la versión de producción:

```bash
npm run build
```

## Evidencias de inteligencia artificial

La carpeta `evidence/` contiene:

- Herramientas utilizadas.
- Registro de tareas de los agentes.
- Respuestas aceptadas, corregidas y rechazadas.
- Errores identificados.
- Validaciones de cálculos.
- Decisiones tomadas por el estudiante.
- Reflexión sobre las limitaciones de la IA.
- Capturas del proceso.

Los prompts principales se encuentran en `prompts/prompts_principales.md`.

## Supuestos y limitaciones

- No se dispone de facturas eléctricas ni curvas horarias de carga de la planta Lasso.
- La tarifa eléctrica, generación, autoconsumo, inversión y mantenimiento son supuestos académicos sujetos a validación.
- La tasa bancaria utilizada es una referencia del segmento productivo corporativo y no una oferta dirigida a Novacero.
- La valoración empresarial es académica y no constituye una oferta o tasación profesional.
- La información pública confirma experiencia fotovoltaica previa en Novacero; por ello, el proyecto se presenta como ampliación o sistema adicional.

## Autoría y responsabilidad

El estudiante es responsable de la selección del desafío, los supuestos, la validación de las fuentes, la interpretación financiera y la recomendación final. La inteligencia artificial fue utilizada como apoyo para organizar, programar, revisar y documentar el proyecto.

## Licencia

Consulte el archivo `LICENSE`.
