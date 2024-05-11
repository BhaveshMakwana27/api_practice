from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app import database,schema,models,utils,oauth2

router = APIRouter(tags=['authentication'])

@router.post('/login',response_model=schema.Token)
def login(user_credentials:schema.UserLogin,db:Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email==user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    if not utils.verify_plain_password(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token({'user_id':user.id})

    return {'access_token':access_token,'token_type':'Bearer'}