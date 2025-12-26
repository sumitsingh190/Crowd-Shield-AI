from pydantic import BaseModel
from datetime import datetime

class IngestRequest(BaseModel):
    crowd_count: int
    avg_density: float
    max_density: int
    density_growth: float
    movement_variance: float


class RiskResponse(BaseModel):
    crowd_count: int
    avg_density: float
    max_density: int
    risk_score: float
    status: str
    alert: bool
    timestamp: datetime
