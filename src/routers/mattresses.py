from fastapi import HTTPException,APIRouter,Header
from src.models.mattress import Mattresses
from src.models.admin import Admin
from src.schemas.mattresses import CreateMattress,CreateMattressPatch
from database.database import sessionLocal
from passlib.context import CryptContext
from src.utils.token import decode_token_a_name
from logs.log_config import logger
from datetime import datetime 
import uuid




mattressauth=APIRouter(tags=["Mattress"])

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")



#---------------------------------------------------create_Mattress------------------------------------------

@mattressauth.post("/create_mattress",response_model=CreateMattress)
def create_mattress(mattress:CreateMattress):

    # find_mattress = db.query(Mattresses).filter(Mattresses.category == mattress.category).first()

    # if find_mattress:
    #     logger.warning(f"Mattress with category {Mattresses.category} already exists")
    #     raise HTTPException(status_code=400,detail="Same category found please try with another one")
    

    new_mattress=Mattresses(
        id = str(uuid.uuid4()),
        user_id=mattress.user_id,
        category=mattress.category,
        description=mattress.description,
        warranty_period=mattress.warranty_period,

    )
    db.add(new_mattress)
    db.commit()

    logger.success(f"Mattress created successfully with category: {new_mattress.category}")
    return new_mattress






#-------------------------------------------------get_mattress_details-------------------------------------



@mattressauth.get("/get_mattress_detail",response_model=list[CreateMattress])
def get_users_mattress_detail(token =Header(...)):
    mattress_name=decode_token_a_name(token)

    db_mattress=db.query(Admin).filter(Admin.u_name == mattress_name,Admin.is_active == True,Admin.is_deleted == False).first()

    if db_mattress is  None:
        raise HTTPException(status_code=200,detail="invalid token")
    
    logger.info(f"Fetching details for mattress ID")
    db_mattress=db.query(Mattresses).filter(Mattresses.is_active == True,Mattresses.is_deleted == False).all()
    
    if db_mattress is None:
        logger.warning(f"mattress with ID  not found or is inactive")
        raise HTTPException(status_code=404,detail= "Product mattress not found")
    
    logger.success(f"Mattress details fetched successfully for mattress ID")
    return db_mattress






#-------------------------------------------patch_mattress-----------------------------------------


@mattressauth.patch("/update_mattress_detail_using_patch", response_model=CreateMattressPatch)
def update_mattress_detail(mattress: CreateMattressPatch,mattress_id:str):

    logger.info(f"Attempting to update mattress details for mattress ID: {mattress_id}")
    find_mattress = db.query(Mattresses).filter(Mattresses.id == mattress_id,Mattresses.is_active == True).first()
    
    if not find_mattress:
        logger.warning(f"Mattress with ID {mattress_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="Mattress not found")
    
    update_data = mattress.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(find_mattress,key,value)
    
    db.commit()
    db.refresh(find_mattress) 

    logger.success(f"Mattress details updated successfully for mattress ID: {mattress_id}")
    return find_mattress 





#-------------------------------------------put_mattress-----------------------------------------


@mattressauth.put("/update_mattress_detail_using_put", response_model=CreateMattress)
def update_mattress_detail(mattress: CreateMattress,mattress_id:str):

    logger.info(f"Attempting to update mattress details for mattress ID: {mattress_id}")
    find_mattress = db.query(Mattresses).filter(Mattresses.id == mattress_id,Mattresses.is_active == True).first()
    
    if not find_mattress:
        logger.warning(f"Mattress with ID {mattress_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="Mattress not found")
    
    find_mattress.user_id=mattress.user_id,
    find_mattress.category=mattress.category,
    find_mattress.description=mattress.description,
    find_mattress.warranty_period=mattress.warranty_period,
    
    db.commit()
    db.refresh(find_mattress) 

    logger.success(f"Mattress details updated successfully for mattress ID: {mattress_id}")
    return find_mattress 





#************************************delete_mattress_details_by_token *******************************


@mattressauth.delete("/delete_mattress_detail_by_token")
def delete_mattress_detail(mattress_id : str):

    logger.info(f"Attempting to delete mattress with ID: {mattress_id}")

    db_mattress=db.query(Mattresses).filter(Mattresses.id == mattress_id and Mattresses.is_active == True).first()

    if db_mattress is None:
        logger.warning(f"Mattress with ID {mattress_id} not found or is inactive")
        raise HTTPException(status_code=404,detail="Mattress not found")
    db_mattress.is_active=False
    db_mattress.is_deleted=True

    db.commit()
    logger.success(f"Mattress {mattress_id} deleted successfully")
    return {"message":"mattress deleted successfully"}