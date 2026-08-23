from  fastapi import HTTPException, Depends, APIRouter
from  mysite.db.model import UserProfile
from mysite.db.schema import UserProfileInputSchema, UserProfileOutSchema, UserProfileRegisterSchema
from mysite.db.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

user_router = APIRouter(prefix='/user', tags=['UserProfile'])


async  def get_db():
    db = SessionLocal()
    try:
        yield  db
    finally:
        db.close()



@user_router.get('/', response_model=List[UserProfileOutSchema])
async def list_user(db: Session = Depends(get_db)):
    return  db.query(UserProfile).all()

@user_router.get("/{user_id}" , response_model=UserProfileOutSchema)
async  def detail_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user:
        raise HTTPException(detail='Такого ID не существует', status_code=400)
    return user


@user_router.put('/{user_id}')
async def update_user(user_id: int, user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='Такого ID не существует', status_code=400)

    for user_key, user_value in user.dict().items():
        setattr(user_db, user_key, user_value)

    db.commit()
    db.refresh(user_db)
    return {'massage': 'Пользователь был изменён'}


@user_router.delete('/{user_id}', response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='Такого ID не существует', status_code=400)

    db.delete(user_db)
    db.commit()
    return {'massege': 'Пользователь был удалён'}
