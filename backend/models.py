# from datetime import datetime, date
# from enum import Enum
# from typing import Optional
# from pydantic import BaseModel, EmailStr
# from sqlalchemy import Column, String, Float, DateTime, Date, Text, Integer, ForeignKey, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship

# Base = declarative_base()


# class RequestStatus(str, Enum):
#     PENDING_INFO = "pending_info"
#     PENDING_SELECTION = "pending_selection"
#     PROPOSAL_SENT = "proposal_sent"
#     ACCEPTED = "accepted"
#     INVOICED = "invoiced"
#     CANCELLED = "cancelled"


# # SQLAlchemy Model
# class RentalRequestDB(Base):
#     __tablename__ = "rental_requests"

#     id = Column(String, primary_key=True)
#     status = Column(String, default=RequestStatus.PENDING_INFO.value)

#     # Client info
#     client_name = Column(String, nullable=True)
#     client_email = Column(String, nullable=False)
#     client_vat = Column(String, nullable=True)
#     client_phone = Column(String, nullable=True)

#     # Rental details
#     pickup_date = Column(Date, nullable=True)
#     return_date = Column(Date, nullable=True)
#     pickup_location = Column(String, nullable=True)
#     return_location = Column(String, nullable=True)
#     vehicle_type = Column(String, nullable=True)
#     special_requests = Column(Text, nullable=True)

#     # Additional info fields (for missing info template)
#     driver_name = Column(String, nullable=True)
#     artist_project_event = Column(String, nullable=True)
#     destination_cities = Column(String, nullable=True)

#     # Staff selection
#     selected_partner_id = Column(String, ForeignKey("partners.id"), nullable=True)
#     selected_vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
#     selected_partner_name = Column(String, nullable=True)
#     selected_vehicle_description = Column(String, nullable=True)
#     cost_price = Column(Float, nullable=True)  # What IRWT pays to partner
#     price = Column(Float, nullable=True)  # What client pays (final price)

#     # Email tracking
#     original_email_id = Column(String, nullable=True)
#     original_email_subject = Column(String, nullable=True)
#     original_email_body = Column(Text, nullable=True)
#     thread_id = Column(String, nullable=True)

#     # Internal notes (staff use only)
#     internal_notes = Column(Text, nullable=True)

#     # Timestamps
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# class ProcessedEmailDB(Base):
#     """Track emails that have been processed (to avoid re-parsing)."""
#     __tablename__ = "processed_emails"

#     email_id = Column(String, primary_key=True)
#     processed_at = Column(DateTime, default=datetime.utcnow)


# # ============== Partner & Vehicle Models ==============

# class PartnerDB(Base):
#     """Rent-a-car partner company."""
#     __tablename__ = "partners"

#     id = Column(String, primary_key=True)
#     name = Column(String, nullable=False, unique=True)
#     contact_email = Column(String, nullable=True)
#     notes = Column(Text, nullable=True)
#     is_active = Column(Integer, default=1)  # SQLite doesn't have boolean
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relationships
#     vehicles = relationship("VehicleDB", back_populates="partner", cascade="all, delete-orphan")


# class VehicleDB(Base):
#     """Vehicle available from a partner."""
#     __tablename__ = "vehicles"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     partner_id = Column(String, ForeignKey("partners.id"), nullable=False)

#     # Vehicle identification
#     category = Column(String, nullable=False)  # e.g., "Ligeiros", "Comerciais", "Minibus"
#     group_code = Column(String, nullable=False)  # e.g., "A", "B", "AD", "AK"
#     description = Column(String, nullable=False)  # e.g., "Renault Clio / VW Polo"

#     # Pricing tiers (daily rates)
#     price_1_3_days = Column(Float, nullable=True)  # 1-3 days
#     price_4_6_days = Column(Float, nullable=True)  # 4-6 days
#     price_7_29_days = Column(Float, nullable=True)  # 7-29 days
#     price_monthly = Column(Float, nullable=True)  # Monthly rate

#     # Additional info
#     franchise = Column(Float, nullable=True)  # Franchise/excess amount in €
#     min_age = Column(Integer, nullable=True)
#     license_years = Column(Integer, nullable=True)
#     notes = Column(Text, nullable=True)

#     is_active = Column(Integer, default=1)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relationships
#     partner = relationship("PartnerDB", back_populates="vehicles")


