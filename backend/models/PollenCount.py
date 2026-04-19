from pydantic import BaseModel

class PollenCount(BaseModel):
    tree: int
    grass: int
    weed: int
