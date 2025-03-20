from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from ..schemas import TokenData
from .. import models
from fastapi import status, Response, HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# # Secret key for encoding and decoding JWT token
SECRET_KEY = "my-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '..', 'templates'))



router = APIRouter()

# Dependency to get templates from main.py
def get_templates() -> Jinja2Templates:
    from ..main import templates
    return templates

# Route to render the login form
@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("login.html", {"request": request})

def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login", status_code=status.HTTP_201_CREATED)  # using status code if success
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not seller:
        print("###")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found/ invalid user")
    if not pwd_context.verify(request.password, seller.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    # Get JWT token
    acces_token = generate_token(data={"sub": seller.username})
    return {"access_token": acces_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            pass
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception