from pydantic import BaseModel
from typing import Optional


class ChatIn(BaseModel):
    user_id: Optional[int]
    message: str


class ChatOut(BaseModel):
    reply: str
    action: Optional[dict] = None