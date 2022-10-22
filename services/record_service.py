from datetime import datetime, timedelta
from schemas.record_schema import RecordAuth
from models.models_mongo import Emails, Phones, Records, User
from typing import List
from uuid import UUID


class RecordService:
    @staticmethod
    async def list_records(user:User) -> List[Records]:
        records = await Records.find(Records.owner.id == user.id).to_list()
        return records
 

    @staticmethod
    async def create_record(user: User, record: RecordAuth):
        async def create_phone(record: RecordAuth):
            phone_list = []
            for phone in record.phones:
                phone_list.append(Phones(phone = phone.phone))
            return phone_list
        async def create_email(record: RecordAuth):
            email_list = []
            for email in record.emails:
                email_list.append(Emails(email = email.email))
            return email_list 
        phones,emails = await create_phone(record), await create_email(record)
        bd = None
        if record.birth_date:
            bd = datetime(int(record.birth_date.split('-')[0]), int(record.birth_date.split('-')[1]), int(record.birth_date.split('-')[2][0:2]))
        record_in = Records(
            name = record.name,
            birth_date = bd,
            address = record.address,
            phones = phones,
            emails = emails,
            owner = user
        )
        await record_in.save()
        return record_in

    
    @staticmethod
    async def retrieve_record(current_user: User, record_id: UUID):
        record = await Records.find_one(Records.id == record_id, Records.owner.id == current_user.id)
        return record
    

    @staticmethod
    async def update_record(current_user: User, record_id: UUID, data: RecordAuth):
        if type(record_id)==str:
            record_id = UUID(record_id)
        record = await Records.find_one(Records.id == record_id, Records.owner.id == current_user.id)
        data.birth_date = datetime(int(data.birth_date.split('-')[0]), int(data.birth_date.split('-')[1]), int(data.birth_date.split('-')[2][0:2]))
        await record.update({"$set": data.dict(exclude_unset=True)})
        await record.save()
        return record
    

    @staticmethod
    async def delete_record(current_user: User, record_id: UUID) -> None:
        if type(record_id)==str:
            record_id = UUID(record_id)
        record = await Records.find_one(Records.id == record_id, Records.owner.id == current_user.id)
        if record:
            await record.delete()
        return None


    @staticmethod
    async def search_record(current_user: User, data: str) -> List[Records]:
        record_list = await Records.find(Records.owner.id == current_user.id, { "$or": [{ 'name': { "$regex": f'{data}' } }, 
        {'tags': { 'name': {"$regex": f'{data}'} } }, {'records': { 'description': {"$regex": f'{data}'} } }] }).to_list()
        return record_list

    
    async def coming_birthday(current_user: User, days: str) -> dict:
        days = int(days)
        birthdays_list = []
        current_date = datetime.now().date()
        timedelta_filter = timedelta(days=days)
        for record in await Records.find(Records.owner.id == current_user.id).to_list():
            if record.name and record.birth_date:  # проверка на None
                current_birthday = record.birth_date.replace(year=current_date.year).date()
                if current_date <= current_birthday <= current_date + timedelta_filter:
                    birthdays_list.append(record)
        return birthdays_list