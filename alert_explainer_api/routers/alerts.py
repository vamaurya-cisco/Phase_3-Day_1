from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Alert
from schemas import AlertCreate, AlertOut, ExplainResponse
from services.explainer import generate_explanation


router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("/", response_model=AlertOut, status_code=status.HTTP_201_CREATED)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)) -> Alert:
    db_alert = Alert(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.get("/", response_model=list[AlertOut])
def list_alerts(db: Session = Depends(get_db)) -> list[Alert]:
    statement = select(Alert).order_by(Alert.id)
    return list(db.scalars(statement).all())


@router.get("/{alert_id}", response_model=AlertOut)
def get_alert(alert_id: int, db: Session = Depends(get_db)) -> Alert:
    alert = db.get(Alert, alert_id)
    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )
    return alert


@router.post("/{alert_id}/explain", response_model=ExplainResponse)
def explain_alert(alert_id: int, db: Session = Depends(get_db)) -> ExplainResponse:
    alert = db.get(Alert, alert_id)
    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    return ExplainResponse(
        alert_id=alert.id,
        explanation=generate_explanation(alert),
        generated_at=datetime.now(timezone.utc),
    )