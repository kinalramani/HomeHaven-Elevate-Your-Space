from fastapi import HTTPException,APIRouter,Header
from src.models.curtains import Curtains
from src.models.admin import Admin
from src.schemas.curtains import CreateCurtains,CreateCurtainsPatch
from database.database import sessionLocal
from passlib.context import CryptContext
from src.utils.token import decode_token_a_id
from logs.log_config import logger
from datetime import datetime 
import uuid




curtainauth=APIRouter(tags=["Curtains"])

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")



#---------------------------------------------------create_curtain------------------------------------------

@curtainauth.post("/create_curtain",response_model=CreateCurtains)
def create_curtain(curtain:CreateCurtains):
    
    new_curtain=Curtains(
        id = str(uuid.uuid4()),
        user_id=curtain.user_id,
        category=curtain.category,
        description=curtain.description,
        warranty_period=curtain.warranty_period,

    )
    db.add(new_curtain)
    db.commit()

    logger.success(f"curtain created successfully with category: {new_curtain.category}")
    return new_curtain






#-------------------------------------------------get_curtain_details-------------------------------------



@curtainauth.get("/get_curtain_detail",response_model=list[CreateCurtains])
def get_users_curtain_detail(token =Header(...)):
    curtain_name=decode_token_a_id(token)

    db_curtain=db.query(Admin).filter(Admin.u_name == curtain_name,Admin.is_active == True,Admin.is_deleted == False).first()

    if db_curtain is  None:
        raise HTTPException(status_code=200,detail="invalid token")
    
    logger.info(f"Fetching details for scurtain ID")
    db_curtain=db.query(Curtains).filter(Curtains.is_active == True,Curtains.is_deleted == False).all()
    
    if db_curtain is None:
        logger.warning(f"curtain with ID  not found or is inactive")
        raise HTTPException(status_code=404,detail= "Product curtain not found")
    
    logger.success(f"Curtain details fetched successfully for curtain ID")
    return db_curtain






#-------------------------------------------patch_curtain-----------------------------------------


@curtainauth.patch("/update_curtaians_detail_using_patch", response_model=CreateCurtainsPatch)
def update_curtains_detail(curtain: CreateCurtainsPatch,curtain_id:str):

    logger.info(f"Attempting to update curtains details for curtain ID: {curtain_id}")
    find_curtain = db.query(Curtains).filter(Curtains.id == curtain_id,Curtains.is_active == True).first()
    
    if not find_curtain:
        logger.warning(f"Curtains with ID {curtain_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="Curatains not found")
    
    update_data = curtain.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(find_curtain,key,value)
   
   
    db.commit()
    db.refresh(find_curtain) 

    logger.success(f"Curtain details updated successfully for curtain ID: {curtain_id}")
    return find_curtain 





#-------------------------------------------put_curtain-----------------------------------------


@curtainauth.put("/update_curtains_detail_using_put", response_model=CreateCurtains)
def update_curtains_detail(curtain: CreateCurtains,curtain_id:str):

    logger.info(f"Attempting to update curtains details for curtain ID: {curtain_id}")
    find_curtain = db.query(Curtains).filter(Curtains.id == curtain_id,Curtains.is_active == True).first()
    
    if not find_curtain:
        logger.warning(f"Curtain with ID {curtain_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="Curtain not found")
    
    find_curtain.user_id=curtain.user_id,
    find_curtain.category=curtain.category,
    find_curtain.description=curtain.description,
    find_curtain.warranty_period=curtain.warranty_period,
    
    db.commit()
    db.refresh(find_curtain) 

    logger.success(f"Curtain details updated successfully for curtain ID: {curtain_id}")
    return find_curtain 





#************************************delete_curtains_details  *******************************


@curtainauth.delete("/delete_curtains_detail")
def delete_curtains_detail(curtain_id : str):

    logger.info(f"Attempting to delete curtain with ID: {curtain_id}")

    db_curtain=db.query(Curtains).filter(Curtains.id == curtain_id and Curtains.is_active == True).first()

    if db_curtain is None:
        logger.warning(f"Curtain with ID {curtain_id} not found or is inactive")
        raise HTTPException(status_code=404,detail="Curtain not found")
    db_curtain.is_active=False
    db_curtain.is_deleted=True

    db.commit()
    logger.success(f"Curtain {curtain_id} deleted successfully")
    return {"message":"curtain deleted successfully"}