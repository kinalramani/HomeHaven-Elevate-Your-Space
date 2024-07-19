from pydantic import BaseModel
from typing import List,Optional
import datetime




class PaymentBase(BaseModel):
    user_id : str
    order_id : str
    payment_method : str
    payment_date : datetime
    amount : float
    status : str
    transaction_id : Optional[str]=None
    currency : str




class PaymentBasepatch(BaseModel):
    user_id : Optional[str]=None
    order_id : Optional[str]=None
    payment_method : Optional[str]=None
    payment_date : datetime
    amount : Optional[float]=None
    status : Optional[str]=None
    transaction_id : Optional[str]=None
    currency : Optional[str]=None