import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ytmusicapi
import ollama
from dotenv import load_dotenv
from typing import Optional

app = FastAPI(title="Pollen Player")

# Accounting for javascript on the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all sites to talk to your backend
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, POST, etc.
    allow_headers=["*"],
)

yt = ytmusicapi.YTMusic()

load_dotenv()
AMBEE_API_KEY = os.getenv("AMBEE_API_KEY")

class PollenPlayerRequest(BaseModel):
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PollenCount(BaseModel):
    tree: int
    grass: int
    weed: int

class PollenPlayerRequest(BaseModel):
    aqi: int
    pollen_count: PollenCount
    search_words: str
    playlist_id: str
    