from sqlalchemy import Column,String,Boolean,CheckConstraint,DateTime,JSON
from sqlalchemy.orm import relationship
from database.database import Base
import uuid
from datetime import datetime





class User(Base):
    __tablename__ = "users"
    
    id = Column(String(100), primary_key=True, default=str(uuid.uuid4()))
    f_name = Column(String(100), nullable=False)
    l_name = Column(String(100), nullable=False)
    e_mail = Column(String(200), nullable=False)
    password = Column(String(100), nullable=False)
    mo_number = Column(String(10), nullable=False)
    address=Column(String(200),nullable=False)
    pincode=Column(String(6),nullable=False)
    state=Column(String(100),nullable=False)
    city=Column(String(100),nullable=False)
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_verified = Column(Boolean, default=False)
   
    
    # Add a CHECK constraint for the mobile number length
    __table_args__ = (
        CheckConstraint('length(mo_number) = 10', name='check_mo_number_length'),
    )