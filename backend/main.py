import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import ytmusicapi
import ollama
from geopy.geocoders import Nominatim
from dotenv import load_dotenv
from backend.models.PollenCount import PollenCount
from backend.models.PollenPlayerRequest import PollenPlayerRequest
from backend.models.PollenPlayerResponse import PollenPlayerResponse
import asyncio

load_dotenv()
AMBEE_API_KEY = os.getenv("AMBEE_API_KEY")

app = FastAPI(title="Pollen Player")

# Accounting for javascript on the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

yt = ytmusicapi.YTMusic()
geolocator = Nominatim(user_agent="pollenplayer")

@app.post("/generate-atmosphere", response_model=PollenPlayerResponse)
async def generate_atmosphere(request: PollenPlayerRequest):
    lat = request.latitude
    lng = request.longitude

    if request.type == "zip":
        try:
            location = geolocator.geocode(f"{request.zip_code}, USA")
            if not location:
                raise HTTPException(status_code=400, detail="Invalid zip code")
            lat, lng = location.latitude, location.longitude
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Geocoding Error: {e}")
        
    async with httpx.AsyncClient() as client:
        header = {"x-api-key": AMBEE_API_KEY, "Content-Type": "application/json"}
        try:
            aqi_url = f"https://api.ambeedata.com/latest/by-lat-lng?lat={lat}&lng={lng}"
            pollen_url = f"https://api.ambeedata.com/latest/pollen/by-lat-lng?lat={lat}&lng={lng}"
            
            aqi_task = client.get(aqi_url, headers=header)
            pollen_task = client.get(pollen_url, headers=header)
            aqi_res, pollen_res = await asyncio.gather(aqi_task, pollen_task)

            aqi_current = aqi_res.json().get("stations", [{}])[0].get("AQI", 42)
            pollen_count = pollen_res.json().get("data", [{}])[0].get("Count", {})

            pollen_current = PollenCount(
                tree=pollen_count.get("tree_pollen", None),
                grass=pollen_count.get("grass_pollen", None),
                weed=pollen_count.get("weed_pollen", None)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ambee Fetch Failed: {e}")
        

    ai_prompt = f"""
    You are an AI music curator. Your ONLY job is to output a 4-word YouTube search query for an instrumental song. Do not say "Here is your query" or use quotes.

    Environment Data:
    AQI: {aqi_current} (If high: dark, dystopian, moody. If low: bright, upbeat)
    Pollen: Tree: {pollen_current.tree}, Grass: {pollen_current.grass}, Weed: {pollen_current.weed}
    (If any are over 50: indoor chillhop lo-fi. If all low: acoustic outdoor)

    Example Outputs:
    - Dark dystopian synthwave instrumental
    - Bright acoustic outdoor morning
    - Indoor chillhop lofi beats

    DO NOT GIVE ANY EXPLAINATION OR ANY OTHER WORDS JUST
    Generate the 3-word Search Query for the current environment:
    """
    # You are an atmospheric music curator. Translate the following environmental data into a 
    # 4 to 6 word YouTube Music search query for an instrumental song.

    # Translation Rules:
    # - AQI Thresholds: 
    #   * 0-50 (Clean): Bright, airy, upbeat tones.
    #   * 51-100 (Moderate): Neutral, atmospheric, steady.
    #   * 101+ (Hazardous): Dark, moody, dystopian, heavy tones.
    # - Pollen Thresholds: 
    #   * Low counts: Acoustic, organic, outdoor vibes.
    #   * High counts (above 20): Indoor, muffled, heavy lo-fi, chillhop.

    # Current Environment:
    # AQI: {aqi_current}
    # Pollen: {pollen_sum}

    # Generate the search query based on the rules above.
    # DO NOT USE THE WORDS 'AQI' or 'Pollen'
    # OUTPUT STRICTLY THE KEYWORDS. No introductory text, no explanations, and no quotation marks.
    # """

    try:
        ai_res = ollama.chat(model='phi3', messages=[{'role': 'user', 'content': ai_prompt}], options={'num_predict': 10})
        ai_keywords = ai_res['message']['content'].strip().replace('"', '')
    except:
        ai_keywords = "Generic lo-fi beats"

    try:
        search_res = yt.search(query=ai_keywords, filter="songs")
        
        if search_res:
            video_ids = [item['videoId'] for item in search_res[:10]if 'videoId' in item]
        else:
            print("YOUTUBE RETURNED EMPTY LIST. USING FALLBACK.")
            video_ids = ["jfKfPfyJRdk", "5qap5aO4i9A", "rUxyKA_-grg"]
    except Exception as e:
        print(f"YouTube search crashed: {e}")
        video_ids = ["jfKfPfyJRdk", "5qap5aO4i9A", "rUxyKA_-grg"]

    return {
        "aqi": aqi_current,
        "pollen_count": pollen_current,
        "search_words": ai_keywords,
        "video_ids": video_ids # Renamed this key! (Again)
    }
