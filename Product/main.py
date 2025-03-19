from fastapi import FastAPI, status, Response, HTTPException
from fastapi.params import Depends
from . import schemas
from . import models
from sqlalchemy.sql.functions import mode
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)

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


@app.delete("/product/{id}")
def products(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {"product deleted"}

@app.get("/products", response_model=List[schemas.DisplayProduct])  # to show only some params (description and name)
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get("/product/{id}", response_model=schemas.DisplayProduct)  # to show only some params (description and name)
def products(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@app.put("/product/{id}")
def products(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.model_dump())
    db.commit()
    return product

@app.post("/product", status_code=status.HTTP_201_CREATED)  # using status code if success
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description=request.description, price=request.price)
    # Add product to db:
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request
