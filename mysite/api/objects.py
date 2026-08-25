from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from mysite.db.model import FileObject
from mysite.db.schema import FileObjectResponseSchema, FileObjectCreateSchema
from mysite.db.db import SessionLocal


object_router = APIRouter(prefix="/objects",tags=["Objects"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@object_router.post("/", response_model=FileObjectResponseSchema)
async def object_create(
    payload: FileObjectCreateSchema,
    db: Session = Depends(get_db)
):
    # Если user_id берется из аутентификации или захардкожен, добавьте его:
    file_object = FileObject(
        dataset_file=payload.dataset_file,
        task_file=payload.task_file,
        img_file=payload.img_file,
        # user_id=1  # Укажите нужный user_id
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