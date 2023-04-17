from typing import Optional
from uuid import UUID
from schemas.user_schema import UserAuth
from models.models_mongo import User
from core.security import get_password, verify_password
import pymongo
from utils.regex import check_user_name

from schemas.user_schema import UserUpdate


class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        if check_user_name(user.password):
            user_in = User(
                username=user.username,
                email=user.email,
                hashed_password=get_password(user.password)
            )

            await user_in.save()
            print("New user was created")
        else:
            print("User was not created. Try a password 4-20 character length.")
            return None
        return user_in
    
    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=user.hashed_password):
            return None
        
        return user
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user
    
    @staticmethod
    async def get_user_by_id(id: UUID) -> Optional[User]:
        user = await User.find_one(User.user_id == id)
        return user
    
    @staticmethod
    async def update_user(id: UUID, data: UserUpdate) -> User:
        user = await User.find_one(User.user_id == id)
        if not user:
            raise pymongo.errors.OperationFailure("User not found")
    
        await user.update({"$set": data.dict(exclude_unset=True)})
        return user