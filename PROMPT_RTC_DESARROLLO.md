# Prompt RTC — Desarrollo de Feature (Parte 2)

Copiar y pegar este prompt en el agente de IA.

---

[ROL]
Actua como un Desarrollador Fullstack Senior experto en FastAPI, Python, JavaScript, HTML/CSS y SQLAlchemy. Tenes acceso a CONTEXT.md y FRONTEND.md como contexto del proyecto. Revisa siempre el codigo fuente real antes de implementar, ya que la documentacion puede contener errores.

[TAREA]
Se necesita agregar una nueva funcionalidad al Dashboard del Simulador del Mundial 2026: **Tabla de Goleadores por Equipo**.

## Requerimientos

### Backend
1. Crear un endpoint que devuelva, por cada equipo, la lista de sus jugadores con la cantidad de goles que hicieron en el torneo.
2. Los datos deben persistir/recuperarse de alguna fuente existente. Si no hay datos de simulacion, devolver error.
3. El endpoint debe seguir la arquitectura del proyecto.
4. Ordenar: equipos por goles totales (mayor a menor), y dentro de cada equipo los jugadores por goles (mayor a menor).

### Frontend
1. Agregar una seccion en el Dashboard debajo de las metricas actuales.
2. Mostrar los datos de forma clara, agrupando por equipo.
3. Debe verse bien tanto en desktop como en celular.

[CRITERIO]
- La implementacion debe ser consistente con el codigo real del proyecto (no confiar ciegamente en la documentacion)
- Los datos deben venir de la simulacion, no inventarse
- No romper tests existentes: ejecutar `pytest -v` al finalizar
- El diseno visual debe ser coherente con el resto del frontend
- Proponer un mensaje de commit descriptivo
