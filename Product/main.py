from fastapi import FastAPI
from . import models
from .database import engine
from .routers import product, seller, login
import os
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# templates = Jinja2Templates(directory="templates")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))

app = FastAPI(
    # Adding metadata:
    title="Products API",
    description="Get details in our website",
    terms_of_service="http://www.google.com",
    contact={
        "Developer name": "Jose",
        "website": "http://www.google.com",
        "email": "jose.sosa@bendix.com"
    },
    license_info={
        "name": "XYZ",
        "url": "http://www.google.com"
    },
    # docs_url="/documentation", redoc_url=None
)
# Configure FastAPI tp serve static files (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static')), name="static")


app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)

# Create tables in the database (if they does not exist)
models.Base.metadata.create_all(engine)
