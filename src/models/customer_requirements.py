from sqlalchemy import Column,String,Boolean,DateTime,ForeignKey,Text
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime





class CustomerRequirements(Base):
    __tablename__ = "customerrequirements"
    
    id = Column(String(100), primary_key=True, default=str(uuid.uuid4()))
    description=Column(String(500),nullable=False)
    Customer_id=Column(String(100),ForeignKey('users.id'),nullable=False)
    product_name=Column(String(100),nullable=False)
    additional_notes=Column(Text)
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_verified = Column(Boolean, default=False)