# # Pydantic Models for API
# class RentalRequestCreate(BaseModel):
#     client_email: EmailStr
#     client_name: Optional[str] = None
#     client_vat: Optional[str] = None
#     client_phone: Optional[str] = None
#     pickup_date: Optional[date] = None
#     return_date: Optional[date] = None
#     pickup_location: Optional[str] = None
#     return_location: Optional[str] = None
#     vehicle_type: Optional[str] = None
#     special_requests: Optional[str] = None
#     driver_name: Optional[str] = None
#     artist_project_event: Optional[str] = None
#     destination_cities: Optional[str] = None
#     original_email_id: Optional[str] = None
#     original_email_subject: Optional[str] = None
#     original_email_body: Optional[str] = None


# class RentalRequest(BaseModel):
#     id: str
#     status: RequestStatus
#     client_name: Optional[str] = None
#     client_email: str
#     client_vat: Optional[str] = None
#     client_phone: Optional[str] = None
#     pickup_date: Optional[date] = None
#     return_date: Optional[date] = None
#     pickup_location: Optional[str] = None
#     return_location: Optional[str] = None
#     vehicle_type: Optional[str] = None
#     special_requests: Optional[str] = None
#     driver_name: Optional[str] = None
#     artist_project_event: Optional[str] = None
#     destination_cities: Optional[str] = None
#     selected_partner_id: Optional[str] = None
#     selected_vehicle_id: Optional[int] = None
#     selected_partner_name: Optional[str] = None
#     selected_vehicle_description: Optional[str] = None
#     cost_price: Optional[float] = None
#     price: Optional[float] = None
#     original_email_subject: Optional[str] = None
#     internal_notes: Optional[str] = None
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         from_attributes = True


# class NotesUpdate(BaseModel):
#     notes: str


# class PartnerSelection(BaseModel):
#     partner_id: str
#     vehicle_id: int
#     cost_price: float  # What IRWT pays to partner
#     price: float  # What client pays


# # ============== Partner & Vehicle Pydantic Schemas ==============

# class VehicleBase(BaseModel):
#     category: str
#     group_code: str
#     description: str
#     price_1_3_days: Optional[float] = None
#     price_4_6_days: Optional[float] = None
#     price_7_29_days: Optional[float] = None
#     price_monthly: Optional[float] = None
#     franchise: Optional[float] = None
#     min_age: Optional[int] = None
#     license_years: Optional[int] = None
#     notes: Optional[str] = None


# class VehicleCreate(VehicleBase):
#     partner_id: str


# class Vehicle(VehicleBase):
#     id: int
#     partner_id: str
#     is_active: bool
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         from_attributes = True


# class PartnerBase(BaseModel):
#     name: str
#     contact_email: Optional[str] = None
#     notes: Optional[str] = None


# class PartnerCreate(PartnerBase):
#     pass


# class Partner(PartnerBase):
#     id: str
#     is_active: bool
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         from_attributes = True


# class PartnerWithVehicles(Partner):
#     vehicles: list[Vehicle] = []

#     class Config:
#         from_attributes = True


# class VehicleWithPartner(Vehicle):
#     partner: Partner

#     class Config:
#         from_attributes = True


# # Database setup
# def get_engine(database_url: str):
#     return create_engine(database_url)


# def get_session_maker(engine):
#     return sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def init_db(engine):
#     Base.metadata.create_all(bind=engine)


from datetime import datetime, date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String, Float, DateTime, Date, Text, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class RequestStatus(str, Enum):
    PENDING_INFO = "pending_info"
    PENDING_SELECTION = "pending_selection"
    PROPOSAL_SENT = "proposal_sent"
    ACCEPTED = "accepted"
    INVOICED = "invoiced"
    CANCELLED = "cancelled"


# SQLAlchemy Model
class RentalRequestDB(Base):
    __tablename__ = "rental_requests"

    id = Column(String, primary_key=True)
    status = Column(String, default=RequestStatus.PENDING_INFO.value)

    # Client info
    client_name = Column(String, nullable=True)
    client_email = Column(String, nullable=False)
    client_vat = Column(String, nullable=True)
    client_phone = Column(String, nullable=True)

    # Rental details
    pickup_date = Column(Date, nullable=True)
    return_date = Column(Date, nullable=True)
    pickup_location = Column(String, nullable=True)
    return_location = Column(String, nullable=True)
    vehicle_type = Column(String, nullable=True)
    special_requests = Column(Text, nullable=True)

    # Additional info fields (for missing info template)
    driver_name = Column(String, nullable=True)
    artist_project_event = Column(String, nullable=True)
    destination_cities = Column(String, nullable=True)

    # Staff selection
    selected_partner_id = Column(String, ForeignKey("partners.id"), nullable=True)
    selected_vehicle_id = Column(String, ForeignKey("vehicles.id"), nullable=True)  # CHANGED: Integer → String
    selected_partner_name = Column(String, nullable=True)
    selected_vehicle_description = Column(String, nullable=True)
    cost_price = Column(Float, nullable=True)
    price = Column(Float, nullable=True)

    # Email tracking
    original_email_id = Column(String, nullable=True)
    original_email_subject = Column(String, nullable=True)
    original_email_body = Column(Text, nullable=True)
    thread_id = Column(String, nullable=True)

    # Internal notes (staff use only)
    internal_notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProcessedEmailDB(Base):
    __tablename__ = "processed_emails"

    email_id = Column(String, primary_key=True)
    processed_at = Column(DateTime, default=datetime.utcnow)


