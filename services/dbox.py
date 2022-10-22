from os import link
import pathlib
import dropbox
from dropbox import Dropbox
from dropbox.exceptions import AuthError
import io
import base64

from beanie import Document

class File(Document): # Now I don't know how it shoud work
    name = str
    link = str

base64_DROPBOX_ACCESS_TOKEN = 'c2wuQlJyb3NfbWpLbjIydXV3c3dOQXFaOGFTTktQNjRRaUE3ODBWQklKem9BY2RYUnl0MTYzTHp1c0xFV3lWTHBaX0g3LWEwaGpucTFiT2NHNlhoNVg5dzVuWGhuMWoxcnRseUtES1E0VkJrLTNNZkNlZGlzQVlWZUJaME1nM0hPa0hIV2N6WXVtMU43cXA='

base64_bytes = base64_DROPBOX_ACCESS_TOKEN.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)
DROPBOX_ACCESS_TOKEN = message_bytes.decode('ascii')

CATEGORIES = ['archives', 'audio', 'documents', 'images', 'video']

FILE_TYPES = {'images': ('JPEG', 'PNG', 'JPG', 'SVG', 'BMP', 'TIF', 'TIFF', 'GIF', 'WEBP'),
              'archives': ('ZIP', 'GZ', 'TAR'),
              'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'PY'),
              'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
              'video':  ('AVI', 'MP4', 'MOV', 'MKV', 'MPG')
        }

def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = Dropbox(DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def order_files():
    links = dropbox_get_link()
    sort_files = {'images':{}, 'documents':{}}
    for key, value in links.items():
        ext = key.split(".")[-1]
        move_to =""
        for k, v in FILE_TYPES.items():
            if ext.upper() in FILE_TYPES.get(k):
                move_to = k
                break

        old_value = sort_files.get(move_to)
        old_value[key]=value
        sort_files[k]=old_value
    return sort_files


def dropbox_list_files():
    dbx = dropbox_connect()
    try:
        files = dbx.files_list_folder("").entries
        files_list = []
        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                files_list.append(file)
        return files_list
    except Exception as e:
        print('Error getting list of files from Dropbox: ' + str(e))


def dropbox_upload_file(local_path, local_file, dropbox_file_path):
    try:
        dbx = dropbox_connect()

        local_file_path = pathlib.Path(local_path) / local_file

        with local_file_path.open("rb") as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

            return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))


def dropbox_upload_binary_file(binary_file, dropbox_file_path):
    try:
        dbx = dropbox_connect()
        meta = dbx.files_upload(binary_file.read(), f"/{dropbox_file_path}", mode=dropbox.files.WriteMode("overwrite"))

        return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))

def dropbox_get_link():
    links = {}
    dbx = dropbox_connect()
    files = dropbox_list_files('')
    for file in files:
        try:
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(file)
            links[file[1:]]=(shared_link_metadata.url).replace('?dl=0', '?dl=1')
        except dropbox.exceptions.ApiError as exception:
            if exception.error.is_shared_link_already_exists():
                shared_link_metadata = dbx.sharing_get_shared_links()
                shared_link = (shared_link_metadata.links[0].url).replace('?dl=0', '?dl=1')
                links[file[1:]]=shared_link
    return links


dropbox_list_files()

# dropbox_upload_file(r'C:\Users\kuzik\Desktop', '2000-a2907b9c3d50e49cd3e9303a04e8a8a2.jpg', f'/2000-a2907b9c3d50e49cd3e9303a04e8a8a2.jpg')
# dropbox_upload_binary_file()
# sort_files = order_files()
# print(sort_files)
# 2000-a2907b9c3d50e49cd3e9303a04e8a8a2.jpg