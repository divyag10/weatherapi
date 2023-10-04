from fastapi import FastAPI, File, UploadFile, Request, APIRouter
import uvicorn
import shutil
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
	''' Provide excel file to be uploaded '''
	return templates.TemplateResponse("uploadfile.html", {"request": request})


@router.post("/uploader/")
async def create_upload_file(file: UploadFile):
	''' Upload excel with outfit data to be used with decision tree '''
	dest_dir = Path(__file__).resolve().parent
	dest_path = dest_dir / 'outfit_table.xlsx'
	with open(dest_path, "wb") as buffer:
		shutil.copyfileobj(file.file, buffer)
	return {"filename": file.filename}