from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    data_path: str = os.getenv("DATA_PATH", "data")
    data_zip_url: str = os.getenv(
        "DATA_ZIP_URL",
        "https://drive.google.com/uc?export=download&id=1RlX-BzLvSehEc_cwCuWmu_PhFRiNJvrE"
    )
    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

settings = Settings()