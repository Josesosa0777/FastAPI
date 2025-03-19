from fastapi import FastAPI, Body, Request, File, UploadFile, Form, Depends
from pydantic import BaseModel, Field, HttpUrl
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from typing import Annotated
from jose import jwt
from typing import Set, List
from uuid import UUID
from datetime import date, datetime, time, timedelta


class Event(BaseModel):
    event_id: UUID
    start_date: date
    start_time: datetime
    end_time: datetime
    repeat_time: time
    execute_after: timedelta


class Profile(BaseModel):
    name: str
    email: str
    age: int


class Image(BaseModel):
    url: HttpUrl
    name: str


class Product(BaseModel):
    name: str
    price: int = Field(title="Price of the item", description="This would be the price of the item being added.", gt=0)
    discount: int
    discounted_price: float
    tags: Set[str] = []  # unique tags
    image: List[Image]

    class Config:  # add example to documentation
        json_schema_extra = {
            "example": {
                "name": "Phone",
                "price": 100,
                "discount": 0,
                "discounted_price": 0,
                "tags": ["electronics", "phones"],
                "image": [
                    {"url": "http://www.google.com",
                    "name": "phone image"},
                    {"url": "http://www.google.com",
                    "name": "phone image side view"},
                ]
            }
        }


class Offer(BaseModel):
    name: str
    description: str
    price: float
    products: List[Product]


class User(BaseModel):
    name: str = Field(example="Joseph")  # Add example to doc using Fields
    email: str


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users = {
    "jose": {"username": "jose", "email": "jose.sosa@bendix.net", "password": "sosa"}
}

# Secret key for encoding and decoding JWT token
SECRET_KEY = "my-secret"
ALGORITHM = "HS256"

def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        # Decode the token
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = data.get("username")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = users.get(username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Remove the password from the user data before returning
        user_data = {key: value for key, value in user.items() if key != "password"}
        return user_data
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def index():
    return "Hello there"

# id here is a path parameter
@app.get("/property/{id}")
def property(id: int):
    return f"Property {id}"

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = encode_token({"username": user["username"], "email": user["email"]})
    return {"access_token": token}

@app.post("/login2")
def login2(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

@app.post("/addevent")
def addevent(event: Event):
    return event

@app.post("/addoffer")
def property(offer: Offer):
    return {offer}

@app.post("/purchase")
def purchase(user: User, product: Product):
    return {"user": user, "product": product}
    # {

@app.post("/addproduct/{product_id}")
def addproduct(product: Product, product_id: int, category: str):
    product.discounted_price = product.price - (product.price * product.discount)/100
    return {"product_id": product_id, "product": product, "category": category}
    # {
    # "name": "iphone",
    # "price": 1000,
    # "discount": 5,
    # "discounted_price": 0
    # }

@app.get("/users/admin")
async def admin():
    return "This is admin page"


@app.post("/adduser")
def adduser(profile: Profile):
    return profile

@app.get("/users/profile")
async def profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user

@app.get("/products")
async def products(id: int = None, price: int = None):  # Default parameters  # http://127.0.0.1:8000/products
    return {f"Product with id: {id} and price {price}"}  # http://127.0.0.1:8000/products?id=10&price=100  This is a query parameter

@app.get("/profile/{userid}/comments")
def profile(userid:int, commentid: int):  # Combination path and query parameters
    return {f"Profile page for user: {userid} and comment with {commentid}"}  #  http://127.0.0.1:8000/profile/10/comments?commentid=20
