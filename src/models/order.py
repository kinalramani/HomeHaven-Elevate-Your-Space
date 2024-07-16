from sqlalchemy import Column,String,Boolean,DateTime,ForeignKey,Float
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime




class Order(Base):
    __tablename__ = "order"
    
    id = Column(String(100), primary_key=True, default=str(uuid.uuid4()))
    req_id=Column(String(100),ForeignKey('customerrequirements.id'),nullable=False)
    user_id=Column(String(100),ForeignKey('users.id'),nullable=False)
    description=Column(String(500),nullable=False)
    product_id=Column(String(200),nullable=False)
    notes = Column(String(200), default="")
    price = Column(Float(10, 2), nullable=False)
    status=Column(String(200),nullable=False )
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)



    