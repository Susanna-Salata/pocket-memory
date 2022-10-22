from datetime import datetime
from typing import Optional
from beanie import Document, Indexed, Link, before_event, Replace, Insert
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4


class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    first_name: Optional[str] = None 
    last_name: Optional[str] = None
    disabled: Optional[bool] = None
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False
    
    @property
    def create(self) -> datetime:
        return self.id.generation_time
    
    @classmethod
    async def by_email(self, email: str) -> "User":
        return await self.find_one(self.email == email)
    
    class Collection:
        name = "users"


class Tag(Document):
    id: UUID = Field(default_factory=uuid4, unique=True)
    name: str
    class Collection:
        name = 'tag'

class Record(Document):
    id: UUID = Field(default_factory=uuid4, unique=True)
    description: str
    # done: bool
    class Collection:
        name = 'record'

class Note(Document):
    id: UUID = Field(default_factory=uuid4, unique=True)
    name: str
    records: list[Optional[Link[Record]]]
    tags: list[Optional[Link[Tag]]]
    owner: Link[User]
    created: datetime = Field(default_factory=datetime.utcnow) # Now I don't know how do datatime in project. Try understand it.
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    class Collection:
        name = 'note'

    @before_event([Replace, Insert])
    def update_update_at(self):
        self.updated_at = datetime.utcnow()

class Emails(Document):
    id: UUID = Field(default_factory=uuid4, unique=True, alias='_id')
    email: EmailStr

    class Collection:
        name = 'email'

    class Config:
        allow_population_by_field_name = False
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
            }
        }

class Phones(Document):
    id: UUID = Field(default_factory=uuid4, unique=True)
    phone: str
    class Collection:
        name = 'phone'

    class Config:
        allow_population_by_field_name = False
        schema_extra = {
            "example": {
                "phone": "08008008080",
            }
        }

class Records(Document):
    id: UUID = Field(default_factory=uuid4, unique=True)
    name: str
    birth_date: datetime = None 
    address: str
    emails: list[Optional[Link[Emails]]]
    phones: list[Optional[Link[Phones]]]
    owner: Link[User]
    created: datetime = Field(default_factory=datetime.utcnow) # Now I don't know how do datatime in project. Try understand it.
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    class Colltction:
        name = 'records'

    @before_event([Replace, Insert])
    def update_update_at(self):
        self.updated_at = datetime.utcnow()


class File(Document): # Now I don't know how it shoud work 
    name = str
    link = str