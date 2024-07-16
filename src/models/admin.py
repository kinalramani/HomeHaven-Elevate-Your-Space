from sqlalchemy import Column,String,Boolean,DateTime
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime




class Admin(Base):
    __tablename__ = "admin"
    
    id = Column(String(100), primary_key=True, default=str(uuid.uuid4()))
    u_name=Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
   

    