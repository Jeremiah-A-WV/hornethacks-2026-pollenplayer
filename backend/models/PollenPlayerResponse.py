from pydantic import BaseModel
from typing import List
from backend.models.PollenCount import PollenCount

class PollenPlayerResponse(BaseModel):
    aqi: int
    pollen_count: PollenCount
    search_words: str
    video_ids: List[str]
