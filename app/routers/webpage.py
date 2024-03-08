from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def intro(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

@router.get("/privacy-policy", response_class=HTMLResponse)
async def intro(request: Request):
    return templates.TemplateResponse("privacypolicy.html", {"request": request})

@router.get("/terms-and-condition", response_class=HTMLResponse)
async def intro(request: Request):
    return templates.TemplateResponse("termcondition.html", {"request": request})

@router.get("/delete-account", response_class=HTMLResponse)
async def intro(request: Request):
    return templates.TemplateResponse("deleteAccount.html", {"request": request})