from typing import List 
from fastapi import APIRouter ,Response, HTTPException
from sqlalchemy.orm import Session 
import schemas, database, models
from fastapi import Depends, status
from hashing import Hash
from repository import user


router = APIRouter(
    prefix='/user',
    tags=['users']
)

@router.post('/', response_model=schemas.ShowUser)
def create_user(request : schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id: int, response: Response,db: Session = Depends(database.get_db)):
    return user.getByID(id, response, db)


