from pydantic import BaseModel
from typing import Dict, Any

class PredictionRequest(BaseModel):
    year: int
    month: int

class PredictionResponse(BaseModel):
    year: int
    month: int
    predictions: Dict[str, Dict[str, Any]]  # Contains estimated and previous prices for each quality