# Prompt RTC - Feature innovadora con agentes

[ROL]
Actua como un Desarrollador Fullstack Senior experto en FastAPI, SQLAlchemy, Pydantic, JavaScript, HTML y CSS. Tenes acceso a CONTEXT.md y FRONTEND.md, pero debes revisar el codigo fuente real antes de implementar porque la documentacion puede estar desactualizada.

[CONTEXTO]
El proyecto es un Simulador del Mundial 2026 con arquitectura Repository -> Service -> Router. La simulacion genera partidos, goles, campeon, metricas de dashboard y persiste el ultimo resultado en `services/simulation_cache.py`.

[TAREA]
Implementar una nueva funcionalidad con valor de producto: Tabla de Goleadores por Equipo.

Backend:
1. Extender la informacion cacheada de la ultima simulacion para guardar los goles asignados a jugadores, agrupados por equipo.
2. Crear schemas Pydantic para representar:
   - jugador goleador: nombre y goles
   - equipo: nombre, goles totales y lista ordenada de jugadores
3. Crear endpoint `GET /metrics/team-scorers`.
4. Si no existe simulacion previa, responder HTTP 404 con el mismo criterio que el dashboard.
5. Ordenar equipos por goles totales descendente y jugadores por goles descendente.
6. Garantizar que la suma de goles por equipo coincida con `total_goals` del dashboard.

Frontend:
1. En `static/index.html`, agregar una seccion debajo de los KPIs del dashboard.
2. Consumir `GET /metrics/team-scorers` despues de ejecutar la simulacion.
3. Mostrar cards responsive por equipo con total de goles y top jugadores.
4. Mantener la estetica CDA existente: cards limpias, azul institucional, buen espaciado y lectura mobile.

[CRITERIO]
- No inventar datos: todo debe salir de la simulacion.
- Respetar la arquitectura existente.
- No romper endpoints existentes.
- Agregar tests para endpoint, ordenamiento y consistencia de goles.
- Ejecutar `pytest -v` y dejar todo verde.
- Generar evidencia visual de la feature funcionando.

[RESULTADO ESPERADO]
La app permite simular el Mundial y ver, dentro del dashboard, una tabla clara de goleadores agrupada por equipo. La suite completa debe pasar.
