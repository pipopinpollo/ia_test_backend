from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.metrics_service import MetricsService
from schemas.metrics import DashboardMetrics, TeamScorersSchema

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get("/dashboard", response_model=DashboardMetrics)
def get_dashboard_metrics(db: Session = Depends(get_db)):
    service = MetricsService(db)
    return service.get_dashboard_metrics()


@router.get("/team-scorers", response_model=list[TeamScorersSchema])
def get_team_scorers(db: Session = Depends(get_db)):
    service = MetricsService(db)
    return service.get_team_scorers()
