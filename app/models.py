from pydantic import BaseModel
from typing import Dict, Any

class PredictionResponse(BaseModel):
    year: int
    month: int
    predictions: Dict[str, Dict[str, Any]]  # Contains estimated and previous prices for each quality

class PriceResponse(BaseModel):
    year: int
    month: int
    results: Dict[str, Dict[str, Any]]
    is_prediction: bool