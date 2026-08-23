from pydantic.json_schema import model_json_schema
from  mysite.db.model import *
from  sqladmin import  ModelView


class UserProfileAdmin(ModelView, model = UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]

