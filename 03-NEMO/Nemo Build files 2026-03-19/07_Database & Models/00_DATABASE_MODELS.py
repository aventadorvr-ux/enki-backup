# Database Models - SQLAlchemy
# Location: EC2 3.25.170.226:/home/ubuntu/nz-realestate-ai/app/db/models.py
# Status: DEFINED but TABLES NOT CREATED

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    email = Column(String(200))
    phone = Column(String(50))
    budget = Column(Float)
    timeline = Column(String(50))
    pre_approved = Column(Boolean, default=False)
    score = Column(Integer)
    qualified = Column(Boolean, default=False)
    status = Column(String(50), default="new")
    assigned_agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    assigned_agent = relationship("Agent")

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(500))
    suburb = Column(String(100))
    city = Column(String(100))
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    price = Column(Float)
    description = Column(Text)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    client_name = Column(String(200))
    client_email = Column(String(200))
    datetime = Column(DateTime)
    status = Column(String(50), default="confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    buyer_name = Column(String(200))
    seller_name = Column(String(200))
    sale_price = Column(Float)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    deadlines = relationship("Deadline", back_populates="transaction")

class Deadline(Base):
    __tablename__ = "deadlines"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    task = Column(String(500))
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    
    transaction = relationship("Transaction", back_populates="deadlines")

# Database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./nz_realestate.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

# ⚠️ MIGRATIONS NOT RUN - Database tables do not exist
# Run: alembic init alembic
# Run: alembic revision --autogenerate -m "Initial migration"
# Run: alembic upgrade head
