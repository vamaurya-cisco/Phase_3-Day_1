from fastapi import FastAPI

from database import Base, engine
from routers.alerts import router as alerts_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Intelligence Layer -- Alert Explainer API")
app.include_router(alerts_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "AI Intelligence Layer is running"}