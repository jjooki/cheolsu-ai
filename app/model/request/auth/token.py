from pydantic import BaseModel, Field
from typing import Optional
    
class Token(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    id: Optional[int] = None