
from enum import Enum as PyEnum
from typing import Optional, List
from datetime import date, datetime

from sqlalchemy import String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from passlib.context import CryptContext

from mysite.db.db import Base

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class UserStatusChoice(str, PyEnum):
    basic = "basic"
    pro = "pro"

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(
        String(16),
        default=UserStatusChoice.basic.value,
        nullable=False
    )
    registered_date: Mapped[date] = mapped_column(Date, default=date.today)
    file_object: Mapped[List['RefreshToken']] = relationship(back_populates="user",cascade="all, delete-orphan")

    refresh_tokens: Mapped[List['RefreshToken']] = relationship(
        back_populates="token_user",
        cascade="all, delete-orphan"
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))
    token_user: Mapped["UserProfile"] = relationship(back_populates="refresh_tokens")
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.token}'


class FileObject(Base):
    __tablename__='file_object'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dataset_file: Mapped[str] = mapped_column(String)
    task_file: Mapped[str | None] = mapped_column(String, nullable=True)
    image_file: Mapped[str | None] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))
    user:Mapped["UserProfile"] = relationship(back_populates="file_object")
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)





