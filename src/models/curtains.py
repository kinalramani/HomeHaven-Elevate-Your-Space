from sqlalchemy import Column,String,Boolean,DateTime,Text,ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime





class Curtains(Base):
    __tablename__ = "curtains"
    
    id = Column(String(100), primary_key=True, default=str(uuid.uuid4()))
    user_id= Column(String(100),ForeignKey('users.id'))
    category = Column(String(100), nullable=False)
    description=Column(Text)
    warranty_period = Column(String)
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_verified = Column(Boolean, default=False)