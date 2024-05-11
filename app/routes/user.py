from fastapi import APIRouter
from fastapi import status,HTTPException, Depends
from sqlalchemy.orm import Session
from app import models,schema,utils
from app.database import engine,get_db

user_app = APIRouter(prefix='/user',tags=['User'])


@user_app.post('/',response_model=schema.UserOut,status_code=status.HTTP_201_CREATED)
def create_user(user:schema.CreateUser,db:Session = Depends(get_db)):

    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    user = models.User(**dict(user))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@user_app.get('/{id}', response_model=schema.UserOut,status_code=status.HTTP_302_FOUND)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user doesn't exist")

    return user