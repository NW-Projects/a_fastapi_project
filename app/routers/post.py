from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oath2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=['Posts'])


# Read all posts from database
#@router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostVotesView])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str] =""):

#   posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).all()
    
    return posts



#Read one post from database
@router.get("/{id}", response_model=schemas.PostVotesView)
def get_post(id: int, db: Session= Depends(get_db), current_user: int = Depends(oath2.get_current_user)):

#   post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")
    return post





# Create post
# *Returns data to client for validation purpose*
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse )
def create_posts(post:schemas.CreatePost, db: Session= Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    #print(current_user)
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post





#Delete post
@router.delete("/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT, db: Session= Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)





#Update post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post:schemas.UpdatePost, db: Session= Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


