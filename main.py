from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import numpy as np
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],  # Ganti dengan domain frontend Anda
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")
BPS_URL = f"https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/0000/var/500/key/{API_KEY}"

class PredictionRequest(BaseModel):
    year: int
    month: int  # Tambahkan parameter bulan

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        x, y = fetch_rice_price_data()

        if len(x) < 2:
            return {"error": "Not enough data to interpolate"}

        # Interpolasi menggunakan data bulanan
        coeffs = np.polyfit(x, y, deg=min(3, len(x)-1))
        polynomial = np.poly1d(coeffs)

        # Hitung nilai prediksi berdasarkan bulan dan tahun
        query_point = request.year + (request.month - 1) / 12.0
        estimated_price = float(polynomial(query_point))

        return {
            "year": request.year,
            "month": request.month,
            "estimated_price": estimated_price,
            "coefficients": coeffs.tolist()
        }

    except RuntimeError as e:
        return {"error": str(e)}

def fetch_rice_price_data():
    try:
        # Ambil data dari API
        response = requests.get(BPS_URL)
        response.raise_for_status()  # Raise an error for HTTP errors
        print("Full API Response:", response.text)  # Debugging line untuk melihat respons lengkap
        result = response.json()
        print("Parsed API Response:", result)  # Debugging line untuk melihat hasil parsing JSON

        # Ambil data dari respons
        datacontent = result.get("datacontent", {})
        if not datacontent:
            raise ValueError("API response does not contain 'datacontent' or it is empty.")

        months = []
        prices = []

        # Proses data dari datacontent
        # Format key seperti: "350001231" (kualitas(1) + tahun(2) + bulan(2))
        for key, price in datacontent.items():
            try:
                if len(key) >= 9:
                    # Ekstrak tahun dan bulan dari key
                    quality_code = key[0:1]  # First digit represents quality
                    year_code = int(key[5:7])  # Year is in positions 5-6
                    month_code = int(key[7:])  # Month is at the end
                    
                    # Konversi kode tahun ke tahun sebenarnya (113 -> 2013)
                    year = 1900 + year_code if year_code >= 100 else 2000 + year_code
                    
                    # Gunakan hanya data dari kualitas premium (kode 1)
                    if quality_code == '3':  # Adjust based on which quality you want
                        months.append(year + (month_code - 1) / 12.0)
                        prices.append(float(price))
            except (ValueError, TypeError, AttributeError) as e:
                print(f"Skipping invalid item: {key}={price}, error: {e}")  # Debugging line
                continue  # Lewati data yang tidak valid

        # Pastikan ada data yang valid
        if not months or not prices:
            raise ValueError("No valid data found in API response.")

        return np.array(months), np.array(prices)

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching data from API: {e}")
    except ValueError as e:
        raise RuntimeError(f"Data processing error: {e}")