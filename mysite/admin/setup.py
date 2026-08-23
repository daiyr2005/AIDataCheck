from .views import UserProfileAdmin
from  fastapi import FastAPI
from sqladmin import Admin
from mysite.db.db import engine



def setup_admin(user_app: FastAPI):
    admin = Admin(user_app, engine)
    admin.add_view(UserProfileAdmin)
