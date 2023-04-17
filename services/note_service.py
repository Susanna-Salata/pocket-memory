from typing import List
from uuid import UUID
from schemas.note_schema import NoteAuth
from models.models_mongo import Note, Tag, Record, User
from collections import OrderedDict
from utils.regex import check_note_name


class NoteService:
    @staticmethod
    async def list_notes(user: User) -> List[Note]:
        notes = await Note.find(Note.owner.id == user.id).to_list()
        return notes


    @staticmethod
    async def create_note(user: User, note: NoteAuth):
        async def create_tag(note: NoteAuth):
            tag_list = []
            for tag in note.tags:
                tag_list.append(Tag(name = tag.name))
            return tag_list

        async def create_record(note: NoteAuth):
            rec_list = []
            for rec in note.records:
                rec_list.append(Record(description = rec.description))
            return rec_list
        if check_note_name(note):
            tags,records = await create_tag(note), await create_record(note)
            note_in = Note(
                name = note.name,
                records = records,
                tags = tags,
                owner=user
            )

            return await note_in.save()
        else:
            print("Note name is too short")
            return None


    @staticmethod
    async def retrieve_note(current_user: User, note_id: UUID):
        note = await Note.find_one(Note.id == note_id, Note.owner.id == current_user.id)
        return note
    
    @staticmethod
    async def update_note(current_user: User, note_id: UUID, data: NoteAuth):
        if type(note_id) == str:
            note_id = UUID(note_id)
        note = await NoteService.retrieve_note(current_user, note_id)
        await note.update({"$set": data.dict(exclude_unset=True)})
        
        await note.save()
        return note
    
    @staticmethod
    async def delete_note(current_user: User, note_id: UUID) -> None:
        if type(note_id) == str:
            note_id = UUID(note_id)
        note = await NoteService.retrieve_note(current_user, note_id)
        if note:
            await note.delete()
            
        return None

    
    async def search_note(current_user: User, data: str) -> List[Note]:
        note_list = await Note.find(Note.owner.id == current_user.id, { "$or": [{ 'name': { "$regex": f'{data}' } }, 
        {'tags': { 'name': {"$regex": f'{data}'} } }, {'records': { 'description': {"$regex": f'{data}'} } }] }).to_list()
        return note_list


    @staticmethod
    async def sort_list(user: User) -> List[Note]:
        notes = await Note.find(Note.owner.id == user.id).to_list()
        note_dict = {}
        for note in notes:
            for tags in note.tags:
                if tags.name in note_dict.keys():
                    value = note_dict.get(tags.name)
                    value.append(note)
                else:
                    note_dict[tags.name] = [note]
                    # print(note.name)
        return OrderedDict(sorted(note_dict.items()))
