from fastapi import HTTPException,APIRouter,Header
from src.models.customer_requirements import CustomerRequirements
from src.models.admin import Admin
from src.schemas.customer_requirements import CreateCustReq,CreateCustReqPatch
from database.database import sessionLocal
from passlib.context import CryptContext
from src.utils.token import decode_token_a_id
from logs.log_config import logger
from src.models.curtains import Curtains
from src.models.mattress import Mattresses
from src.models.sofa import Sofas
from datetime import datetime 
import uuid




custreqauth=APIRouter(tags=["CustomerRequirements"])

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")



#---------------------------------------------------create_customer_requirements_details------------------------------------------

@custreqauth.post("/create_customer_requirements_details",response_model=CreateCustReq)
def create_customer_requirements_details(custreq:CreateCustReq):
    product_1=db.query(Sofas).filter(Sofas.category == custreq.product_name,Sofas.is_active == True,Sofas.is_deleted == False).first()
    product_1=custreq.product_name

    if product_1 is None:
        raise HTTPException(status_code=404,detail="product_1 is not found")
    
    product_2=db.query(Mattresses).filter(Mattresses.category == custreq.product_name,Mattresses.is_active == True,Mattresses.is_deleted == False).first()
    product_2=custreq.product_name

    if product_2 is None:
        raise HTTPException(status_code=404,detail="product_2 is not found")
    
    product_3=db.query(Curtains).filter(Curtains.category == custreq.product_name,Curtains.is_active == True,Curtains.is_deleted == False).first()
    product_3=custreq.product_name

    if product_3 is None:
        raise HTTPException(status_code=404,detail="product_3 is not found")
    
    
    new_custreq=CustomerRequirements(
        id = str(uuid.uuid4()),
        description=custreq.description,
        Customer_id=custreq.Customer_id,
        product_name=custreq.product_name,
        additional_notes =custreq.additional_notes,

    )
    db.add(new_custreq)
    db.commit()

    return new_custreq






#-------------------------------------------------get_custreq_details-------------------------------------




@custreqauth.get("/get_all_cust_detail",response_model=list[CreateCustReq])
def get_custreq_detail(token =Header(...)):
    custreq_name=decode_token_a_id(token)

    db_custreq=db.query(Admin).filter(Admin.u_name == custreq_name,Admin.is_active == True,Admin.is_deleted == False).first()

    if db_custreq is  None:
        raise HTTPException(status_code=200,detail="invalid token")
    
    logger.info(f"Fetching details for custreq ID")
    db_custreq=db.query(CustomerRequirements).filter(CustomerRequirements.is_active == True,CustomerRequirements.is_deleted == False).all()
    
    if db_custreq is None:
        logger.warning(f"custreq with ID  not found or is inactive")
        raise HTTPException(status_code=404,detail= "Product custreq not found")
    
    logger.success(f"Custreq details fetched successfully for custreq ID")
    return db_custreq






#-------------------------------------------patch_custreq-----------------------------------------


@custreqauth.patch("/update_custreq_detail_using_patch", response_model=CreateCustReqPatch)
def update_custreq_detail(custreq: CreateCustReqPatch,custreq_id:str):  
    

    logger.info(f"Attempting to update custreq details for custreq ID: {custreq_id}")
    find_custreq = db.query(CustomerRequirements).filter(CustomerRequirements.id == custreq_id,CustomerRequirements.is_active == True).first()
    
    if not find_custreq:
        logger.warning(f"Custreq with ID {custreq_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="Custreq not found")
    
    update_data = custreq.dict(exclude_unset=True)
    
    for key, value in update_data.items():   
        setattr(find_custreq,key,value)

    db.commit()
    db.refresh(find_custreq) 

    logger.success(f"Custreq details updated successfully for custreq ID: {custreq_id}")
    return find_custreq 





#-------------------------------------------put_custreq-----------------------------------------


@custreqauth.put("/update_custreq_detail_using_put", response_model=CreateCustReq)
def update_custreq_detail(custreq: CreateCustReq,custreq_id:str):

    logger.info(f"Attempting to update custreq details for cust ID: {custreq_id}")
    find_custreq = db.query(CustomerRequirements).filter(CustomerRequirements.id == custreq_id,CustomerRequirements.is_active == True).first()
    
    if not find_custreq:
        logger.warning(f"Custreq with ID {custreq_id} not found or is inactive")
        raise HTTPException(status_code=404, detail="custreq not found")
    
    find_custreq.description=custreq.description,
    find_custreq.Customer_id=custreq.Customer_id,
    find_custreq.product_name=custreq.product_name,
    find_custreq.additional_notes =custreq.additional_notes,
    
    
    db.commit()
    db.refresh(find_custreq) 

    logger.success(f"Custreq details updated successfully for customer ID: {custreq_id}")
    return find_custreq 





#************************************delete_custreq_details *******************************


@custreqauth.delete("/delete_custreq_detail")
def delete_custreq_detail(custreq_id : str):

    logger.info(f"Attempting to delete custreq with ID: {custreq_id}")

    db_custreq=db.query(CustomerRequirements).filter(CustomerRequirements.id == custreq_id and CustomerRequirements.is_active == True).first()

    if db_custreq is None:
        logger.warning(f"Custreq with ID {custreq_id} not found or is inactive")
        raise HTTPException(status_code=404,detail="Custreq not found")
    db_custreq.is_active=False
    db_custreq.is_deleted=True

    db.commit()
    logger.success(f"Custreq {custreq_id} deleted successfully")
    return {"message":"Custreq deleted successfully"}