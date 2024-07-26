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
    logger.info("Decoding token and fetching delivery details")
    admin_name=decode_token_a_name(token)
    db_admin=db.query(Admin).filter(Admin.u_name == admin_name,Admin.is_active == True,Admin.is_deleted == False).first()

    if db_admin is  None:
        logger.warning("Invalid token")
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
    logger.info(f"Updating delivery with ID: {delivery_id}")

    existing_delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if existing_delivery is None:
        logger.warning(f"Delivery with ID {delivery_id} not found")
        raise HTTPException(status_code=404, detail="Delivery not found")

    for var, value in vars(delivery).items():
        setattr(existing_delivery, var, value) if value else None

    db.commit()
    db.refresh(existing_delivery)
    
    logger.success(f"Delivery with ID: {delivery_id} updated successfully")
    # Check and update order status if delivery status is 'done'
    if existing_delivery.status == "done":
        order = db.query(Order).filter(Order.id == existing_delivery.order_id).first()
        if order:
            order.status = "done"
            db.commit()
            db.refresh(order)
            logger.success(f"Order with ID: {order.id} updated to 'done' status due to delivery completion")

    return existing_delivery


#-----------------------------------------------------confirm delivery--------------------------------


@deliveryauth.put("/confirm_delivery")
def confirm_reservation(delivery_id: str):
    logger.info(f"Confirming delivery with ID: {delivery_id}")
    
    db_delivery = db.query(Delivery).filter(Delivery.id == delivery_id, Delivery.is_active == True, Delivery.is_deleted == False).first()
    if db_delivery is None:
        logger.warning(f"Delivery with ID {delivery_id} not found")
        raise HTTPException(status_code=404, detail="Delivery not found")
    
    db_delivery.status = "confirmed"
    db.commit()
    logger.info(f"Delivery with ID: {delivery_id} confirmed")


    db_order = db.query(Order).filter(Order.id == db_delivery.order_id).first()
    if db_order is None:
        logger.warning(f"Order with ID {db_delivery.order_id} not found")
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order.status = "done"
    db.commit()
    logger.success(f"Order with ID: {db_order.id} updated to 'done' status")
    
    user = db.query(User).filter(User.id == db_delivery.user_name).first()
    if user is None:
        logger.warning(f"User with ID {db_delivery.user_name} not found")
        raise HTTPException(status_code=404, detail="User not found")
    
   
    user_email = user.e_mail
    
    success, message = send_email(
        receiver_email=user_email,
        subject="Delivery Confirmation",
        body=f"Your delivery for the order ID {db_order.id} has been completed successfully."
    )

    if not success:
        logger.error(f"Failed to send email to {user_email}: {message}")
        raise HTTPException(status_code=500, detail=message)

    logger.success(f"Delivery confirmation email sent to {user_email}")
    return {"message": "Delivery confirmed and notification sent to user", "order_id": db_order.id, "delivery_id": db_delivery.id}

   
