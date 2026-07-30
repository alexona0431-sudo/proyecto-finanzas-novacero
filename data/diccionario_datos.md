# Diccionario de datos del proyecto

## Propósito
Definir las variables, categorías y estructuras básicas que se usarán para organizar la información del análisis.

## Variables propuestas
- fecha_recoleccion: fecha en que se registró la fuente o dato.
- fuente: nombre o referencia de la documentación consultada.
- tipo_fuente: documental, institucional, técnica, financiera o regulatoria.
- categoria: grupo de información, por ejemplo consumo energético, costos, financiación, regulación o riesgo.
- variable: nombre de la variable específica.
- valor: dato o texto asociado.
- unidad: unidad de medida de la variable, si aplica.
- observaciones: notas aclaratorias o condiciones del dato.
- estado_validacion: pendiente, validado o rechazado.

## Estructura recomendada para tablas
- id_registro: identificador único.
- fecha_recoleccion: fecha de registro.
- fuente: referencia documental.
- tipo_fuente: categoría de la fuente.
- categoria: bloque temático.
- variable: variable concreta.
- valor: valor numérico o textual.
- unidad: unidad de medida.
- observaciones: notas de contexto.
- estado_validacion: estado de revisión.

## Reglas de uso
- Cada registro debe mantener trazabilidad a una fuente.
- No se deben incluir valores sin contexto o sin validación.
- Los datos deben ser susceptibles de revisión manual y de auditoría.
