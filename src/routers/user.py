from fastapi import HTTPException,APIRouter,Header
from src.models.user import User
from src.models.otp import Otp
from src.schemas.user import UserBase,OTPRequest,OTPVerify,UserPatch
from database.database import sessionLocal
from passlib.context import CryptContext
from src.utils.token import logging_token,decode_token_u_id
from logs.log_config import logger
from datetime import datetime 
from src.utils.otp import generate_otp,send_otp_email
import uuid
from src.models.admin import Admin
from src.utils.token import decode_token_a_id,decode_token_a_name





userauth=APIRouter(tags=["Users"])

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

#************************************ register_employee*******************************


@userauth.post("/create_user",response_model=UserBase)
def create_user_details(user:UserBase):

    logger.info(f"Attempting to create a new user with email: {user.e_mail} ")
    find_same_email = db.query(User).filter(User.e_mail==user.e_mail ).first()

    if find_same_email:
        logger.warning(f"User with email {user.e_mail} already exists")
        raise HTTPException(status_code=400,detail="Same email found please try with another one")
    
    logger.info(f"Attempting to create a new user with mo.no: {user.mo_number}")
    find_same_mo_number = db.query(User).filter(User.mo_number==user.mo_number ).first()

    if find_same_mo_number:
        logger.warning(f"User with mo.number {user.mo_number} already exists")
        raise HTTPException(status_code=400,detail="Same mo.number found please try with another one")

    new_user=User(
        id = str(uuid.uuid4()),
        f_name=user.f_name,
        l_name=user.l_name,
        e_mail=user.e_mail,
        password=pwd_context.hash(user.password),
        mo_number=user.mo_number,
        address=user.address,
        pincode=user.pincode,
        state=user.state,
        city=user.city,

    )
    db.add(new_user)
    db.commit()

    logger.success(f"User created successfully with ID: {new_user.id}")
    return new_user



#************************************ get_user_detail*******************************

@userauth.get("/get_user_detail",response_model=UserBase)
def get_employee_detail(token=Header(...)):
    user_id=decode_token_u_id(token)
    logger.info(f"Fetching details for user ID: {user_id}")
    db_user=db.query(User).filter(User.id == user_id,User.is_active == True,User.is_deleted == False,User.is_verified == True).first()
    
    if db_user is None:
        logger.warning(f"User with ID {user_id} not found or is inactive")
        raise HTTPException(status_code=404,detail= "user not found")
    
    logger.success(f"User details fetched successfully for user ID: {user_id}")
    return db_user




#************************************ get employee_all_details*******************************

@userauth.get("/get_user_all_details",response_model=list[UserBase])
def get_user_all_details(token= Header(...)):
    admin_name=decode_token_a_name(token)
    db_admin=db.query(Admin).filter(Admin.u_name == admin_name,Admin.is_active == True,Admin.is_deleted == False).first()

    if db_admin is  None:
        raise HTTPException(status_code=200,detail="invalid token")
    
    logger.info(f"Fetching all details ")
    db_user=db.query(User).filter(User.is_active == True,User.is_deleted == False,User.is_deleted == False,User.is_verified == True).all()

    if db_user is None:
        logger.warning(f"No active user")
        raise HTTPException(status_code=404,detail="user not found")
    
    logger.success(f"User details fetched successfully")
    return db_user




#-------------------------------------------patch_employee-----------------------------------------


