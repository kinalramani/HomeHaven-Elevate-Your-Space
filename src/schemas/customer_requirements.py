from pydantic import BaseModel
from typing import List,Optional



class CreateCustReq(BaseModel):
    description : str
    Customer_id : str
    product_name : str
    additional_notes : str




class CreateCustReqPatch(BaseModel):
    description : Optional[str]=None
    Customer_id : Optional[str]=None
    product_name : Optional[str]=None
    additional_notes : Optional[str]=None
