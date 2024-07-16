from pydantic import BaseModel
from typing import List,Optional



class DeliveryBoyBase(BaseModel):
    name: str
    mo_number : str
    delivery_id : str




class DeliveryBoyBasePatch(BaseModel):
    name: Optional[str]=None
    mo_number : Optional[str]=None
    delivery_id : Optional[str]=None