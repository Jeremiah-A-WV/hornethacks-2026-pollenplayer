import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ytmusicapi
import ollama

app = FastAPI(title="Pollen Player")
yt = ytmusicapi.YTMusic()

AMBEE_API_KEY = os.getenv("AMBEE_API_KEY")

class VibeCall(BaseModel):
    lat: float
    lng: float

class PollenRisk(BaseModel):
    tree: str
    grass: str
    weed: str

class VibeResponse(BaseModel):
    aqi: int
    pollen_risk: PollenRisk
    search_words: str
    playlist_id: str
    