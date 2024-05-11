from fastapi import APIRouter
from fastapi import status,HTTPException, Depends
from sqlalchemy.orm import Session
from app import models,schema,oauth2
from typing import List,Optional
from app.database import engine,get_db
from sqlalchemy import func
# cursor = conn.cursor()

post_app = APIRouter(prefix='/post',tags=['Posts'])

@post_app.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_post(new_post:schema.PostCreate,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user) ):
    # cursor.execute('''insert into post (title,content,published,rating) values(%s,%s,%s,%s) returning *''',(new_post.title,new_post.content,new_post.published,new_post.rating))
    # ins_post = cursor.fetchone()
    # conn.commit()
   
    #ins_post = models.Post(title=new_post.title,content=new_post.content,published=new_post.published,rating=new_post.rating)

    ins_post = models.Post(owner_id=current_user.id,**dict(new_post)) # '**' operator used to get all field at ones we dont have to write code like above line
    db.add(ins_post)
    db.commit()
    db.refresh(ins_post)
    return ins_post

@post_app.get('/{id}',response_model=schema.PostOut)
def get_post(id:int,db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(f'''select * from post where id={id}''')
    # post = cursor.fetchall()

    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Post Found for id : {id}")
        # response.status_code=404
        # return {"Message":f"No Post Found for id : {id}"}
    return post


@post_app.get('/',response_model=List[schema.PostOut])
def get_posts(db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)
              ,limit : int = 10,skip : int = 0,search : Optional[str] = ''):
    # cursor.execute('''select * from post''')
    # posts = cursor.fetchall()

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    result = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Post.id == models.Votes.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # result_dict = [{"post":post,"votes": count} for post, count in result]

    return result


@post_app.delete('/{id}',status_code=status.HTTP_302_FOUND)
def delete_post(id:int,db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(f"delete from post where id={id} returning *")
    # post_to_del = cursor.fetchone()

    post_to_del = db.query(models.Post).filter(models.Post.id==id)

    if post_to_del.first() is None:
            # conn.commit()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Post to delete with id : {id}")

    if post_to_del.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'You are not authorized to perform this action')

    post_to_del.delete()
    db.commit()
    return {"Message":f"Post deleted with id {id}"}


@post_app.put('/{id}')
def update_post(id:int,post:schema.PostCreate,db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):

    # cursor.execute(f"""update post set title='{post.title}',content='{post.content}',rating='{post.rating}' where id={id} returning *""")
    # up_post = cursor.fetchone()

    up_post = db.query(models.Post).filter(models.Post.id==id)

    if up_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not found")

    if up_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'You are not authorized to perform this action')
    # conn.commit()

    up_post.update(dict(post))
    db.commit()

    return {"Message":"Updated"}