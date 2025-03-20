from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..routers.login import get_current_user
from ..database import get_db
from .. import models, schemas
from typing import List
from fastapi import status, Response, HTTPException


router = APIRouter(
    tags=["Products"],
    prefix="/product"
)


@router.delete("/{id}")
def products(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {"product deleted"}

@router.get("/", response_model=List[schemas.DisplayProduct])  # to show only some params (description and name)
def products(db: Session = Depends(get_db), current_user: schemas.Seller = Depends(get_current_user)):
    products = db.query(models.Product).all()
    return products

@router.get("/{id}", response_model=schemas.DisplayProduct)  # to show only some params (description and name)
def products(id, response: Response, db: Session = Depends(get_db), current_user: schemas.Seller = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.put("/{id}")
def products(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.model_dump())
    db.commit()
    return product

@router.post("/", status_code=status.HTTP_201_CREATED)  # using status code if success
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=1)
    # Add product to db:
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request
