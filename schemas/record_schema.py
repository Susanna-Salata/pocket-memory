from typing import List
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from models.models_mongo import Emails, Phones



class RecordAuth(BaseModel):
    name: str = Field(...,)
    birth_date: str = None
    address: str = Field(...,)
    emails: List[Emails]
    phones: List[Phones]


class RecordOut (BaseModel):
    name: str = Field(...,)
    birth_date: datetime
    address: str = Field(...,)
    emails: List[Emails]
    phones: List[Phones]

    