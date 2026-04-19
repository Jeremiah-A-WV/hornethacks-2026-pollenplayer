from typing import Optional
from pydantic import BaseModel

class PollenPlayerRequest(BaseModel):
    type: str
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
