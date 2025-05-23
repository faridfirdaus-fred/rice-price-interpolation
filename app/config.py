# filepath: c:\Users\faridfred\Documents\Development\rice-price-interpolation\app\config.py
from pydantic_settings import BaseSettings  # Perubahan di sini
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    api_key: str = os.getenv("API_KEY")
    bps_url: str = f"https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/0000/var/500/key/{os.getenv('API_KEY')}"

settings = Settings()