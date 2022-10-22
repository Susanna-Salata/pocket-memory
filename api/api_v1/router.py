from fastapi import APIRouter
from .hendlers import note, record, user
from api.auth.jwt import auth_router

router = APIRouter()

router.include_router(note.note_router, prefix='/notes', tags=['notes'])
router.include_router(record.record_router, prefix='/records', tags=['records'])
router.include_router(user.user_router, prefix='/users', tags=["users"])
router.include_router(auth_router, prefix='/auth', tags=["auth"])
