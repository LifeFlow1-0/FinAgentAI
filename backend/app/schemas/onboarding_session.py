from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    expires_at: datetime
    data: dict = Field(default_factory=dict) 