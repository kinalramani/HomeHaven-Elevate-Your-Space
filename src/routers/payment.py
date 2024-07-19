from fastapi import HTTPException,APIRouter,Header
from src.models.order import Order
from src.models.admin import Admin
from src.schemas.payment import PaymentBase,PaymentBasepatch
from database.database import sessionLocal
from src.models.payment import Payment
from passlib.context import CryptContext
from src.utils.token import decode_token_a_id
from logs.log_config import logger
from src.utils.otp import send_email
from datetime import datetime 
import uuid





paymentauth=APIRouter(tags=["Payment"])

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")



#--------------------------------------------------register payment------------------------------------------


@paymentauth.post("/create_payment",response_model=PaymentBase)
def create_payment(payment:PaymentBase):
    
    db_order=db.query(Order).filter(Order.id == payment.order_id).first()

    if db_order is None:
        raise HTTPException(status_code=403,detail="order not found")
    
    amount = db_order.price
    
    new_payment=Payment(
        id = str(uuid.uuid4()),
        user_id=payment.user_id,
        order_id = payment.order_id,
        payment_method =payment.payment_method,
        payment_date = payment.payment_date,
        amount = amount,
        status = payment.status,
        transaction_id = payment.transaction_id,
        currency = payment.currency,

    )
    db.add(new_payment)
    db.commit()

    logger.success(f"Payment created successfully with id: {new_payment.id}")
    return new_payment


#-------------------------------------------------------get payment details by admin---------------------------------


@paymentauth.get("/get_payment_detail",response_model=list[PaymentBase])
def get_users_pyament_detail(token =Header(...)):
    admin_name=decode_token_a_id(token)

    db_payment=db.query(Admin).filter(Admin.u_name == admin_name,Admin.is_active == True,Admin.is_deleted == False).first()

    if db_payment is  None:
        raise HTTPException(status_code=200,detail="invalid token")
    
    logger.info(f"Fetching details for payment ID")
    db_payment=db.query(Payment).filter(Payment.is_active == True,Payment.is_deleted == False).all()
    
    if db_payment is None:
        logger.warning(f"Payment with ID  not found or is inactive")
        raise HTTPException(status_code=404,detail= "Payment not found")
    
    logger.success(f"Payment details fetched successfully for payment ID")
    return db_payment



#--------------------------------------------------------update paymentusing patch----------------------------------

@paymentauth.patch("/update_paymen_using_patch", response_model=PaymentBasepatch)
def update_payment(payment: PaymentBasepatch,id:str):
    
    db_payments = db.query(Payment).filter(Payment.id == id, Payment.is_active == True,Payment.is_deleted==False).first()

    if  db_payments  is None:
        raise HTTPException(status_code=404, detail="payment not found")

    for field_name, value in payment.dict().items():
        if value is not None:
            setattr( db_payments , field_name, value)

    db.commit()
    return  db_payments



#---------------------------------------------------------update payment using put----------------------------------

@paymentauth.put("/update_payment_using_put", response_model=PaymentBase)
def update_payment(payment: PaymentBase,id:str):
    
    db_payments = db.query(Payment).filter(Payment.id == id, Payment.is_active == True,Payment.is_deleted==False).first()

    if  db_payments  is None:
        raise HTTPException(status_code=404, detail="payment not found")

    db_payments.user_id = payment.user_id,
    db_payments.order_id = payment.order_id,
    db_payments.payment_method = payment.payment_method,
    db_payments.payment_date = payment.payment_date,
    db_payments.amount = payment.amount,
    db_payments.status = payment.status,
    db_payments.transaction_id = payment.transaction_id,
    db_payments.currency = payment.currency,
    

    db.commit()
    return  db_payments


#---------------------------------------------------------------payment delete------------------------------------


@paymentauth.delete("/delete_payments")
def delete_product(id:str):
    db_payments = db.query(Payment).filter(Payment.id==id,Payment.is_active==True,Payment.is_deleted==False).first()
    if db_payments is None:
        raise HTTPException(status_code=404,detail="payment not found")
    db_payments.is_active=False
    db_payments.is_deleted =True
    db.commit()
    return {"message": "payment deleted successfully"}



#-------------------------------------------------create_payment_internet---------------------------------


@paymentauth.post("/make_payment", response_model=PaymentBase)
def make_payment(payment: PaymentBase):
    db_order = db.query(Order).filter(Order.id == payment.order_id).first()

    if db_order is None:
        raise HTTPException(status_code=403, detail="order not found")
    
    amount = db_order.price
    
    new_payment = Payment(
        id=str(uuid.uuid4()),
        user_id=payment.user_id,
        order_id=payment.order_id,
        payment_method=payment.payment_method,
        payment_date=payment.payment_date,
        amount=amount,
        status=payment.status,
        transaction_id=payment.transaction_id,
        currency=payment.currency,
    )
    db.add(new_payment)
    db.commit()

    logger.success(f"Payment created successfully with id: {new_payment.id}")

    # Send email notification
    user_email = "jenistalaviya3178@gmail.com"  # Replace with actual recipient email
    subject = "Payment Confirmation"
    body = f"Your payment with ID {new_payment.id} has been successfully processed."
    send_email(subject, user_email, body)
    
    return new_payment