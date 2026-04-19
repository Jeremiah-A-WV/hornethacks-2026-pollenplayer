# hornethacks-2026-pollenplayer
Music recommendations based on pollen count and air quality.


## To run, you need:
ollama model phi3 downloaded

To run the front-end: 
python -m http.server 8080

To run the back-end:
uvicorn backend.main:app --reload

Pollen Player utilizes the unofficial YouTube Music API and the Ambee API to leverage real-time Air Quality measures to
generate unique playlists.

Microsoft's Phi-3 model is leveraged to take the amount of pollen in the air alongside the AQI (Air Quality Index) and 
create a "vibe" based on the environment in your area. Alternatively, you may also enter a Zip Code to get pull data 
from another area and generate an entirely different "vibe."