@userauth.patch("/update_user_using_patch", response_model=UserPatch)
def update_employee(user: UserPatch,token=Header(...)):
    user_id=decode_token_u_id(token)

    logger.info(f"Attempting to update user details for user ID: {user_id}")
    find_user = db.query(User).filter(User.id == user_id,User.is_active == True).first()
    
    if not find_user:
        logger.warning(f"User with ID {user_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="user not found")
    
    update_data = user.dict(exclude_unset=True)

    if 'password' in update_data:
        hashed_password = pwd_context.hash(update_data['password'])
        update_data['password'] = hashed_password
    
    for key, value in update_data.items():
            
        if key == 'e_mail': 
            inside_find_user = db.query(User).filter(User.e_mail == value).first()
            if inside_find_user:
                raise HTTPException(status_code=403,detail="user already exist")
            
        if key == 'mo_number': 
            inside_find_user = db.query(User).filter(User.mo_number == value).first()
            if inside_find_user:
                raise HTTPException(status_code=403,detail="user already exist")
            
        setattr(find_user,key,value)
    db.commit()
    db.refresh(find_user) 

    logger.success(f"User details updated successfully for user ID: {user_id}")
    return find_user 


#*******************************************put_employee********************************************

@userauth.put("/update_user_using_put", response_model=UserBase)
def update_employee(user: UserBase,token=Header(...)):
    user_id=decode_token_u_id(token)
    logger.info(f"Attempting to update user details for user ID: {user_id}")
    find_user = db.query(User).filter(User.id == user_id,User.is_active == True).first()

    if not find_user:
        logger.warning(f"User with ID {user_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="user not found")
    
    update_data = user.dict(exclude_unset=True)

    if 'password' in update_data:
        hashed_password = pwd_context.hash(update_data['password'])
        update_data['password'] = hashed_password
    
    for key, value in update_data.items():
            
        if key == 'e_mail': 
            inside_find_user = db.query(User).filter(User.e_mail == value).first()
            if inside_find_user:
                raise HTTPException(status_code=403,detail="user already exist")
            
        if key == 'mo_number': 
            inside_find_user = db.query(User).filter(User.mo_number == value).first()
            if inside_find_user:
                raise HTTPException(status_code=403,detail="user already exist")
            
        setattr(find_user,key,value)
    db.commit()
    db.refresh(find_user) 

    logger.success(f"User details updated successfully for user ID: {user_id}")
    return find_user

#************************************delete_user_by_token *******************************


@userauth.delete("/delete_user_by_token")
def delete_user_detail(token=Header(...)):
    user_id=decode_token_u_id(token)

    logger.info(f"Attempting to delete user with ID: {user_id}")

    db_user=db.query(User).filter(User.id == user_id and User.is_active == True).first()

    if db_user is None:
        logger.warning(f"User with ID {user_id} not found or is inactive")
        raise HTTPException(status_code=404,detail="user not found")
    db_user.is_active=False
    db_user.is_deleted=True

    db.commit()
    logger.success(f"User {user_id} deleted successfully")
    return {"message":"user deleted successfully"}




#*************************************forget_password_by_token************************************


@userauth.put("/forget_password_by_token")
def forget_user_detail(new_password:str,token=Header(...)):
    user_id=decode_token_u_id(token)
    logger.info(f"Attempting to reset password for user ID: {user_id}")
    db_user=db.query(User).filter(User.id == user_id,User.is_active == True,User.is_deleted == False,User.is_verified == True).first()

    if db_user is None:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404,detail="user not found")
    db_user.password=pwd_context.hash(new_password)
    
    db.commit()

    logger.success(f"Password reset successfully for user ID: {user_id}")
    return "forget  password successfully"


    

#*******************************************Reset_Password_by_token***************************


@userauth.put("/reset_Password_by_token")
def reset_password( user_oldpass: str, user_newpass: str,token=Header(...)):
    user_id=decode_token_u_id(token)
    logger.info(f"Attempting to reset password for user ID: {user_id}")
    db_user = db.query(User).filter(User.id == user_id,User.is_active == True,User.is_deleted == False,User.is_verified == True).first()

    if db_user is None:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    
    if pwd_context.verify(user_oldpass , db_user.password):
        db_user.password = pwd_context.hash(user_newpass)
        db.commit()
        logger.success(f"Password reset successfully for user ID: {user_id}")
        return "Password reset successfully"
    else:
        logger.warning(f"Old password not matched for user ID: {user_id}")
        return "old password not matched"
    



#**************************************logging_users**************************************



@userauth.get("/logging_user")
def logging_user(e_mail:str, password:str):
    # breakpoint()
    logger.info(f"Attempting to log in user with username: {e_mail}")
    db_user = db.query(User).filter(User.e_mail == e_mail,User.is_active == True,User.is_deleted == False,User.is_verified == True).first()
    if db_user is None:
        logger.warning(f"User with username {e_mail} not found or inactive")
        raise HTTPException(status_code=404, detail="User not found")
    
    if not pwd_context.verify(password, db_user.password):
        logger.warning(f"Incorrect password attempt for username: {e_mail}")
        raise HTTPException(status_code=404, detail="Password is incorrect")
    
    access_token = logging_token(db_user.id,e_mail)

    logger.success(f"User {e_mail} logged in successfully")
    return  access_token




#**************************************************************OTP************************************************

import uuid
Otp_router=APIRouter(tags=["Otp"])
db= sessionLocal()



#*************************************************generate_otp*******************************************


@Otp_router.post("/generate_otp")
def generate_otp_endpoint(request: OTPRequest):
    email = request.e_mail
    logger.info(f"Received OTP generation request for email: {email}")  
    user = db.query(User).filter(User.e_mail == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    otp_code = generate_otp(email)
    send_otp_email(email, otp_code)

    logger.success("OTP generated and sent successfully to the provided email address")
    return {"message": "OTP generated and sent successfully to the provided email address."}




#**********************************************verify_otp********************************************

@Otp_router.post("/verify_otp")
def verify_otp(otp_verify: OTPVerify):
    logger.info(f"Received OTP verification request for email: {otp_verify.e_mail}")
    otp_entry = db.query(Otp).filter(
        Otp.e_mail == otp_verify.e_mail,
        Otp.u_otp == otp_verify.otp,
        Otp.expires_at > datetime.now(),
    ).first()
    if otp_entry is None:
        logger.warning(f"Invalid or expired OTP for email: {otp_verify.e_mail}")
        raise HTTPException(status_code=400, detail="Invalid or expired OTP") 
    db_user = db.query(User).filter(User.e_mail == otp_verify.e_mail).first()
    db_user.is_verified = True
    logger.success(f"User with email {otp_verify.e_mail} verified successfully")

    
    db.delete(otp_entry)
    db.commit()
    logger.success(f"Deleted OTP entry for email: {otp_verify.e_mail}")


    return {"message": "OTP verified successfully"}
