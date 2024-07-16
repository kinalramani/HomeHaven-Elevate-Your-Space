from sqlalchemy import Column,String,Boolean,DateTime,ForeignKey,CheckConstraint
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime




class DeliveryBoy(Base):
    __tablename__ = "deliveryboy"
    
    id = Column(String(100), primary_key=True, default=str(uuid.uuid4()))
    delivery_id=Column(String(100),ForeignKey('deliveries.id'),nullable=False)
    name=Column(String(100),nullable=False)
    mo_number=Column(String(10),nullable=False)
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    

    # Add a CHECK constraint for the mobile number length
    __table_args__ = (
        CheckConstraint('length(mo_number) = 10', name='check_mo_number_length'),
    )