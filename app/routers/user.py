from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=['Users'])

#Create User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreatedResponse)
def create_user(user:schemas.CreateUser, db: Session= Depends(get_db)):
    #Hash Password
    hashed_password = utils.hash(user.password)
    user.password=hashed_password
    
    #post user details
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserFoundResponse)
def get_user(id: int, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {id} not found")
    return user