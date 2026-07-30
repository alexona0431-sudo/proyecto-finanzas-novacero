# Evaluación económica y financiera de un sistema fotovoltaico para Novacero S.A.

## Descripción del proyecto
Este repositorio documenta la fase inicial de un proyecto académico orientado a responder si es económica y financieramente viable que Novacero S.A. implemente un sistema fotovoltaico en su planta industrial de Lasso mediante financiamiento bancario. El enfoque es metodológico, académico y de análisis técnico-financiero.

## Pregunta del desafío
¿Es económica y financieramente viable que Novacero S.A. implemente un sistema fotovoltaico en su planta industrial de Lasso mediante financiamiento bancario?

## Objetivos
- Construir una estructura de trabajo multiagente que cubra los requisitos obligatorios del curso.
- Organizar la documentación, los supuestos, las fuentes y la evidencia del proceso.
- Preparar la base para futuras evaluaciones económicas, financieras, de valoración y de riesgo.
- Mantener un marco ético y verificable, sin inventar cifras ni resultados no sustentados.

## Tecnologías utilizadas
- Next.js para la base de la aplicación web.
- JavaScript y React en la capa de interfaz.
- Python para análisis de datos, notebooks y procesamiento inicial.
- Markdown para documentación, prompts y evidencia del proceso.

## Estructura de carpetas
- agents/: definiciones de rol y tareas para cada agente del sistema multiagente.
- data/: diccionario de datos, datos originales y datos limpios para el análisis.
- docs/: documentos de apoyo y referencias del proyecto.
- evidence/: registro de decisiones, validaciones, revisiones de IA y limitaciones del proceso.
- prompts/: plantillas de prompts para guiar el análisis.
- public/: recursos estáticos del proyecto.
- src/: base de la aplicación; por ahora se conserva sin modificaciones en esta fase.
- tests/: espacio para pruebas futuras.

## Instrucciones de instalación y ejecución
### Requisitos previos
- Node.js 18 o superior.
- Python 3.10 o superior.

### Instalar dependencias de la app web
```bash
npm install
```

### Ejecutar la aplicación en desarrollo
```bash
npm run dev
```

### Instalar dependencias de Python
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Fuentes previstas
- Documentación técnica y operativa del sistema fotovoltaico.
- Información de costos, consumo energético y condiciones de mercado relevantes.
- Fuentes regulatorias, sectoriales y financieras que puedan sustentar supuestos y comparativos.
- Fuentes oficiales como BCE, INEC, SRI, Superintendencia de Compañías y Novacero.

## Estado actual del proyecto
La fase actual corresponde a documentación y configuración inicial. No se ha construido el dashboard ni se han modificado los archivos de la carpeta src. La documentación ya incorpora los elementos de análisis financiero, valoración, riesgos y dashboard exigidos por el curso.
