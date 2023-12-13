from pydantic import BaseModel
from typing import Optional

class SignUPModel(BaseModel):
    id : Optional[int]
    username :str
    email :str
    password :str   
    is_staff : Optional[bool]
    is_active :Optional[bool]


    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "username":"John Doe",
                "email":"john@email.com",
                "password":"john123",
                "is_staff":False,
                "is_active":True
            }
        }

class Settings(BaseModel):
    authjwt_secret_key : str = '2590a0ade58f6b7012b552617cbda0c97a2b7ebb7ad8313144036be48ca519be'


class LoginModel(BaseModel):
    username:str 
    password:str


class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="PENDING"
    pizza_size:Optional[str]="SMALL"
    user_id:Optional[int]


    class Config:
        orm_mode = True
        schema = {
            "example":{
                "quantity":2,
                "pizza_size":"LARGE"
            }
        }

class OrderStatus(BaseModel):
    id:int
    order_status : Optional[str] = "PENDING"