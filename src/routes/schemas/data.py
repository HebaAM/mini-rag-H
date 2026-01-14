from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    file_id: str
    chunk_size: Optional[int] = 100  
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0 #prefer 0,1 (binary switch) instead of bool 