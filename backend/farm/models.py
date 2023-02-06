from pydantic import BaseModel

class FarmOwner(BaseModel):
    id: int
    farmId: int
    userId: int
