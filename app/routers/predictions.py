from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from app.services.regression import perform_polynomial_regression
from app.services.interpolation import perform_cubic_spline_interpolation
from app.utils import fetch_rice_price_data
from app.config import settings  # Import settings
import os
import traceback

router = APIRouter()

class PredictionRequest(BaseModel):
    year: int
    month: int

class PredictionResponse(BaseModel):
    year: int
    month: int
    predictions: Dict[str, Dict[str, Any]]

@router.post("/predictions", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        # Only allow predictions after December 2023
        if request.year < 2024 or (request.year == 2023 and request.month <= 12):
            raise HTTPException(status_code=400, detail="Prediction is only available for dates after December 2023. For historical data, use the /historical endpoint.")

        # Pass API URL from settings
        rice_data = fetch_rice_price_data(settings.bps_url)
        predictions = {}

        # Calculate target month for prediction
        predict_month = request.year + (request.month - 1) / 12

        # Calculate previous month
        previous_month = request.month - 1 if request.month > 1 else 12
        previous_year = request.year if request.month > 1 else request.year - 1
        previous_month_float = previous_year + (previous_month - 1) / 12

        # First, calculate all predictions for the target month
        for quality, (months, prices) in rice_data.items():
            if len(months) < 2:
                predictions[quality] = {"error": "Not enough data to interpolate"}
                continue

            # Calculate predicted price for target month using polynomial regression
            # This is better for future predictions as it captures long-term trends
            estimated_price = perform_polynomial_regression(months, prices, predict_month=predict_month)
            
            # For previous month:
            # - If it's in 2023 or earlier, use cubic spline (better for historical data)
            # - If it's in 2024 or later, use polynomial regression (for consistency with predictions)
            if previous_year < 2024:
                previous_price = perform_cubic_spline_interpolation(months, prices, predict_month=previous_month_float)
            else:
                previous_price = perform_polynomial_regression(months, prices, predict_month=previous_month_float)

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
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

class HistoricalResponse(BaseModel):
    historical: Dict[str, List[Dict[str, Any]]]

@router.get("/historical", response_model=HistoricalResponse)
async def get_historical():
    try:
        # Pass API URL from settings
        rice_data = fetch_rice_price_data(settings.bps_url)
        
        # Format for chart: {quality: [{year, month, price}, ...]}
        historical = {}
        for quality, (months, prices) in rice_data.items():
            historical[quality] = [
                {
                    "month": int(round((m % 1) * 12)) + 1,
                    "year": int(m),
                    "price": float(p)
                }
                for m, p in zip(months, prices)
                if 2013 <= int(m) <= 2024 and 1 <= int(round((m % 1) * 12)) + 1 <= 12
            ]
        return {"historical": historical}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))