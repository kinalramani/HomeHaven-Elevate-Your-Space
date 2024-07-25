from pydantic import BaseModel
from typing import List,Optional
from datetime import date




class PaymentBase(BaseModel):
    user_id : str
    order_id : str
    payment_date : date
    amount : float
    transaction_id : Optional[str]=None




class PaymentBasepatch(BaseModel):
    user_id : Optional[str]=None
    order_id : Optional[str]=None
    payment_date : date
    amount : Optional[float]=None
    transaction_id : Optional[str]=None



class PaymentIntentRequest(BaseModel):
    amount: int
    currency: str = 'INR'