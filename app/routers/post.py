from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from  typing import List, Optional
from sqlalchemy.orm import Session
from app import oauth2
from sqlalchemy import func
#up two directories 
from .. import models, schemas, oauth2
from .. database import get_db

#create a router object
router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user), 
    limit: int=10, skip: int =0, search: Optional[str] = ""):  #passed in db to use sqlalchemy
    
    # i am getting all posts from all users...
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #by default, sqlalchemy will be a left inner join
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, 
    isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

    #if i want all posts from a specific user, then use commented code on next line
    #posts = db-query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    #return posts  #return the tuple or dictionary??

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)):
    #user_id was get_current_user:
    ##here is the raw sql version below commented out to use sqlalchemy
    #cursor.execute("""INSERT INTO posts(title, content, published) 
    #        VALUES (%s, %s, %s) RETURNING * """,
    #            (post.title, post.content, post.published))
    #
    #new_post = cursor.fetchone() #this fetches what was returned in RETURNING * from previous sql statement call
    ##now commit the changes

    #conn.commit()
    ##for digital alchemy access the models.Post and then pass in the three variables that i need
    
    ##to do this using a dictionary so we don't have to type out each field
    #being passed to models.Post(), use this format instead:
    
    new_post = models.Post(owner_id = current_user.id,**post.dict()) #double stars upacks the dictionary
    
    ## -- long form of line above is repeated below
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    #to get something like the RETURNING * statement in sqlalchemy call .refresh(new_post)
    # this retrieves the new post and stores it in the new_post variable for returning to
    # function call
    db.refresh(new_post)

    return new_post
   

@router.get("/{id}", response_model= schemas.PostOut)         #pass path parameter of id to identify specific post
async def get_post(id: int, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):        #fastAPI automagically extracts id and int converts to int and can pass into function
    
    #SQL Code
    #cursor.execute(""" SELECT * FROM posts where id = %s""", (str(id)))
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, 
    isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #check to make sure that we have this post, if not return a 404
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail= f"post with id: {id} was not found")
        
   


    return post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts where id = %s returning *""", (str(id)))
    #deleted_post = cursor.fetchone()

    # i don't have an index below...do i need to fetchone before i can raise an exception?
    # and i'm assuming that i have to call commit() once i've passed the delete statement
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
       detail = f"post with id: {id} does not exist.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.
            HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action") 

    #conn.commit()
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)): # did not call this as asynchronous here
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s 
    #WHERE id = %s RETURNING * """,(post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()

    #save a query to find the post wiht the right id...
    post_query = db.query(models.Post).filter(models.Post.id == id)

    #now, run the query...save in post
    post = post_query.first()

    #check to make sure the post exists...if not...raise exception
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail = f"post with id: {id} does not exist.")
        #assuming the post is found...convert to dictionary and store it
    #conn.commit()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.
            HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    # if post does exist, run update on query and pass in fields as a dictionary

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

