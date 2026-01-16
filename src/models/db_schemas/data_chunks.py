from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    _id: Optional[ObjectId]
    chunk_data: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int= Field(..., gt=0)
    chunk_project_id: ObjectId

    class Config:  # to allow ObjectId type (which is foreign to pydantic) without errors
        arbitrary_types_allowed = True