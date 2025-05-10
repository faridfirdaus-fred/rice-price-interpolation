from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.utils import fetch_rice_price_data
from scipy.interpolate import CubicSpline
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class PredictionRequest(BaseModel):
    year: int
    month: int

class PredictionResponse(BaseModel):
    year: int
    month: int
    predictions: Dict[str, Dict[str, Any]]  # Contains estimated and previous prices for each quality

@router.post("/predictions", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        # Get API URL from environment variable
        API_KEY = os.getenv("API_KEY")
        BPS_URL = f"https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/0000/var/500/key/{API_KEY}"
        
        # Pass the URL to the function
        rice_data = fetch_rice_price_data(BPS_URL)

        predictions = {}

        for quality, (x, y) in rice_data.items():
            if len(x) < 2:
                predictions[quality] = {"error": "Not enough data to interpolate"}
                continue

            spline = CubicSpline(x, y, bc_type='natural')

            query_point = request.year + (request.month - 1) / 12.0
            estimated_price = float(spline(query_point))

            if request.month == 1:
                prev_year = request.year - 1
                prev_month = 12
            else:
                prev_year = request.year
                prev_month = request.month - 1

            previous_point = prev_year + (prev_month - 1) / 12.0
            previous_price = float(spline(previous_point))

            predictions[quality] = {
                "estimated_price": estimated_price,
                "previous_price": previous_price,
            }

        return {
            "year": request.year,
            "month": request.month,
            "predictions": predictions,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))