# Prompt RTC — Diagnostico de Bugs (Parte 1)

Copiar y pegar este prompt en el agente de IA.

---

[ROL]
Actua como un Desarrollador Backend Senior experto en Python, FastAPI, SQLAlchemy y Pydantic. Tenes acceso al archivo CONTEXT.md como contexto del proyecto. Usalo para entender la arquitectura, endpoints y modelos, pero **siempre verificá contra el código fuente real** porque la documentación puede tener errores.

[TAREA]
Te voy a describir 3 bugs de backend que ocurren en el Simulador del Mundial 2026. Por cada uno:
1. Identifica la causa raiz revisando el código fuente
2. Indica archivo y linea exacta donde esta el bug
3. Proponé el fix con el código corregido
4. Verifica que los tests existentes sigan pasando

Los bugs son:

**Bug 1 — Dashboard con metricas inconsistentes:**
Cuando se ejecuta la simulación, el dashboard muestra comportamientos extraños en el promedio de goles por partido (`avg_goals_per_match`). A veces da exactamente 0.0 aunque haya goles en los partidos. Otras veces, si se modifican ciertas condiciones, el valor es demasiado alto (cientos o miles). La formula de calculo del promedio parece tener varios problemas encimados. Revisar el servicio de métricas y como se persisten los datos de la simulacion.

**Bug 2 — Las metricas del dashboard no están sincronizadas con la simulacion:**
El total de partidos (`total_matches`) y el promedio de goles no reflejan correctamente lo que realmente ocurrió en el torneo. Por ejemplo, un mundial tiene 64 partidos pero el dashboard muestra un número distinto. Revisar como se calculan y almacenan las metricas al finalizar la simulacion. Podria haber un problema de cache o de calculo.

**Bug 3 — Error al actualizar datos de un usuario:**
Haciendo una prueba con `PUT /users/{id}`, si se envían solo algunos campos para actualizar (por ejemplo solo el nombre), el servidor responde con error HTTP 422. Sin embargo, enviando el cuerpo completo funciona correctamente. Revisar los schemas de validación y los handlers del endpoint de usuarios.

[CRITERIO]
- Causa raiz exacta con referencia a archivo y linea
- Los fixes deben ser consistentes con la arquitectura real del proyecto (revisar el código, no confiar ciegamente en la documentación)
- Después de cada fix, ejecutar `pytest -v` para verificar que los tests pasen
- Proponer un mensaje de commit descriptivo para cada fix
- Si la documentación no coincide con el código real, priorizar el código real
