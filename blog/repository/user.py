from fastapi import APIRouter ,Response, HTTPException
import schemas, database, models
from hashing import Hash
from sqlalchemy.orm import Session 
from fastapi import Depends, status


def getByID(id: int, response: Response,db: Session ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'User with id {id} is not available')
    return user

def create(request : schemas.User, db: Session):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
