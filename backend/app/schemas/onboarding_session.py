from datetime import datetime
from pydantic import BaseModel, Field

class SessionOut(BaseModel):
    id: str
    created_at: datetime
    expires_at: datetime
    data: dict = Field(default_factory=dict)

    class Config:
        orm_mode = True 