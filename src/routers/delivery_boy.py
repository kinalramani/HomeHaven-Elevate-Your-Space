from fastapi import HTTPException,APIRouter,Header
from src.models.delivery_boy import DeliveryBoy
from src.models.admin import Admin
from src.models.order import Order
from src.schemas.delivery_boy import DeliveryBoyBase,DeliveryBoyBasePatch
from database.database import sessionLocal
from passlib.context import CryptContext
from src.utils.token import decode_token_a_name
from logs.log_config import logger
from datetime import datetime 
import uuid





deliveryboyauth=APIRouter(tags=["DeliveryBoy"])

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")



# #--------------------------------------------------Get all pending delivery by admin----------------------------------


@deliveryboyauth.post("/create_delivery_boy",response_model=DeliveryBoyBase)
def create_delivery_boy_detail(deliveryboy:DeliveryBoyBase):
    logger.info(f"register delivery boy detail")

    new_deliveryboy=DeliveryBoy(
        id = str(uuid.uuid4()),
        name = deliveryboy.name,
        mo_number=deliveryboy.mo_number,
        delivery_id=deliveryboy.delivery_id,

    )
    db.add(new_deliveryboy)
    db.commit()

    logger.success(f"Deliveryboy created successfully with name: {new_deliveryboy.name}")
    return new_deliveryboy



#------------------------------------------------------get delivery boy details by admin----------------------------------


@deliveryboyauth.get("/get_delivery_boy_detail",response_model=list[DeliveryBoyBase])
def get_users_mattress_detail(token =Header(...)):
    deliveryboy_name=decode_token_a_name(token)

    db_deliveryboy=db.query(Admin).filter(Admin.u_name == deliveryboy_name,Admin.is_active == True,Admin.is_deleted == False).first()

    if db_deliveryboy is  None:
        raise HTTPException(status_code=200,detail="invalid token")
    
    logger.info(f"Fetching details for deliveryboy ID")
    db_deliveryboy=db.query(DeliveryBoy).filter(DeliveryBoy.is_active == True,DeliveryBoy.is_deleted == False).all()
    
    if db_deliveryboy is None:
        logger.warning(f"deliveryboy with ID  not found or is inactive")
        raise HTTPException(status_code=404,detail= "deliveryboy not found")
    
    logger.success(f"Deliveryboy details fetched successfully for deliveryboy ID")
    return db_deliveryboy




#----------------------------------------------------Update deliveryboy details using patch------------------------


@deliveryboyauth.patch("/update_deliveryboy_detail_using_patch", response_model=DeliveryBoyBasePatch)
def update_deliveryboy_detail(deliveryboy: DeliveryBoyBasePatch,deliveryboy_id:str):

    logger.info(f"Attempting to update deliveruboy details for deliveryboy  ID: {deliveryboy_id}")
    find_deliveryboy = db.query(DeliveryBoy).filter(DeliveryBoy.id == deliveryboy_id,DeliveryBoy.is_active == True).first()
    
    if not find_deliveryboy:
        logger.warning(f"Deliveryboy with ID {deliveryboy_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="Deliveryboy not found")
    
    update_data = deliveryboy.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(find_deliveryboy,key,value)
    
    db.commit()
    db.refresh(find_deliveryboy) 

    logger.success(f"Deliveryboy details updated successfully for deliveryboy ID: {deliveryboy_id}")
    return find_deliveryboy 




#-----------------------------------------------Update deliveryboy details using put------------------------

@deliveryboyauth.put("/update_deliveryboy_detail_using_put", response_model=DeliveryBoyBase)
def update_deliveryboy_detail_using_put(deliveryboy: DeliveryBoyBase,deliveryboy_id:str):

    logger.info(f"Attempting to update deliveryboy details for deliveryboy ID: {deliveryboy_id}")
    find_deliveryboy = db.query(DeliveryBoy).filter(DeliveryBoy.id == deliveryboy_id,DeliveryBoy.is_active == True).first()
    
    if not find_deliveryboy:
        logger.warning(f"Deliveryboy with ID {deliveryboy_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="Deliveryboy not found")
    
    find_deliveryboy.name=deliveryboy.name,
    find_deliveryboy.mo_number=deliveryboy.mo_number,
    find_deliveryboy.delivery_id=deliveryboy.delivery_id,
    db.commit()
    db.refresh(find_deliveryboy) 

    logger.success(f"Deliveryboy details updated successfully for mattress ID: {deliveryboy_id}")
    return find_deliveryboy


#----------------------------------------------------Delete deliveryboy details---------------------------------

@deliveryboyauth.delete("/delete_deliveryboy_detail")
def delete_deliveryboy_detail(deliveryboy_id : str):

    logger.info(f"Attempting to delete deliveryboy with ID: {deliveryboy_id}")

    db_deliveryboy=db.query(DeliveryBoy).filter(DeliveryBoy.id == deliveryboy_id and DeliveryBoy.is_active == True).first()

    if db_deliveryboy is None:
        logger.warning(f"Deliveryboy with ID {deliveryboy_id} not found or is inactive")
        raise HTTPException(status_code=404,detail="Deliveryboy not found")
    db_deliveryboy.is_active=False
    db_deliveryboy.is_deleted=True

    db.commit()
    logger.success(f"Deliveryboy {deliveryboy_id} deleted successfully")
    return {"message":"deliveryboy deleted successfully"}










    
