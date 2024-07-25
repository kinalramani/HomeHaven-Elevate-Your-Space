from sqlalchemy import Column,String,Boolean,DateTime,ForeignKey,Float,Date
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime





class Payment(Base):
    __tablename__ = "payment"
    
    id = Column(String(100), primary_key=True, default=str(uuid.uuid4()))
    user_id= Column(String(100),ForeignKey('users.id'))
    order_id=Column(String(100),ForeignKey('order.id'))
    payment_method = Column(String(20),nullable=False)
    payment_date = Column(Date, nullable=False)
    amount = Column(Float(10,3),nullable=False)
    status = Column(String, nullable=False, default="pending")
    transaction_id = Column(String(50), nullable=True)
    currency = Column(String(3), default='USD') 
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_verified = Column(Boolean, default=False)