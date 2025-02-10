from pydantic import BaseModel
from datetime import datetime

class FireRecord(BaseModel):
    id: int
    acquisition_date: datetime
    latitude: float
    longitude: float
    brightness: float
    confidence: int
    region: str