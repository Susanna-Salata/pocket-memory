import uvicorn
from http import server
from fastapi import FastAPI, Request, APIRouter, responses
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.models_mongo import *
from api.api_v1.router import router
from schemas.note_schema import NoteAuth
from schemas.record_schema import RecordAuth
from services.record_service import RecordService
from services.user_service import UserService
from services.note_service import NoteService
from api.auth.forms import *
from api.auth.jwt import login, refresh_token
from api.deps.user_deps import get_current_user
from api.api_v1.hendlers.user import create_user
import time
from threading import Thread
from scrap.scrap import scraping
from api.api_v1.hendlers.record import *
from api.api_v1.hendlers import note
from services.dbox import *


valute = {}
news = {}
sport = {}
weather = {}


def main_scrap():
    while True:
        global valute, news, sport, weather
        valute, news, sport, weather = scraping()
        time.sleep(900)  # перезапуск каждые 15 минут


Thread(target=main_scrap, args=()).start()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
api_router = APIRouter()


app.mount("/static", StaticFiles(directory="static"), name="static")


recordService = RecordService()
userService = UserService()
noteService = NoteService()
templates = Jinja2Templates(directory="templates")


# @api_router.post('/dashboard', response_class=HTMLResponse)
# async def dashboard(request: Request):
#     token = request._cookies.get("access_token").split(" ")[1]
#     user = await get_current_user(token)
#     x = await list(user)
#     print(x)
#     return templates.TemplateResponse("dashboard/dashboard.html",
#                                       context={"request": request})


async def get_user(request):
    token = request._cookies.get("access_token").split(" ")[1]
    try:
        user = await get_current_user(token)
        return user
    except:
        new_token = await refresh_token(refresh_token=request._cookies.get("refresh_token"))
        user = await get_current_user(new_token.get('access_token'))
        return user


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    if (request._cookies.get("access_token")):
        user = await get_user(request)
        return templates.TemplateResponse("index.html", 
                                         {"request": request,
                                          "valute": valute,
                                          "news": news,
                                          "sport": sport,
                                          "weather": weather,
                                          "user": user.__dict__})
    return templates.TemplateResponse("index.html",
                                     {"request": request,
                                      "valute": valute,
                                      "news": news,
                                      "sport": sport,
                                      "weather": weather,})


@app.post('/', response_class=HTMLResponse)
async def home(request: Request):
    user = await get_user(request)
    # x = await list(user)
    return templates.TemplateResponse("index.html",
                                     {"request": request,
                                      "valute": valute,
                                      "news": news,
                                      "sport": sport,
                                      "weather": weather,
                                      "user": user.__dict__})


