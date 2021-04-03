from typing import List 
from fastapi import APIRouter ,Response, HTTPException
from sqlalchemy.orm import Session 
import schemas, database, models
from fastapi import Depends, status
from hashing import Hash


router = APIRouter()

@router.post('/user', response_model=schemas.ShowUser, tags=['users'])
def create_user(request : schemas.User, db: Session = Depends(database.get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=['users'])
def get_user(id, response: Response,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'User with id {id} is not available')
    return user


