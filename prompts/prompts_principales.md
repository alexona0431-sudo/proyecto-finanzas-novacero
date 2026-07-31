# Prompts principales del sistema multiagente

Los siguientes prompts resumen las instrucciones principales utilizadas durante el desarrollo. Cada agente debía trabajar únicamente con datos verificables, identificar los supuestos y entregar resultados revisables.

## 1. Agente coordinador

> Organiza el proyecto final de Novacero según la rúbrica del profesor. Divide el trabajo entre agentes económicos, financieros, de datos, ingeniería económica, valoración, riesgo y visualización. Verifica que cada producto tenga fuentes, cálculos reproducibles y validación humana. No aceptes datos inventados.

## 2. Agente de investigación económica

> Analiza el entorno macroeconómico, sectorial y energético relacionado con Novacero y una ampliación fotovoltaica en Lasso. Utiliza fuentes oficiales como BCE, INEC, ARCONEL, Superintendencia de Compañías y documentos institucionales de Novacero. Cita cada fuente y separa los hechos de las inferencias.

## 3. Agente de datos

> Extrae las partidas financieras de los PDF de Novacero correspondientes a 2023, 2024 y 2025. Conserva cuenta, código, año, valor, unidad, PDF, página, tipo de dato, fórmula y estado de validación. No completes valores inciertos. Genera CSV, JSON y diccionario.

## 4. Agente auditor

> Revisa la base financiera contra los PDF originales. Comprueba las igualdades de activo, pasivo, patrimonio, resultados y flujos. Registra diferencias, errores y correcciones. Rechaza cualquier cifra que no tenga una fuente verificable.

## 5. Agente financiero

> Calcula liquidez, prueba ácida, efectivo, endeudamiento, deuda/patrimonio, márgenes, ROA, ROE, cobertura de intereses, rotaciones y sistema DuPont. Explica la evolución 2023-2025 y qué decisiones permite sustentar. Deja fórmulas y resultados reproducibles.

## 6. Agente de ingeniería económica

> Construye el flujo de caja de una ampliación fotovoltaica de 1.000 kWp. Identifica la inversión, generación, autoconsumo, tarifa evitada, mantenimiento, degradación, impuestos, depreciación, reemplazo del inversor, valor residual y financiamiento. Calcula VAN, TIR, beneficio/costo, payback simple y descontado. Compara recursos propios, crédito y no invertir.

## 7. Agente de riesgo

> Elabora escenarios optimista, base y pesimista. Calcula sensibilidad frente a inversión, generación, tarifa, autoconsumo y tasa de descuento. Determina puntos de equilibrio y construye una matriz con probabilidad, impacto y tratamiento.

## 8. Agente de valoración

> Estima el valor patrimonial de Novacero mediante FCFE como método principal y valor contable ajustado como contraste. Explica los supuestos, la diferencia entre métodos, la política de dividendos o reinversión y los riesgos de control corporativo.

## 9. Agente de visualización

> Construye un dashboard en Next.js que muestre el desafío, entorno económico, estados financieros, razones, flujo proyectado, VAN, TIR, B/C, recuperación, WACC, alternativas, escenarios, sensibilidad, valoración, riesgos, fuentes, fecha y recomendación. Incluye interpretación, interacción y diseño adaptable a celulares.

## 10. Prompt de revisión final

> Audita el proyecto completo contra la rúbrica. Verifica que los enlaces funcionen, los cálculos se reproduzcan, los datos simulados estén identificados, las fuentes estén citadas y la recomendación se derive de los resultados. Señala cualquier elemento obligatorio faltante antes de la entrega.
