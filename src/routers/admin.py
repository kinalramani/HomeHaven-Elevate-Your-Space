from fastapi import HTTPException,APIRouter,Header
from src.models.admin import Admin
from src.schemas.admin import AdminBase,AdminPatch
from database.database import sessionLocal
from passlib.context import CryptContext
from src.utils.token import admin_logging_token,decode_token_a_id
from logs.log_config import logger
from datetime import datetime 
import uuid




adminauth=APIRouter(tags=["Admin"])

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")



#************************************ register_admin*******************************

@adminauth.post("/register_admin",response_model=AdminBase)
def create_user_details(admin:AdminBase):

    logger.info(f"Attempting to create a new admin with email: {admin.u_name} ")
    find_same_u_name = db.query(Admin).filter(Admin.u_name == admin.u_name ).first()

    if find_same_u_name:
        logger.warning(f"admin with user_name {Admin.u_name} already exists")
        raise HTTPException(status_code=400,detail="Same user_name found please try with another one")
    

    new_admin=Admin(
        id = str(uuid.uuid4()),
        u_name=admin.u_name,
        password=pwd_context.hash(admin.password),

    )
    db.add(new_admin)
    db.commit()

    logger.success(f"Admin created successfully with ID: {new_admin.id}")
    return new_admin





#************************************ get_admin_detail*******************************

@adminauth.get("/get_admin_detail",response_model=AdminBase)
def get_employee_detail(token=Header(...)):
    admin_id=decode_token_a_id(token)
    logger.info(f"Fetching details for admin ID: {admin_id}")
    db_admin=db.query(Admin).filter(Admin.id == admin_id,Admin.is_active == True,Admin.is_deleted == False).first()
    
    if db_admin is None:
        logger.warning(f"Admin with ID {admin_id} not found or is inactive")
        raise HTTPException(status_code=404,detail= "Admin not found")
    
    logger.success(f"Admin details fetched successfully for admin ID: {admin_id}")
    return db_admin






#-------------------------------------------patch_admin-----------------------------------------


@adminauth.patch("/update_admin_using_patch", response_model=AdminPatch)
def update_employee(admin: AdminPatch,token=Header(...)):
    admin_id=decode_token_a_id(token)

    logger.info(f"Attempting to update admin details for admin ID: {admin_id}")
    find_admin = db.query(Admin).filter(Admin.id == admin_id,Admin.is_active == True).first()
    
    if not find_admin:
        logger.warning(f"Admin with ID {admin_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="Admin not found")
    
    update_data = admin.dict(exclude_unset=True)

    if 'password' in update_data:
        hashed_password = pwd_context.hash(update_data['password'])
        update_data['password'] = hashed_password
    
    for key, value in update_data.items():
            
        if key == 'u_name': 
            inside_find_admin = db.query(Admin).filter(Admin.u_name == value).first()
            if inside_find_admin:
                raise HTTPException(status_code=403,detail="Admin already exist")
            
        setattr(find_admin,key,value)
    db.commit()
    db.refresh(find_admin) 

    logger.success(f"Admin details updated successfully for admin ID: {admin_id}")
    return find_admin 




#-------------------------------------------put_admin-----------------------------------------


@adminauth.put("/update_admin_using_put", response_model=AdminBase)
def update_employee(admin: AdminBase,token=Header(...)):
    admin_id=decode_token_a_id(token)

    logger.info(f"Attempting to update admin details for admin ID: {admin_id}")
    find_admin = db.query(Admin).filter(Admin.id == admin_id,Admin.is_active == True).first()
    
    if not find_admin:
        logger.warning(f"Admin with ID {admin_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="Admin not found")
    
    update_data = admin.dict(exclude_unset=True)

    if 'password' in update_data:
        hashed_password = pwd_context.hash(update_data['password'])
        update_data['password'] = hashed_password
    
    for key, value in update_data.items():
            
        if key == 'u_name': 
            inside_find_admin = db.query(Admin).filter(Admin.u_name == value).first()
            if inside_find_admin:
                raise HTTPException(status_code=403,detail="Admin already exist")
            
        setattr(find_admin,key,value)
    db.commit()
    db.refresh(find_admin) 

    logger.success(f"Admin details updated successfully for admin ID: {admin_id}")
    return find_admin 




#************************************delete_admin_by_token *******************************


@adminauth.delete("/delete_admin_by_token")
def delete_user_detail(token=Header(...)):
    admin_id=decode_token_a_id(token)

    logger.info(f"Attempting to delete admin with ID: {admin_id}")

    db_admin=db.query(Admin).filter(Admin.id == admin_id and Admin.is_active == True).first()

    if db_admin is None:
        logger.warning(f"Admin with ID {admin_id} not found or is inactive")
        raise HTTPException(status_code=404,detail="Admin not found")
    db_admin.is_active=False
    db_admin.is_deleted=True

    db.commit()
    logger.success(f"Admin {admin_id} deleted successfully")
    return {"message":"admin deleted successfully"}





#*************************************forget_password_by_token************************************


@adminauth.put("/forget_admin_password_by_token")
def forget_user_detail(new_password:str,token=Header(...)):
    admin_id=decode_token_a_id(token)
    logger.info(f"Attempting to reset password for admin ID: {admin_id}")
    db_admin=db.query(Admin).filter(Admin.id == admin_id,Admin.is_active == True,Admin.is_deleted == False).first()

    if db_admin is None:
        logger.warning(f"Admin with ID {admin_id} not found")
        raise HTTPException(status_code=404,detail="admin not found")
    db_admin.password=pwd_context.hash(new_password)
    
    db.commit()

    logger.success(f"Password reset successfully for admin ID: {admin_id}")
    return "forget  password successfully"


    

#*******************************************Reset_Password_by_token***************************


@adminauth.put("/reset_admin_Password_by_token")
def reset_password( user_oldpass: str, user_newpass: str,token=Header(...)):
    admin_id=decode_token_a_id(token)
    logger.info(f"Attempting to reset password for user ID: {admin_id}")
    db_admin = db.query(Admin).filter(Admin.id == admin_id,Admin.is_active == True,Admin.is_deleted == False).first()

    if db_admin is None:
        logger.warning(f"User with ID {admin_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    
    if pwd_context.verify(user_oldpass , db_admin.password):
        db_admin.password = pwd_context.hash(user_newpass)
        db.commit()
        logger.success(f"Password reset successfully for user ID: {admin_id}") 
        return "Password reset successfully"
    else:
        logger.warning(f"Old password not matched for user ID: {admin_id}")
        return "old password not matched"
    


#**************************************logging_admin**************************************



@adminauth.get("/logging_admin")
def logging_user(u_name:str, password:str):
    # breakpoint()
    logger.info(f"Attempting to log in user with username: {u_name}")
    db_admin = db.query(Admin).filter(Admin.u_name == u_name,Admin.is_active == True,Admin.is_deleted == False).first()
    if db_admin is None:
        logger.warning(f"User with username {u_name} not found or inactive")
        raise HTTPException(status_code=404, detail="User not found")
    
    if not pwd_context.verify(password, db_admin.password):
        logger.warning(f"Incorrect password attempt for username: {u_name}")
        raise HTTPException(status_code=404, detail="Password is incorrect")
    
    access_token = admin_logging_token(db_admin.id, u_name, db_admin.u_name)

    logger.success(f"User {u_name} logged in successfully")
    return  access_token
