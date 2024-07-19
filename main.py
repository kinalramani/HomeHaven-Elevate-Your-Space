from fastapi import FastAPI
from src.routers.user import userauth
from src.routers.user import Otp_router
from src.routers.admin import adminauth
from src.routers.sofa import sofaauth
from src.routers.curtains import curtainauth
from src.routers.customer_requirementes import custreqauth
from src.routers.mattresses import mattressauth
from src.routers.order import orderauth
from src.routers.delivery import deliveryauth
from src.routers.delivery_boy import deliveryboyauth
from src.routers.payment import paymentauth



app=FastAPI()


app.include_router(userauth)
app.include_router(Otp_router)
app.include_router(adminauth)
app.include_router(sofaauth)
app.include_router(curtainauth)
app.include_router(custreqauth)
app.include_router(mattressauth)
app.include_router(orderauth)
app.include_router(deliveryauth)
app.include_router(deliveryboyauth)
app.include_router(paymentauth)
