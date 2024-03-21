from mongoengine import Document,  StringField, IntField, ListField
from pydantic import BaseModel
class AdminUserModel(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    accesKey = StringField(required=False)
    
    
class AdminUserScheme(BaseModel):
    name: str
    email: str
    password: str
    
class AdminUserLogin(BaseModel):
    email: str
    password: str
    
    
    
    #AIzaSyC3xr_nnP442368-FJc7qK3whUpsjRrMOU