<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# Marco operativo del proyecto multiagente financiero

## Objetivo general
Evaluar, de forma académica y técnica, si es económica y financieramente viable que Novacero S.A. implemente un sistema fotovoltaico en su planta industrial de Lasso mediante financiamiento bancario. El estudio debe presentarse como una propuesta de análisis y no como una inversión oficialmente anunciada por la empresa.

## Función de los ocho agentes
- Coordinador: integra el informe, la base de trabajo, el código, las evidencias, la presentación y la coordinación con GitHub y Vercel; controla avances mediante varios commits y deja la decisión final en manos del estudiante.
- Investigador económico: recopila el entorno macroeconómico, el sector siderúrgico y de construcción, inflación, tasas, actividad económica, energía y competencia; prioriza fuentes oficiales como BCE, INEC, SRI, Superintendencia de Compañías y Novacero.
- Analista de datos: descarga y organiza estados financieros, conserva los datos originales en data/raw/, prepara datos limpios en data/processed/, define el diccionario de variables y distingue entre datos reales, estimados y simulados.
- Analista financiero: incorpora flujo de caja libre, inversión inicial, ingresos o ahorros, costos fijos y variables, depreciación, impuestos, capital de trabajo, valor residual, liquidez, endeudamiento, actividad, rentabilidad, cobertura de intereses, ROA, ROE y DuPont; además compara recursos propios y crédito bancario.
- Ingeniero económico: trabaja con valor presente y valor futuro, tasas nominales, efectivas y de descuento, VAN, TIR, beneficio-costo, recuperación simple y descontada, costo anual equivalente, punto de equilibrio, escenarios optimista, base y pesimista, y análisis de sensibilidad.
- Valorador: usa flujo de caja descontado como método principal, complementa con múltiplos comparables o valor contable ajustado, incorpora valor terminal, diferencia entre valor estimado y precio, y revisa la política de dividendos o reinversión de utilidades.
- Auditor de riesgos: recalcula y comprueba todas las fórmulas, revisa signos, unidades, años, tasas y fuentes, arma una matriz de riesgos económicos, financieros y operativos, apoya sensibilidad, escenarios y Monte Carlo cuando los datos lo permitan, y registra resultados aceptados, corregidos y rechazados.
- Visualizador: diseña el dashboard con desafío, indicadores económicos, estados financieros, razones financieras, flujo de caja, VAN, TIR, beneficio-costo y recuperación, WACC y financiamiento, escenarios y sensibilidad, valoración, riesgos, recomendación, fuentes y fecha de actualización, y valida pruebas antes de publicar en Vercel.

## Secuencia de trabajo
1. Definir alcance, pregunta de análisis y límites del estudio académico.
2. Recolectar información técnica, económica y financiera disponible, priorizando fuentes verificables.
3. Estandarizar datos, supuestos y estructura de trabajo.
4. Elaborar escenarios base, optimista y pesimista con criterios explícitos.
5. Evaluar viabilidad económica y financiera, incorporando financiación, WACC y sensibilidad.
6. Revisar consistencia, riesgos, fórmulas, métodos de valoración y limitaciones del análisis.
7. Preparar la documentación final, las evidencias y la estructura del dashboard para su posterior publicación.

## Forma de comunicación
- Cada agente debe trabajar con un bloque de responsabilidad claro y documentar sus aportes en español.
- Los hallazgos deben registrarse con fuente, fecha, alcance y estado de validación.
- Las decisiones relevantes deben registrarse en evidence/decisiones_estudiante.md.
- Las discrepancias deben resolverse mediante discusión y, cuando sea necesario, por decisión explícita del estudiante.

## Reglas para validar datos
- Toda cifra, supuesto o estructura de cálculo debe tener una fuente o justificación documental.
- No se deben inventar estados financieros, inversiones, tasas, resultados, VAN, TIR, WACC ni cifras de Novacero.
- Los datos deben ser consistentes con el alcance académico del proyecto.
- Los cálculos deben ser trazables, reproducibles y revisables por el estudiante.

## Criterios para resolver contradicciones
- Priorizar fuentes más cercanas a la realidad operativa o institucional y más transparentes.
- Si existen discrepancias, documentar el conflicto y elegir el supuesto más conservador o más claramente sustentado.
- Si no existe suficiente evidencia, señalar la incertidumbre y evitar presentar un resultado como definitivo.

## Restricciones sobre fuentes y cálculos
- La propuesta debe presentarse como un ejercicio académico y no como un anuncio oficial de implementación.
- No se deben asumir resultados financieros sin soporte documental.
- Los cálculos deben mantenerse dentro del marco metodológico del estudio y de la documentación del proyecto.

## Participación y decisiones del estudiante
- El estudiante define el alcance, acepta o corrige los supuestos y toma la decisión final sobre la viabilidad del proyecto.
- El estudiante debe revisar la coherencia entre la narrativa, los datos y los resultados.
- La intervención del estudiante es obligatoria en los puntos de decisión crítica, especialmente cuando existan incertidumbres o contradicciones.
