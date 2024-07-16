from pydantic import BaseModel
from typing import List,Optional



class CreateCurtains(BaseModel):
    user_id :str
    category : str
    description : Optional[str]=None
    warranty_period : str




class CreateCurtainsPatch(BaseModel):
    user_id :Optional[str]=None
    category : Optional[str]=None
    description : Optional[str]=None
    warranty_period : Optional[str]=None