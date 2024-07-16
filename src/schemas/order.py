from pydantic import BaseModel
from typing import List,Optional




class OrderBase(BaseModel):
    req_id: str
    user_id: str
    description: str
    product_id: str
    notes: str
    price: float
    status: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    is_active: bool

class OrderBasePatch(BaseModel):
    req_id: Optional[str]=None
    user_id: Optional[str]= None
    description: Optional[str]= None
    product_id: Optional[str]= None
    notes: Optional[str]= None
    price: float
    status: Optional[str]= None