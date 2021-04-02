from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn


app = FastAPI()


@app.get("/")
def index():
    # Return String
    #return "heyy"

    # Return dict which will get converteed to json
    return {"hello": "world"}


@app.get("/about")
def about():
    return {"data": "about page"}


@app.get("/blog/{id}")
def show(id):
    # id is string here
    return {"data": id} 


@app.get("/blog/{id}/comments")
def comments(id : int):
    # Use hints to enforce data type of ID as int
    return {"comments": id} 


@app.get("/blog")
def blog(limit=10, published:bool = True, sort:Optional[str]=None):

    return {"data": f"limit={limit}  published={published} sort={sort}"}


class Blog(BaseModel):
    title: str 
    body: str 
    published: Optional[bool]


'''
@app.post("/blog")
def create_blog(request: Blog):
    return request
'''

@app.post("/blog")
def create_blog(blog: Blog):
    return {'data': f"Blog is created with title as {blog.title}"}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=9000)
