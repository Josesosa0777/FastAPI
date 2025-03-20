from fastapi import FastAPI
from . import models
from .database import engine
from .routers import product, seller

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
app.include_router(product.router)
app.include_router(seller.router)

models.Base.metadata.create_all(engine)



# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # Secret key for encoding and decoding JWT token
# SECRET_KEY = "my-secret"
# ALGORITHM = "HS256"
