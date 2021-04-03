from typing import List 
from fastapi import APIRouter ,Response, HTTPException
from sqlalchemy.orm import Session 
import schemas, database, models
from fastapi import Depends, status


router = APIRouter()

@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs 


#@app.post('/blog', status_code=201)
@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request : schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



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


@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
def show(id, response: Response,db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with id {id} is not available')
    return blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with id {id} is not available')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'deleted'


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request : schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f'Blog with id {id} is not available')
    blog.update({'title': 'updated title'}, synchronize_session=False)
    db.commit()
    return 'updated '

