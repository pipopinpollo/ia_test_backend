# Mundial 2026 Simulator — Contexto del Proyecto

## Stack Tecnologico
- Python 3.11+
- FastAPI
- PostgreSQL + SQLAlchemy 2.0
- Uvicorn
- Pydantic 2.x

## Arquitectura
El proyecto sigue el patron: **Repository -> Service -> Router**

Cada capa se comunica con la siguiente de forma unidireccional:
- `Repository` se encarga de la persistencia (CRUD contra PostgreSQL)
- `Service` contiene la logica de negocio
- `Router` expone los endpoints HTTP

**Importante:** Los servicios se comunican directamente entre si sin pasar por los repositorios. Las rutas llaman a los servicios, nunca a los repositorios.

## Endpoints Disponibles

| Metodo | Path                     | Descripcion                       |
|--------|--------------------------|-----------------------------------|
| GET    | /api/teams/              | Listar todos los equipos          |
| GET    | /api/teams/{id}          | Obtener equipo con jugadores      |
| POST   | /api/teams/              | Crear equipo                      |
| GET    | /api/players/            | Listar jugadores (filtro team_id) |
| GET    | /api/players/{id}        | Obtener jugador                   |
| POST   | /api/players/            | Crear jugador                     |
| POST   | /simulator/              | Ejecutar simulacion del mundial   |
| GET    | /dashboard/metrics       | Obtener metricas del dashboard    |

**Nota:** Los endpoints usan el prefijo `/api/` pero en el codigo los routers estan montados sin ese prefijo. Verificar en `main.py` como estan incluidos realmente.

## Modelos de Base de Datos

### Team
- `id`: Integer (PK)
- `name`: String, unique
- `code`: String(3), unique
- `group_name`: String(1), nullable
- `flag_url`: String, nullable
- `created_at`: DateTime

**Relacion:** Un equipo tiene muchos jugadores (one-to-many). La relacion usa `cascade="all, delete-orphan"`.

### Player
- `id`: Integer (PK)
- `name`: String
- `position`: String(2) — GK, DF, MF, FW
- `number`: Integer, nullable (dorsal)
- `team_id`: Integer (FK -> teams.id)
- `created_at`: DateTime

**Relacion:** Un jugador pertenece a un equipo (many-to-one).

### User
- `id`: Integer (PK)
- `name`: String
- `email`: String, unique
- `password_hash`: String, nullable
- `created_at`: DateTime

## Como ejecutar
```bash
python main.py
```

La aplicacion arranca en http://localhost:8000

## Como ejecutar tests
```bash
python -m pytest tests/
```

## Referencias
- Archivo de configuracion: `config.py`
- Cache de simulacion: `services/simulation_cache.py`
- Las rutas de los routers usan el prefijo `/api/` segun CONTEXT.md, confirmar en el codigo
