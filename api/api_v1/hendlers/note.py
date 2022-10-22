from uuid import UUID
from fastapi import APIRouter, Depends
from typing import List
from schemas.note_schema import NoteAuth
from services.note_service import NoteService
from models.models_mongo import Note, User
from api.deps.user_deps import get_current_user


note_router = APIRouter()


@note_router.get('/search', summary="Search note by user input", response_model=List[NoteAuth])
async def search(data: str, current_user: User = Depends(get_current_user)):
    print("search starts")
    print(data)
    print(current_user)
    return await NoteService.search_note(current_user, data)
    

@note_router.get('/get_all_notes', summary="Get all notes of the user", response_model=List[NoteAuth])
async def list(current_user: User = Depends(get_current_user)):
    return await NoteService.list_notes(current_user)


@note_router.get('/sort', summary="Get all notes of the user sortted by tags")
async def sort_list(current_user: User = Depends(get_current_user)):
    return await NoteService.sort_list(current_user)


@note_router.get('/{note_id}', summary="Get a note by note_id", response_model=NoteAuth)
async def retrieve(note_id: UUID, current_user: User = Depends(get_current_user)):
    return await NoteService.retrieve_note(current_user, note_id)



@note_router.post('/create_note', summary="Create new note", response_model=Note)
async def create_note(data: NoteAuth, current_user: User = Depends(get_current_user)):
    return await NoteService.create_note(current_user, data)


@note_router.put('/{note_id}', summary="Update note by note_id", response_model=NoteAuth)
async def update(note_id: UUID, data: NoteAuth, current_user: User = Depends(get_current_user)):
    return await NoteService.update_note(current_user, note_id, data)


@note_router.delete('/{note_id}', summary="Delete note by note_id")
async def delete(note_id: UUID, current_user: User = Depends(get_current_user)):
    await NoteService.delete_note(current_user, note_id)
    return None