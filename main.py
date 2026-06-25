import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import users_router, teams_router, players_router, simulator_router, metrics_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mundial 2026 - Simulator API")

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://127.0.0.1:5173,http://localhost:5173,"
        "https://pipopinpollo.github.io",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def allow_private_network_access(request, call_next):
    response = await call_next(request)
    if request.headers.get("access-control-request-private-network") == "true":
        response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response


app.include_router(users_router)
app.include_router(teams_router)
app.include_router(players_router)
app.include_router(simulator_router)
app.include_router(metrics_router)


@app.get("/")
def root():
    return {"status": "ok", "service": "Mundial 2026 Simulator API"}
