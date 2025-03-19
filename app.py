from fastapi import FastAPI, Body, Request, File, UploadFile, Form, Depends
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

list_of_usernames = list()
templates = Jinja2Templates(directory="htmldirectory")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    print("form_data user: ", form_data.username)
    # breakpoint()
    return {"access_token": form_data.username, "token_type": "bearer"}


@app.get("/users/profilepic")
async def profile_pic(token: str = Depends(oauth_scheme)):
    print(token)
    return {"user": "jos", "profile_pic": "myface"}


class NameValues(BaseModel):
    name: str = None
    country: str
    age: int
    base_salary: float

@app.get("/home/{user_name}", response_class=HTMLResponse)
def write_home(request: Request, user_name: str):
    return templates.TemplateResponse("home.html", {"request": request, "username": user_name})

@app.post("/submitform")
async def handel_form(assignment: str = Form(...), assignment_file: UploadFile = File(...)):
    print(assignment)
    print(assignment_file.filename)
    content_assignment = await assignment_file.read()
    print(content_assignment)
