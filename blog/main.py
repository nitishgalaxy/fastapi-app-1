from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas
import models 
from database import engine, SessionLocal
from sqlalchemy.orm import Session 
from typing import List 

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()


models.Base.metadata.create_all(engine)

#@app.post('/blog', status_code=201)
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request : schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs 


'''
@app.get('/blog/{id}')
def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog
'''


'''
@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def show(id, response: Response,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f'Blog with id {id} is not available'}
    return blog
'''


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id, response: Response,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with id {id} is not available')
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with id {id} is not available')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request : schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with id {id} is not available')
    blog.update({'title': 'updated title'}, synchronize_session=False)
    db.commit()
    return 'updated '


@app.post('/user')
def create_user(request : schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

