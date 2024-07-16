from pydantic import BaseModel,EmailStr
from typing import List,Optional



class AdminBase(BaseModel):
    u_name : str
    password : str 


class AdminPatch(BaseModel):
    u_name : Optional[str]=None
    password : Optional[str]=None