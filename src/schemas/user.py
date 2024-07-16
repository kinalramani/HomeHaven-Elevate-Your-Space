from pydantic import BaseModel,EmailStr
from typing import List,Optional



class UserBase(BaseModel):
    f_name : str
    l_name : str
    e_mail : str
    password : str 
    mo_number : str
    address : str
    pincode : str
    state : str
    city : str
    


class UserPass(BaseModel):
    u_name : str
    password : str 

class UserPatch(BaseModel):
    f_name : Optional[str]=None
    l_name : Optional[str]=None
    e_mail : Optional[str]=None
    password : Optional[str]=None
    mo_number : Optional[str]=None
    address : Optional[str]=None
    pincode : Optional[str]=None
    state : Optional[str]=None
    city : Optional[str]=None



class OtpRequest(BaseModel):
    user_id:str
    e_mail: str

class OtpVerificationRequest(BaseModel):
    e_mail: str
    otp: str
    user_id:str

class OTPRequest(BaseModel):
    e_mail: str
class OTPVerify(BaseModel):
    e_mail: str
    otp: str