from typing import List 
from fastapi import APIRouter ,Response, HTTPException
from sqlalchemy.orm import Session 
import schemas, database, models
from fastapi import Depends, status
from repository import blog


router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db)):
    return blog.get_all(db)


#@app.post('/blog', status_code=201)
@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request : schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.create(request, db)



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


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id:int, response: Response,db: Session = Depends(database.get_db)):
    return blog.getByID(id, response, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(database.get_db)):
    return blog.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request : schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.update(id, request, db)



