from typing import List
from pydantic import BaseModel, Field
from models.models_mongo import Record, Tag


class NoteAuth(BaseModel):
    name: str = Field(...,)
    records: List[Record] 
    tags: List[Tag] 


    