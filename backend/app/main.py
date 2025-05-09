from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import numpy as np
import requests
from scipy.interpolate import CubicSpline
from pydantic import BaseModel
import json
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    
load_dotenv()

app = FastAPI()

# Update with your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")
BPS_URL = f"https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/0000/var/500/key/{API_KEY}"

class PredictionRequest(BaseModel):
    year: int
    month: int

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        # Fetch and process data
        rice_data = fetch_rice_price_data()

        predictions = {}
        target_date = request.year + (request.month - 1) / 12.0

        for quality, (x, y) in rice_data.items():
            try:
                # Create cubic spline interpolation
                cs = CubicSpline(x, y)
                
                # Find the closest previous date in our data
                previous_date_idx = np.where(x < target_date)[0]
                
                if len(previous_date_idx) > 0:
                    previous_date_idx = previous_date_idx[-1]
                    previous_date = x[previous_date_idx]
                    previous_price = y[previous_date_idx]
                else:
                    previous_date = x[0]
                    previous_price = y[0]
                
                # Get the estimated price using the spline
                estimated_price = float(cs(target_date))
                
                predictions[quality] = {
                    "estimated_price": round(estimated_price),
                    "previous_price": round(previous_price)
                }
            except Exception as e:
                print(f"Error calculating prediction for {quality}: {str(e)}")
                continue

        return {
            "year": request.year,
            "month": request.month,
            "predictions": predictions,
        }

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

def fetch_rice_price_data():
    try:
        print(f"Fetching data from: {BPS_URL}")
        response = requests.get(BPS_URL)
        response.raise_for_status()
        result = response.json()

        datacontent = result.get("datacontent", {})
        if not datacontent:
            raise ValueError("API response does not contain 'datacontent' or it is empty.")

        months_dict = {
            "premium": [],
            "medium": [],
            "low_quality": [],
        }
        prices_dict = {
            "premium": [],
            "medium": [],
            "low_quality": [],
        }

        for key, price in datacontent.items():
            try:
                if len(key) >= 9:
                    quality_code = key[0:1]
                    year_code = int(key[5:7])
                    month_code = int(key[7:])

                    year = 1900 + year_code if year_code >= 100 else 2000 + year_code
                    month_value = year + (month_code - 1) / 12.0
                    
                    # Map quality codes to quality types
                    quality_map = {"1": "premium", "2": "medium", "3": "low_quality"}
                    quality = quality_map.get(quality_code)
                    
                    if quality and price:
                        try:
                            price_value = float(price)
                            months_dict[quality].append(month_value)
                            prices_dict[quality].append(price_value)
                        except ValueError:
                            continue
            except (ValueError, TypeError, AttributeError) as e:
                print(f"Error processing data point {key}: {e}")
                continue

        processed_data = {}
        for quality in ["premium", "medium", "low_quality"]:
            months = np.array(months_dict[quality])
            prices = np.array(prices_dict[quality])

            if len(months) < 4:  # Need at least 4 points for cubic spline
                continue

            sorted_indices = np.argsort(months)
            months = months[sorted_indices]
            prices = prices[sorted_indices]

            unique_months, unique_indices = np.unique(months, return_index=True)
            unique_prices = prices[unique_indices]

            if len(unique_months) < 4:
                continue

            if not np.all(np.diff(unique_months) > 0):
                print(f"Warning: Month data for {quality} is not strictly increasing after processing.")
                continue

            processed_data[quality] = (unique_months, unique_prices)

        if not processed_data:
            raise ValueError("No valid data found after processing.")

        return processed_data

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching data from API: {e}")
    except ValueError as e:
        raise RuntimeError(f"Data processing error: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")

# Add debug endpoint to test API connection
@app.get("/")
def read_root():
    return {"status": "API is running"}