class PartnerDB(Base):
    __tablename__ = "partners"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    contact_email = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vehicles = relationship("VehicleDB", back_populates="partner", cascade="all, delete-orphan")


class VehicleDB(Base):
    __tablename__ = "vehicles"

    id = Column(String, primary_key=True)  # CHANGED: Integer autoincrement → String (Airtable ID)
    partner_id = Column(String, ForeignKey("partners.id"), nullable=False)

    category = Column(String, nullable=False)
    group_code = Column(String, nullable=False)
    description = Column(String, nullable=False)

    price_1_3_days = Column(Float, nullable=True)
    price_4_6_days = Column(Float, nullable=True)
    price_7_29_days = Column(Float, nullable=True)
    price_monthly = Column(Float, nullable=True)

    franchise = Column(Float, nullable=True)
    min_age = Column(Integer, nullable=True)
    license_years = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    partner = relationship("PartnerDB", back_populates="vehicles")


# ============== Pydantic Models ==============

class RentalRequestCreate(BaseModel):
    client_email: EmailStr
    client_name: Optional[str] = None
    client_vat: Optional[str] = None
    client_phone: Optional[str] = None
    pickup_date: Optional[date] = None
    return_date: Optional[date] = None
    pickup_location: Optional[str] = None
    return_location: Optional[str] = None
    vehicle_type: Optional[str] = None
    special_requests: Optional[str] = None
    driver_name: Optional[str] = None
    artist_project_event: Optional[str] = None
    destination_cities: Optional[str] = None
    original_email_id: Optional[str] = None
    original_email_subject: Optional[str] = None
    original_email_body: Optional[str] = None


class RentalRequest(BaseModel):
    id: str
    status: RequestStatus
    client_name: Optional[str] = None
    client_email: str
    client_vat: Optional[str] = None
    client_phone: Optional[str] = None
    pickup_date: Optional[date] = None
    return_date: Optional[date] = None
    pickup_location: Optional[str] = None
    return_location: Optional[str] = None
    vehicle_type: Optional[str] = None
    special_requests: Optional[str] = None
    driver_name: Optional[str] = None
    artist_project_event: Optional[str] = None
    destination_cities: Optional[str] = None
    selected_partner_id: Optional[str] = None
    selected_vehicle_id: Optional[str] = None  # CHANGED: int → str
    selected_partner_name: Optional[str] = None
    selected_vehicle_description: Optional[str] = None
    cost_price: Optional[float] = None
    price: Optional[float] = None
    original_email_subject: Optional[str] = None
    internal_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotesUpdate(BaseModel):
    notes: str


class PartnerSelection(BaseModel):
    partner_id: str
    vehicle_id: str   # CHANGED: int → str
    cost_price: float
    price: float


class VehicleBase(BaseModel):
    category: str
    group_code: str
    description: str
    price_1_3_days: Optional[float] = None
    price_4_6_days: Optional[float] = None
    price_7_29_days: Optional[float] = None
    price_monthly: Optional[float] = None
    franchise: Optional[float] = None
    min_age: Optional[int] = None
    license_years: Optional[int] = None
    notes: Optional[str] = None


class VehicleCreate(VehicleBase):
    id: str          # CHANGED: now required, caller supplies the Airtable ID
    partner_id: str


class Vehicle(VehicleBase):
    id: str          # CHANGED: int → str
    partner_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PartnerBase(BaseModel):
    name: str
    contact_email: Optional[str] = None
    notes: Optional[str] = None


class PartnerCreate(PartnerBase):
    pass


class Partner(PartnerBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PartnerWithVehicles(Partner):
    vehicles: list[Vehicle] = []

    class Config:
        from_attributes = True


class VehicleWithPartner(Vehicle):
    partner: Partner

    class Config:
        from_attributes = True


# Database setup
def get_engine(database_url: str):
    return create_engine(database_url)


def get_session_maker(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(engine):
    Base.metadata.create_all(bind=engine)