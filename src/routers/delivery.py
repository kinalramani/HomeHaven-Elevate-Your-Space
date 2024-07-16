from fastapi import HTTPException,APIRouter,Header
from src.models.delivery import Delivery
from src.models.admin import Admin
from src.models.order import Order
from src.models.user import User
from src.schemas.delivery import DeliveryBase
from database.database import sessionLocal
from passlib.context import CryptContext
from src.utils.token import decode_token_a_name
from logs.log_config import logger
from src.utils.otp import send_email
from datetime import datetime 
import uuid





deliveryauth=APIRouter(tags=["Delivery"])

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")



# #--------------------------------------------------Get all pending delivery by admin----------------------------------


@deliveryauth.get("/get_all_pending_details_by_admin",response_model=list[DeliveryBase])
def get_user_all_details(token= Header(...)):
    admin_name=decode_token_a_name(token)
    db_admin=db.query(Admin).filter(Admin.u_name == admin_name,Admin.is_active == True,Admin.is_deleted == False).first()

    if db_admin is  None:
        raise HTTPException(status_code=200,detail="invalid token")
    
    logger.info(f"Fetching all details ")
    db_delivery=db.query(Delivery).filter(Delivery.is_active == True,Delivery.is_deleted == False,Delivery.is_deleted == False).all()

    if db_delivery is None:
        logger.warning(f"No active delivery")
        raise HTTPException(status_code=404,detail="delivery not found")
    
    logger.success(f"Delivery details fetched successfully")
    return db_delivery



#---------------------------------------------------------Update Delivery----------------------------------------


@deliveryauth.put("/Update_deliveries", response_model=DeliveryBase)
def update_delivery(delivery_id: str, delivery: DeliveryBase):
    existing_delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if existing_delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")

    for var, value in vars(delivery).items():
        setattr(existing_delivery, var, value) if value else None

    db.commit()
    db.refresh(existing_delivery)
    
    # Check and update order status if delivery status is 'done'
    if existing_delivery.status == "done":
        order = db.query(Order).filter(Order.id == existing_delivery.order_id).first()
        if order:
            order.status = "done"
            db.commit()
            db.refresh(order)

    return existing_delivery


#-----------------------------------------------------confirm delivery--------------------------------


@deliveryauth.put("/confirm_delivery")
def confirm_reservation(reserve_id: str):
    
    db_delivery = db.query(Delivery).filter(Delivery.id == reserve_id, Delivery.is_active == True, Delivery.is_deleted == False).first()
    if db_delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")
    
    db_delivery.status = "confirmed"
    db.commit()

    db_order = db.query(Order).filter(Order.id == db_delivery.order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order.status = "done"
    db.commit()
    
    user = db.query(User).filter(User.id == db_delivery.user_name).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
   
    user_email = user.e_mail
    
    success, message = send_email(
        sender_email="kinalramni14@gmail.com",
        receiver_email=user_email,
        password="irnyitpcqjlebnmv",
        subject="Delivery Confirmation",
        body=f"Your delivery for the order ID {db_order.id} has been completed successfully."
    )

    if not success:
        raise HTTPException(status_code=500, detail=message)

    return {"message": "Delivery confirmed and notification sent to user", "order_id": db_order.id, "delivery_id": db_delivery.id}

   
