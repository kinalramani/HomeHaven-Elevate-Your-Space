from fastapi import HTTPException,APIRouter,Header
from src.models.order import Order
from src.models.admin import Admin
from src.models.user import User
from src.schemas.order import OrderCreate,OrderBase,OrderUpdate,OrderBasePatch
from database.database import sessionLocal
from src.models.delivery_boy import DeliveryBoy
from passlib.context import CryptContext
from src.utils.token import decode_token_a_id
from logs.log_config import logger
from src.models.curtains import Curtains
from src.models.mattress import Mattresses
from src.models.sofa import Sofas
from src.models.delivery import Delivery
from datetime import datetime 
import uuid





orderauth=APIRouter(tags=["Order"])

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


#---------------------------------------------------create_order_details------------------------------------------

@orderauth.post("/create_orders_details",response_model=OrderBase)
def create_order_details(order:OrderBase):
    logger.info("Creating a new order")

    new_order=Order(
        id = str(uuid.uuid4()),
        req_id = order.req_id,
        user_id = order.user_id,
        description = order.description,
        product_id = order.product_id,
        notes = order.notes,
        price = order.price,
        status = "pending",
    
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    logger.success(f"Order created with ID: {new_order.id}")

    

    new_delivery=Delivery(
        id = str(uuid.uuid4()),
        order_id = new_order.id,
        user_name = new_order.user_id,
        address = new_order.user_id,
        payment = new_order.price,
        status = new_order.status,
    )

    
    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)
    logger.success(f"Delivery created for order ID: {new_order.id}")

    return new_order

#-----------------------------------------------------------get all orders---------------------------------


@orderauth.get("/get_all_order_details",response_model=list[OrderBase])
def get_all_order_details(token = Header(...)):
    logger.info("Decoding token and fetching order details")
    order_details=decode_token_a_id(token)

    db_order=db.query(Admin).filter(Admin.u_name == order_details,Admin.is_active == True,Admin.is_deleted == False).first()

    if db_order is  None:
        logger.warning("Invalid token")
        raise HTTPException(status_code=200,detail="invalid token")
    
    logger.info(f"Fetching details for order ID")
    db_order=db.query(Order).filter(Order.is_active == True,Order.is_deleted == False).all()
    
    if db_order is None:
        logger.warning(f"order with ID  not found or is inactive")
        raise HTTPException(status_code=404,detail= "Product order not found")
    
    logger.success(f"order details fetched successfully for order ID")
    return db_order



#--------------------------------------------------Get a specific order by ID---------------------------------

@orderauth.get("/get_order_detail_by_id",response_model=OrderBase)
def get_employee_detail(order_id : str):
    logger.info(f"Fetching details for order ID: {order_id}")
    db_order=db.query(Order).filter(Order.id == order_id,Order.is_active == True,Order.is_deleted == False).first()
    
    if db_order is None:
        logger.warning(f"Order with ID {order_id} not found or is inactive")
        raise HTTPException(status_code=404,detail= "order not found")
    
    logger.success(f"Order details fetched successfully for user ID: {order_id}")
    return db_order



#---------------------------------------------------Update an order using patch----------------------------


@orderauth.patch("/update_orders_using_patch", response_model=OrderBasePatch)
def update_order_using_patch(order_id: str, order: OrderBasePatch):

    logger.info(f"Updating order with ID: {order_id}")
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        logger.warning(f"Order with ID {order_id} not found")
        raise HTTPException(status_code=404, detail="Order not found")
    
    
    for key, value in order.dict().items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    logger.info(f"Order with ID: {order_id} updated successfully")


    db_delivery = db.query(Delivery).filter(Delivery.id == db_order.id).first()
    if db_delivery is None:
        logger.warning(f"Delivery for order ID {order_id} not found")
        raise HTTPException(status_code=404, detail="Delivery not found")
    
    
    for key, value in db_order.dict().items():
        setattr(db_delivery, key, value)
    db.commit()
    db.refresh(db_delivery)

    logger.success(f"Delivery for order ID: {order_id} updated successfully")

    return db_order



#---------------------------------------------------Update an order using put----------------------------


@orderauth.put("/update_orders_using_put", response_model=OrderBase)
def update_order_using_patch(order_id: str, order: OrderBasePatch):

    logger.info(f"Updating order with ID: {order_id}")
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        logger.warning(f"Order with ID {order_id} not found")
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order.req_id = order.req_id
    db_order.user_id = order.user_id,
    db_order.description = order.description,
    db_order.product_id = order.product_id,
    db_order.notes = order.notes,
    db_order.price = order.price,
    db_order.status = order.status,

    db.commit()
    db.refresh(db_order)
    logger.success(f"Order with ID: {order_id} updated successfully")

    db_delivery=db.query(Delivery).filter(Delivery.id == db_order.id).first()

    if db_delivery is None:
        logger.warning(f"Delivery for order ID {order_id} not found")
        raise HTTPException(status_code=404,detail="delivery not db_order")
    
    db_delivery.order_id = db_order.id,
    db_delivery.user_name = db_order.user_id,
    db_delivery.address = db_order.user_id,
    db_delivery.payment = db_order.price,
    db_delivery.status = db_order.status,
    db_delivery.delivery_boy = db_delivery.delivery_boy,

    
    db.commit()
    db.refresh(db_delivery)
    logger.success(f"Delivery for order ID: {order_id} updated successfully")
    return db_order


#------------------------------------------------------------Delete an order------------------------


@orderauth.delete("/delete_order_detail")
def delete_order_detail(order_id : str):

    logger.info(f"Attempting to delete order with ID: {order_id}")

    db_order=db.query(Order).filter(Order.id == order_id and Order.is_active == True).first()

    if db_order is None:
        logger.warning(f"Order with ID {order_id} not found or is inactive")
        raise HTTPException(status_code=404,detail="Order not found")
    db_order.is_active=False
    db_order.is_deleted=True

    db.commit()
    logger.success(f"Order {order_id} deleted successfully")
    return {"message":"Order deleted successfully"}