@app.get('/signup', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get('/contacts', response_class=HTMLResponse)
async def contacts(request: Request):
    user = await get_user(request)
    if not user:
        return responses.RedirectResponse('/signup')
    list_records = await list(user)
    return templates.TemplateResponse("contacts/contacts.html",
                                     {"request": request,
                                      "user": user.__dict__,
                                      "list":list_records,})


@app.post('/contacts', response_class=HTMLResponse)
async def contacts(request: Request):
    if (await request.form()).get("name"):
        form = ContactCreateForm(request)
    if (await request.form()).get("new_contact-id"):
        form = ContactUpdateForm(request)
    if (await request.form()).get("contact-id"):
        form = ContactDeleteForm(request)
    await form.load_data()
    user = await get_user(request)
    if not user:
        return responses.RedirectResponse('/signup')
    if type(form) == ContactCreateForm:
        if await form.is_valid():
            data = RecordAuth(name=form.name,
                              birth_date=form.birth_date,
                              address=form.address,
                              emails=[Emails(email=form.email)],
                              phones=[Phones(phone=form.phones)])
            new_contact = await create_record(data=data ,current_user=user)
        else:
            pass
    list_records = await list(user)
    if type(form) == ContactUpdateForm:
        print(type(form))
        print(form.__dict__)
        data = RecordAuth(name=form.name, 
                          birth_date=form.birth_date,
                          address=form.address,
                          emails=[Emails(email=form.email)],
                          phones=[Phones(phone=form.phones)])
        await update(record_id=form.id, data=data, current_user=user)
    if type(form) == ContactDeleteForm:
        await delete(record_id=form.id, current_user=user)
    list_records = await list(user)
    return templates.TemplateResponse("contacts/contacts.html",
                                     {"request": request,
                                      "user": user.__dict__,
                                      "list":list_records})


@app.get('/notes', response_class=HTMLResponse)
async def notes(request: Request):
    user = await get_user(request)
    if not user:
        return responses.RedirectResponse('/signup')
    notes = await noteService.list_notes(user) 
    return templates.TemplateResponse("notes/notes_dashboard.html",
                                     {"request": request,
                                      "user": user.__dict__,
                                      "notes":notes})

@app.post('/notes', response_class=HTMLResponse)
async def notes(request: Request):
    x = await request.form()
    print(x)
    if (await request.form()).get("note-has-title"):
        form = NoteCreateForm(request)
    if (await request.form()).get("new_note-id"):
        form = NoteUpdateForm(request)
    if (await request.form()).get("note-id"):
        form = NoteDeleteForm(request)
    print(form)
    await form.load_data()
    user = await get_user(request)
    if not user:
        return responses.RedirectResponse('/signup')
    if type(form) == NoteCreateForm:
        data = NoteAuth(name=form.title,
                        records=[Record(description=form.description)],
                        tags=[Tag(name="")])
        new_note = await note.create_note(data=data, current_user=user)
    if type(form) == NoteUpdateForm:
        data = NoteAuth(name=form.title,
                        records=[Record(description=form.description)])
        new_note = await note.update(note_id=form.id,
                                     data=data,
                                     current_user=user)
    if type(form) == NoteDeleteForm:
        await note.delete(note_id=form.id, current_user=user)
    notes = await noteService.list_notes(user)
    return templates.TemplateResponse("notes/notes_dashboard.html",
                                     {"request": request,
                                      "user": user.__dict__,
                                      "notes":notes,
                                      })


@app.get('/files', response_class=HTMLResponse)
async def files(request: Request):
    user = await get_user(request)
    if not user:
        return responses.RedirectResponse('/signup')
    file_list = dropbox_list_files()
    print(file_list)
    return templates.TemplateResponse("files/files.html",
                                     {"request": request,
                                      "user": user.__dict__,
                                      "files":file_list})


@app.post('/uploadfiles', response_class=HTMLResponse)
async def files(request: Request):
    form = FileUploadForm(request)
    await form.load_data()
    user = await get_user(request)
    if not user:
        return responses.RedirectResponse('/signup')
    dropbox_upload_binary_file(binary_file=form.file.file._file,
                               dropbox_file_path=form.file.filename)
    return templates.TemplateResponse("files/files.html",
                                     {"request": request,
                                      "user": user.__dict__,})


@app.post('/signup')
async def signup(request: Request):
    if (await request.form()).get("registerName"):
        form = UserCreateForm(request)
    if (await request.form()).get("loginEmail"):
        form = LoginForm(request) 
    await form.load_data()
    if await form.is_valid():
        if type(form) == LoginForm:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("dashboard/dashboard.html",
                                                  form.__dict__)
            token = await login(response=response, form_data=form)
            redirectresponse = responses.RedirectResponse('/')
            redirectresponse.set_cookie(key="access_token",
                                value=f'Bearer {token.get("access_token")}')
            redirectresponse.set_cookie(key="refresh_token",
                                value=f'{token.get("refresh_token")}')
            return redirectresponse
        elif type(form) == UserCreateForm:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("dashboard/dashboard.html",
                                                  form.__dict__)
            await create_user(data=form)
            form.username = form.email
            token = await login(response=response, form_data=form)
            redirectresponse = responses.RedirectResponse('/')
            redirectresponse.set_cookie(key="access_token",
                                value=f'Bearer {token.get("access_token")}')
            redirectresponse.set_cookie(key="refresh_token",
                                value=f'{token.get("refresh_token")}')
            return redirectresponse
    return templates.TemplateResponse("/signup", context={"request": request})


@app.get('/presentation', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("presentation.html",
                                      {"request": request})


@app.get("/logout")
async def logout(request: Request):
    user = await get_user(request)
    redirectresponse = responses.RedirectResponse('/signup')
    redirectresponse.delete_cookie(key ='access_token')
    redirectresponse.delete_cookie(key ='refresh_token')
    return redirectresponse


@app.on_event("startup")
async def app_init():
    """
        initialize crucial application services
    """
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).MyHelperMongoDB
    await init_beanie(
        database=db_client,
        document_models= [Note, Tag, Record, Emails, Phones, Records, User])
web_router = APIRouter()
web_router.include_router(router=api_router, prefix='', tags=["web-app"])
app.include_router(web_router, prefix=settings.API_V1_STR)
app.include_router(router, prefix=settings.API_V1_STR)


# uvicorn app:app --reload
if __name__ == "__main__":
    config = uvicorn.Config("app:app", 
                            # port=8000,
                            log_level="info", 
                            reload=False,
                            host="0.0.0.0")
    server = uvicorn.Server(config)
    server.run()
