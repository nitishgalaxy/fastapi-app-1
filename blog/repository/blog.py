from sqlalchemy.orm import Session 
import models 
import schemas
from fastapi import status, HTTPException, Response


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs 


def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with id {id} is not available')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'


def update(id: int, request : schemas.Blog, db: Session ):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with id {id} is not available')
    blog.update({'title': 'updated title'}, synchronize_session=False)
    db.commit()
    return 'updated'


def getByID(id:int, response: Response,db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with id {id} is not available')
    return blog
