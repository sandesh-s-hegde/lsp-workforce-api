from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

import models
from database import engine

# Auto-generate database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LSP Workforce & Dispatch API",
    description="Micro-tactical execution engine for routing human and AGV tasks.",
    version="0.1.0"
)


class SystemStatus(BaseModel):
    status: str
    timestamp: datetime
    version: str


@app.get("/", response_model=SystemStatus, tags=["System"])
async def root() -> dict:
    """Health check endpoint to verify the API is online."""
    return {
        "status": "Online",
        "timestamp": datetime.now(),
        "version": "0.1.0"
    }


@app.get("/api/v1/workforce/roster", tags=["Workforce"])
async def get_workforce_roster() -> dict:
    """Fetches the current availability of human workers and AGVs."""
    return {
        "human_workers": [
            {
                "id": "W-101",
                "role": "Forklift Operator",
                "status": "Available",
                "fatigue_score": 12
            },
            {
                "id": "W-102",
                "role": "Picker",
                "status": "On Break",
                "fatigue_score": 65
            }
        ],
        "agv_fleet": [
            {
                "id": "AGV-01",
                "type": "Pallet Jack",
                "status": "Charging",
                "battery_pct": 18
            },
            {
                "id": "AGV-02",
                "type": "Autonomous Forklift",
                "status": "Available",
                "battery_pct": 94
            }
        ]
    }