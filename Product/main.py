from fastapi import FastAPI, status, Response, HTTPException
from fastapi.params import Depends
from . import schemas
from . import models
from sqlalchemy.sql.functions import mode
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from typing import List
from passlib.context import CryptContext

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

models.Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # Secret key for encoding and decoding JWT token
# SECRET_KEY = "my-secret"
# ALGORITHM = "HS256"


@app.delete("/product/{id}", tags=["Products"])
def products(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {"product deleted"}

@app.get("/products", response_model=List[schemas.DisplayProduct], tags=["Products"])  # to show only some params (description and name)
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get("/product/{id}", response_model=schemas.DisplayProduct, tags=["Products"])  # to show only some params (description and name)
def products(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@app.put("/product/{id}", tags=["Products"])
def products(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.model_dump())
    db.commit()
    return product

@app.post("/product", status_code=status.HTTP_201_CREATED, tags=["Products"])  # using status code if success
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=1)
    # Add product to db:
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

@app.post("/seller", response_model=schemas.DisplaySeller, status_code=status.HTTP_201_CREATED, tags=["Seller"])  # using status code if success
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashed_pwd = pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username, email=request.email, password=hashed_pwd)
    # Add seller to db:
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
