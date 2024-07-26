from fastapi import HTTPException,APIRouter,Header
from src.models.sofa import Sofas
from src.models.admin import Admin
from src.schemas.sofa import CreateSofa,CreateSofaPatch
from database.database import sessionLocal
from passlib.context import CryptContext
from src.utils.token import decode_token_a_id
from logs.log_config import logger
from datetime import datetime 
import uuid




sofaauth=APIRouter(tags=["Sofa"])

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")



#---------------------------------------------------create_sofa------------------------------------------

@sofaauth.post("/create_sofa",response_model=CreateSofa)
def create_sofa(sofa:CreateSofa):
    logger.info(f"sofas created")

    new_sofa=Sofas(
        id = str(uuid.uuid4()),
        user_id = sofa.user_id,
        category=sofa.category,
        description=sofa.description,
        warranty_period=sofa.warranty_period,

    )
    db.add(new_sofa)
    db.commit()

    logger.success(f"sofas created successfully with category: {new_sofa.category}")
    return new_sofa






#-------------------------------------------------get_sofa_details-------------------------------------



@sofaauth.get("/get_sofas_detail",response_model=list[CreateSofa])
def get_users_sofas_detail(token =Header(...)):
    admin_name=decode_token_a_id(token)

    db_admin=db.query(Admin).filter(Admin.u_name == admin_name,Admin.is_active == True,Admin.is_deleted == False).first()

    if db_admin is  None:
        raise HTTPException(status_code=200,detail="invalid token")
    
    logger.info(f"Fetching details for sofas ID")
    db_sofa=db.query(Sofas).filter(Sofas.is_active == True,Sofas.is_deleted == False).all()
    
    if db_sofa is None:
        logger.warning(f"Sofa with ID  not found or is inactive")
        raise HTTPException(status_code=404,detail= "Product sofa not found")
    
    logger.success(f"Sofa details fetched successfully for sofa ID")
    return db_sofa






#-------------------------------------------patch_sofas-----------------------------------------


@sofaauth.patch("/update_sofas_detail_using_patch", response_model=CreateSofaPatch)
def update_sofas_detail(sofa: CreateSofaPatch,sofa_id:str):

    logger.info(f"Attempting to update sofa details for sofa ID: {sofa_id}")
    find_sofa = db.query(Sofas).filter(Sofas.id == sofa_id,Sofas.is_active == True).first()
    
    if not find_sofa:
        logger.warning(f"Sofa with ID {sofa_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="Sofa not found")
    
    update_data = sofa.dict(exclude_unset=True)
    
    for key, value in update_data.items():
            
        setattr(find_sofa,key,value)
    db.commit()
    db.refresh(find_sofa) 

    logger.success(f"Sofa details updated successfully for sofa ID: {sofa_id}")
    return find_sofa 





#-------------------------------------------put_sofas-----------------------------------------


@sofaauth.put("/update_sofas_detail_using_put", response_model=CreateSofa)
def update_sofas_detail(sofa: CreateSofa,sofa_id:str):

    logger.info(f"Attempting to update sofa details for sofa ID: {sofa_id}")
    find_sofa = db.query(Sofas).filter(Sofas.id == sofa_id,Sofas.is_active == True).first()
    
    if not find_sofa:
        logger.warning(f"Sofa with ID {sofa_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="Sofa not found")
    
    find_sofa.user_id = sofa.user_id,
    find_sofa.category=sofa.category,
    find_sofa.description=sofa.description,
    find_sofa.warranty_period=sofa.warranty_period,

    db.commit()
    db.refresh(find_sofa) 

    logger.success(f"Sofa details updated successfully for sofa ID: {sofa_id}")
    return find_sofa 





#************************************delete_sofas_details_by_token *******************************


@sofaauth.delete("/delete_sofa_detail_by_token")
def delete_sofas_detail(sofa_id : str):

    logger.info(f"Attempting to delete sofa with ID: {sofa_id}")

    db_sofa=db.query(Sofas).filter(Sofas.id == sofa_id and Sofas.is_active == True).first()

    if db_sofa is None:
        logger.warning(f"Sofas with ID {sofa_id} not found or is inactive")
        raise HTTPException(status_code=404,detail="Sofa not found")
    db_sofa.is_active=False
    db_sofa.is_deleted=True

    db.commit()
    logger.success(f"Sofa {sofa_id} deleted successfully")
    return {"message":"sofa deleted successfully"}