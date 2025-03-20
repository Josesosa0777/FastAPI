from fastapi import APIRouter, Form
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from .. import models, schemas
from fastapi import status
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    tags=["Seller"]
)

# Dependencia para obtener templates desde main.py
def get_templates() -> Jinja2Templates:
    from ..main import templates
    return templates

# Ruta para servir el formulario de registro
@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("register.html", {"request": request})

# @router.post("/seller", response_model=schemas.DisplaySeller, status_code=status.HTTP_201_CREATED)  # using status code if success
# def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
#     breakpoint()
#     hashed_pwd = pwd_context.hash(request.password)
#     new_seller = models.Seller(username=request.username, email=request.email, password=hashed_pwd)
#     # Add seller to db:
#     db.add(new_seller)
#     db.commit()
#     db.refresh(new_seller)
#     return new_seller

# Ruta para crear el vendedor usando datos del formulario
@router.post("/seller", response_model=schemas.DisplaySeller, status_code=status.HTTP_201_CREATED)
def create_seller(
    username: str = Form(...),  # Usamos Form para los datos del formulario
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    hashed_pwd = pwd_context.hash(password)
    new_seller = models.Seller(username=username, email=email, password=hashed_pwd)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
