from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from .. import models, schemas
from fastapi import status

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    tags=["Seller"]
)

@router.post("/seller", response_model=schemas.DisplaySeller, status_code=status.HTTP_201_CREATED)  # using status code if success
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashed_pwd = pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username, email=request.email, password=hashed_pwd)
    # Add seller to db:
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
