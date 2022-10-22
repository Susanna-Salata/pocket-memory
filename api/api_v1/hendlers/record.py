from fastapi import APIRouter, Depends, Request
from schemas.record_schema import RecordAuth, RecordOut
from services.record_service import RecordService
from models.models_mongo import Records, User
from api.deps.user_deps import get_current_user
from uuid import UUID
from typing import List

record_router = APIRouter()


@record_router.get('/get_all_records', summary="Get all records of the user", response_model=List[RecordOut])
async def list(current_user: User = Depends(get_current_user)):
    return await RecordService.list_records(current_user)


@record_router.get('/birthday', summary="Get all records whom b-day is coming", response_model=List[RecordOut])
async def b_day_list(days, current_user: User = Depends(get_current_user)):
    return await RecordService.coming_birthday(current_user, days)    


@record_router.get('/search', summary="Search record by user input", response_model=List[RecordOut])
async def search(data: str, current_user: User = Depends(get_current_user)):
    return await RecordService.search_record(current_user, data)


@record_router.get('/{record_id}', summary="Get a record by record_id", response_model=RecordOut)
async def retrieve(record_id: UUID, current_user: User = Depends(get_current_user)):
    return await RecordService.retrieve_record(current_user, record_id)


@record_router.post('/create_rec', summary="Create new record", response_model=Records)
async def create_record(data: RecordAuth, current_user: User = Depends(get_current_user)):
    return await RecordService.create_record(current_user, data)


@record_router.put('/{record_id}', summary="Update record by record_id", response_model=Records)
async def update(record_id: UUID, data: RecordAuth, current_user: User = Depends(get_current_user)):
    return await RecordService.update_record(current_user, record_id, data)


@record_router.delete('/{record_id}', summary="Delete record by record_id")
async def delete(record_id: UUID, current_user: User = Depends(get_current_user)):
    await RecordService.delete_record(current_user, record_id)
    return None