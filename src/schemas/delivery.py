from pydantic import BaseModel
from typing import List,Optional



class DeliveryBase(BaseModel):
    order_id: str
    user_name: str
    address: str
    payment: str
    status: str
    deliveryboy_id : str