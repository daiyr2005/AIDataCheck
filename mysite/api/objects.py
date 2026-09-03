from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from mysite.db.model import FileObject,UserProfile
from mysite.db.schema import FileObjectResponseSchema, FileObjectCreateSchema
from mysite.db.db import SessionLocal
from mysite.api.auth import get_current_user

object_router = APIRouter(prefix="/file",tags=["Objects"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@object_router.post("/", response_model=FileObjectResponseSchema)
async def object_create(
    payload: FileObjectCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserProfile = Depends(get_current_user),
):
    # Опционально: если загрузка файлов доступна только для PRO-пользователей
    # if current_user.status == UserStatusChoice.basic.value:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Файл жүктөө функционлдулугу pro тарифинде гана жеткиликтүү."
    #     )

    file_object = FileObject(
        dataset_file=payload.dataset_file,
        task_file=payload.task_file,
        image_file=payload.image_file,
        user_id=current_user.id,  # Автоматически берем ID из токена текущего юзера
    )

    db.add(file_object)
    db.commit()
    db.refresh(file_object)

    return file_object

#@object_router.post( "/",response_model=FileObjectResponseSchema)
#async def object_create(file: UploadFile = File(...),db: Session = Depends(get_db)):
#    file_object = FileObject(filename=file.filename,content_type=file.content_type)

#    db.add(file_object)
#    db.commit()
#    db.refresh(file_object)

#    return file_object


@object_router.get("/",response_model=List[FileObjectResponseSchema])
async def object_list(
    db: Session = Depends(get_db)):
    objects = db.query(FileObject).all()
    return objects


@object_router.delete("/{object_id}",response_model=dict)
async def object_delete(
    object_id: int,
    db: Session = Depends(get_db)
):
    user_db = db.query(FileObject).filter(FileObject.id == object_id).first()

    if not user_db:
        raise HTTPException(
            detail="Мындай маалымат жок",
            status_code=404
        )

    db.delete(user_db)
    db.commit()

    return {
        "message": "Маалымат өчүрүлдү"
    }