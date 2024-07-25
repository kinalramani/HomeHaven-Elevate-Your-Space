from fastapi import HTTPException,APIRouter,Header
from src.models.order import Order
from src.models.admin import Admin
from src.models.user import User
from src.schemas.payment import PaymentBase,PaymentBasepatch,PaymentIntentRequest
from database.database import sessionLocal
from src.models.payment import Payment
from passlib.context import CryptContext
from src.utils.token import decode_token_a_id
from logs.log_config import logger
from src.utils.otp import ssend_email
from config import sender_email,password
import uuid
import stripe
from stripe import SignatureVerificationError
from logs.log_config import logger
import os




paymentauth=APIRouter(tags=["Payment"])

db=sessionLocal()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")






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
    db_payments.payment_method ="COD",
    db_payments.payment_date = payment.payment_date,
    db_payments.amount = payment.amount,
    db_payments.status = "confirm",
    db_payments.transaction_id = payment.transaction_id,
    

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


# @paymentauth.post("/make_payment", response_model=PaymentBase)
# def make_payment(payment: PaymentBase):
#     db_order = db.query(Order).filter(
#         Order.id == payment.order_id,
#         Order.is_active == True,
#         Order.is_deleted == False
#     ).first()

#     if db_order is None:
#         raise HTTPException(status_code=403, detail="Order not found")
    
#     amount = db_order.price
    
#     db_user = db.query(User).filter(User.id == payment.user_id).first()
    
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     new_payment = Payment(
#         id=str(uuid.uuid4()),
#         user_id=payment.user_id,
#         order_id=payment.order_id,
#         payment_method="COD",
#         payment_date=payment.payment_date,
#         amount=amount,
#         status="confirm",
#         transaction_id=payment.transaction_id,
#     )
#     db.add(new_payment)
#     db.commit()

#     # Send email notification
#     user_email = db_user.e_mail  # Corrected attribute name
#     subject = "Payment Confirmation"
#     body = f"Your payment with ID {new_payment.id} has been successfully processed."
    
    
    
    
#     try:
#         success, message = ssend_email(subject, user_email, body, sender_email, password)
#         if not success:
#             raise HTTPException(status_code=500, detail=f"Failed to send email: {message}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

#     return new_payment



@paymentauth.post("/create_payment_intent")
def create_payment_intent(request: PaymentIntentRequest):
    try:
        logger.info("Received request to create payment intent with amount: %d and currency: %s", request.amount)
        
        payment_intent = stripe.PaymentIntent.create(
            amount=request.amount * 100,
            currency=request.currency
        )
        
        logger.info("Payment intent created successfully. Client secret: %s", payment_intent.client_secret)
        return {"client_secret": payment_intent.client_secret}
    except Exception as e:
        logger.error("Error creating payment intent: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))