from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId 


class Project(BaseModel):
    _id: Optional[ObjectId]
    project_id: str =Field(..., min_length=1)

    @validator("project_id")
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError("Project ID isn't valid. It must be alphanumeric.")
        return value
    
    class Config: # to allow ObjectId type (which is foreign to pydantic) without errors
        arbitrary_types_allowed = True
