# """API routes for the van rental automation."""

# import os
# import uuid
# from datetime import datetime
# from typing import Optional
# from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
# from sqlalchemy.orm import Session

# from models import (
#     RentalRequest,
#     RentalRequestCreate,
#     RentalRequestDB,
#     RequestStatus,
#     PartnerSelection,
#     NotesUpdate,
#     ProcessedEmailDB,
#     # Partner & Vehicle models
#     PartnerDB,
#     VehicleDB,
#     Partner,
#     PartnerCreate,
#     Vehicle,
#     VehicleWithPartner,
#     VehicleCreate,
# )
# from pydantic import BaseModel
# from fastapi import Response
# from pydantic import BaseModel
# from config import get_settings, Settings
# from services import GmailService, SheetsService
# from agents import EmailParserAgent, ProposalGenerator
# from agents.email_templates import (
#     generate_partner_request_html,
#     generate_partner_request_plain_text,
#     PARTNER_REQUEST_SUBJECT,
# )
# from airtable import Airtable
# from pyairtable import Table


# router = APIRouter()


# # Airtable config
# BASE_ID = os.getenv("AIRTABLE_BASE_ID")
# TABLE_ID = os.getenv("AIRTABLE_TABLE_NAME")
# API_KEY = os.getenv("AIRTABLE_TOKEN")

# if not API_KEY:
#     raise ValueError("AIRTABLE_API_KEY not set in environment")

# airtable = Airtable(BASE_ID, TABLE_ID, api_key=API_KEY)

# # Dependency to get database session
# def get_db():
#     from main import SessionLocal
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# def get_gmail_service(settings: Settings = Depends(get_settings)) -> GmailService:
#     return GmailService(settings.gmail_address, settings.gmail_app_password)


# def get_sheets_service(settings: Settings = Depends(get_settings)) -> Optional[SheetsService]:
#     if settings.google_sheets_id and settings.google_service_account_json:
#         return SheetsService(settings.google_sheets_id, settings.google_service_account_json)
#     return None


# def get_email_parser(settings: Settings = Depends(get_settings)) -> EmailParserAgent:
#     return EmailParserAgent(settings.openai_api_key)


# def get_proposal_generator(settings: Settings = Depends(get_settings)) -> ProposalGenerator:
#     return ProposalGenerator(settings.openai_api_key)


# # ============== Request Endpoints ==============

# @router.get("/requests", response_model=list[RentalRequest])
# def list_requests(
#     status: Optional[RequestStatus] = None,
#     db: Session = Depends(get_db),
# ):
#     """List all rental requests, optionally filtered by status."""
#     query = db.query(RentalRequestDB)

#     if status:
#         query = query.filter(RentalRequestDB.status == status.value)

#     requests = query.order_by(RentalRequestDB.created_at.desc()).all()
#     return [RentalRequest.model_validate(r) for r in requests]


# @router.get("/requests/{request_id}", response_model=RentalRequest)
# def get_request(request_id: str, db: Session = Depends(get_db)):
#     """Get a specific rental request."""
#     request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
#     if not request:
#         raise HTTPException(status_code=404, detail="Request not found")
#     return RentalRequest.model_validate(request)


# @router.post("/requests/{request_id}/select-partner")
# def select_partner(
#     request_id: str,
#     selection: PartnerSelection,
#     db: Session = Depends(get_db),
# ):
#     """Staff selects a rent-a-car partner and vehicle for a request."""
#     request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
#     if not request:
#         raise HTTPException(status_code=404, detail="Request not found")

#     # Always use Airtable partner ID by looking up the partner name in Airtable
#     # First, get the partner name from the local DB (for backward compatibility)
#     partner = db.query(PartnerDB).filter(PartnerDB.id == selection.partner_id).first()
#     partner_name = partner.name if partner else None
#     airtable_partner_id = None
#     if partner_name:
#         # Look up Airtable partner ID by name
#         fornecedores_table = Table(
#             os.getenv("AIRTABLE_TOKEN"),
#             os.getenv("AIRTABLE_BASE_ID"),
#             "tblnSH6ba9irqfB4h"
#         )
#         records = fornecedores_table.all()
#         for rec in records:
#             fields = rec.get('fields', {})
#             full_label = fields.get('Preços dos fornecedores', "")
#             if full_label and full_label.split("—")[0].strip() == partner_name:
#                 airtable_partner_id = rec['id']
#                 break
#     # Fallback: if not found, use the provided ID (may already be Airtable ID)
#     if not airtable_partner_id:
#         airtable_partner_id = selection.partner_id

#     # Get vehicle from database (must match new partner_id)
#     vehicle = db.query(VehicleDB).filter(
#         VehicleDB.id == selection.vehicle_id,
#         VehicleDB.partner_id == airtable_partner_id
#     ).first()
#     if not vehicle:
#         raise HTTPException(status_code=400, detail="Invalid vehicle ID or vehicle doesn't belong to selected partner")

#     request.selected_partner_id = airtable_partner_id
#     request.selected_vehicle_id = selection.vehicle_id
#     request.selected_partner_name = partner_name or "Unknown"
#     request.selected_vehicle_description = f"{vehicle.group_code} - {vehicle.description}"
#     request.cost_price = selection.cost_price
#     request.price = selection.price
#     request.updated_at = datetime.utcnow()

#     db.commit()
#     db.refresh(request)

#     return {
#         "status": "success",
#         "message": f"Partner {partner_name or airtable_partner_id} selected with vehicle {vehicle.description} - Cost: €{selection.cost_price}, Client: €{selection.price}"
#     }


# @router.post("/requests/{request_id}/send-partner-request")
# async def send_partner_request(
#     request_id: str,
#     db: Session = Depends(get_db),
#     gmail: GmailService = Depends(get_gmail_service),
# ):
#     """Send a confirmation request email to the selected rent-a-car partner."""
#     request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
#     if not request:
#         raise HTTPException(status_code=404, detail="Request not found")

#     if not request.selected_partner_id:
#         raise HTTPException(status_code=400, detail="Partner must be selected first")

#     # Get partner info
#     partner = db.query(PartnerDB).filter(PartnerDB.id == request.selected_partner_id).first()
#     if not partner:
#         raise HTTPException(status_code=400, detail="Selected partner not found")

#     if not partner.contact_email:
#         raise HTTPException(status_code=400, detail="Partner has no contact email configured")

#     # Format dates with times
#     pickup_datetime = request.pickup_date.strftime("%d/%m/%Y") if request.pickup_date else "A confirmar"
#     return_datetime = request.return_date.strftime("%d/%m/%Y") if request.return_date else "A confirmar"

#     # Generate emails
#     html_body = generate_partner_request_html(
#         vehicle_type=request.selected_vehicle_description or request.vehicle_type or "A confirmar",
#         pickup_location=request.pickup_location or "A confirmar",
#         return_location=request.return_location or request.pickup_location or "A confirmar",
#         pickup_datetime=pickup_datetime,
#         return_datetime=return_datetime,
#         driver_name=request.client_name or "A confirmar",
#         destination_cities=None,  # Optional
#     )

#     plain_text = generate_partner_request_plain_text(
#         vehicle_type=request.selected_vehicle_description or request.vehicle_type or "A confirmar",
#         pickup_location=request.pickup_location or "A confirmar",
#         return_location=request.return_location or request.pickup_location or "A confirmar",
#         pickup_datetime=pickup_datetime,
#         return_datetime=return_datetime,
#         driver_name=request.client_name or "A confirmar",
#         destination_cities=None,
#     )

#     # Send to partner
#     success = gmail.send_email(
#         to_address=partner.contact_email,
#         subject=PARTNER_REQUEST_SUBJECT,
#         body_text=plain_text,
#         body_html=html_body,
#     )

#     if not success:
#         raise HTTPException(status_code=500, detail="Failed to send email to partner")

#     return {
#         "status": "success",
#         "message": f"Confirmation request sent to {partner.name} ({partner.contact_email})"
#     }


# @router.post("/requests/{request_id}/send-proposal")
# async def send_proposal(
#     request_id: str,
#     background_tasks: BackgroundTasks,
#     db: Session = Depends(get_db),
#     gmail: GmailService = Depends(get_gmail_service),
#     proposal_gen: ProposalGenerator = Depends(get_proposal_generator),
#     sheets: Optional[SheetsService] = Depends(get_sheets_service),
#     settings: Settings = Depends(get_settings),
# ):
#     """Send a rental proposal to the client."""
#     request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
#     if not request:
#         raise HTTPException(status_code=404, detail="Request not found")

#     if not request.selected_partner_id or not request.price:
#         raise HTTPException(status_code=400, detail="Partner and price must be selected first")

#     if not request.pickup_date or not request.return_date:
#         raise HTTPException(status_code=400, detail="Pickup and return dates are required")

#     # Generate proposal email
#     # Use selected vehicle description if available, otherwise fall back to client's request
#     vehicle_info = request.selected_vehicle_description or request.vehicle_type or "van"

#     plain_text, html = proposal_gen.generate_proposal(
#         client_name=request.client_name or "Valued Customer",
#         client_email=request.client_email,
#         pickup_date=request.pickup_date,
#         return_date=request.return_date,
#         pickup_location=request.pickup_location or "TBD",
#         return_location=request.return_location or request.pickup_location or "TBD",
#         vehicle_type=vehicle_info,
#         partner_name=request.selected_partner_name or "Partner",
#         price=request.price,
#         special_requests=request.special_requests,
#     )

#     # Send email as reply to original thread
#     # Use original subject with Re: prefix for proper threading
#     original_subject = request.original_email_subject or f"Van Rental - {request.pickup_location}"
#     if not original_subject.lower().startswith("re:"):
#         subject = f"Re: {original_subject}"
#     else:
#         subject = original_subject

#     success = gmail.send_email(
#         to_address=request.client_email,
#         subject=subject,
#         body_text=plain_text,
#         body_html=html,
#         reply_to_message_id=request.original_email_id,
#     )

#     if not success:
#         raise HTTPException(status_code=500, detail="Failed to send email")

#     # Update status
#     request.status = RequestStatus.PROPOSAL_SENT.value
#     request.updated_at = datetime.now()
#     db.commit()

#     # Update Google Sheet in background
#     if sheets:
#         background_tasks.add_task(
#             sheets.update_request_status,
#             request_id,
#             RequestStatus.PROPOSAL_SENT.value,
#             request.selected_partner_name,
#             request.price,
#         )

#     return {"status": "success", "message": "Proposal sent to client"}


# @router.post("/requests/{request_id}/confirm")
# async def confirm_booking(
#     request_id: str,
#     background_tasks: BackgroundTasks,
#     db: Session = Depends(get_db),
#     gmail: GmailService = Depends(get_gmail_service),
#     proposal_gen: ProposalGenerator = Depends(get_proposal_generator),
#     sheets: Optional[SheetsService] = Depends(get_sheets_service),
#     settings: Settings = Depends(get_settings),
# ):
#     """Confirm a booking after client acceptance."""
#     request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
#     if not request:
#         raise HTTPException(status_code=404, detail="Request not found")

#     if request.status != RequestStatus.ACCEPTED.value:
#         raise HTTPException(status_code=400, detail="Request must be in accepted status")

#     request.status = RequestStatus.INVOICED.value
#     request.updated_at = datetime.utcnow()
#     db.commit()

#     # Send confirmation email
#     # Use selected vehicle description if available
#     vehicle_info = request.selected_vehicle_description or request.vehicle_type or "van"

#     plain_text, html = proposal_gen.generate_confirmation_email(
#         client_name=request.client_name or "Valued Customer",
#         pickup_date=request.pickup_date,
#         return_date=request.return_date,
#         pickup_location=request.pickup_location or "TBD",
#         return_location=request.return_location or request.pickup_location or "TBD",
#         vehicle_type=vehicle_info,
#         partner_name=request.selected_partner_name or "Partner",
#         price=request.price,
#         invoice_number=None,
#     )

#     subject = f"Reserva Confirmada - IRWT {request.pickup_date}"
#     gmail.send_email(
#         to_address=request.client_email,
#         subject=subject,
#         body_text=plain_text,
#         body_html=html,
#     )

#     # Update Google Sheet in background
#     if sheets:
#         background_tasks.add_task(
#             sheets.update_request_status,
#             request_id,
#             RequestStatus.INVOICED.value,
#         )

#     return {
#         "status": "success",
#         "message": "Booking confirmed",
#     }


# @router.post("/requests/{request_id}/mark-accepted")
# def mark_accepted(request_id: str, db: Session = Depends(get_db)):
#     """Manually mark a request as accepted (after client accepts via email)."""
#     request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
#     if not request:
#         raise HTTPException(status_code=404, detail="Request not found")

#     request.status = RequestStatus.ACCEPTED.value
#     request.updated_at = datetime.utcnow()
#     db.commit()

#     return {"status": "success", "message": "Request marked as accepted"}


# @router.put("/requests/{request_id}/notes")
# def update_notes(request_id: str, notes_update: NotesUpdate, db: Session = Depends(get_db)):
#     """Update internal notes for a request."""
#     request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
#     if not request:
#         raise HTTPException(status_code=404, detail="Request not found")

#     request.internal_notes = notes_update.notes
#     request.updated_at = datetime.utcnow()
#     db.commit()

#     return {"status": "success", "message": "Notes updated"}


# # ============== Partner Endpoints ==============

# @router.get("/partners", response_model=list[Partner])
# def list_partners(db: Session = Depends(get_db)):
#     """List all rent-a-car partners, sorted by cheapest vehicle price."""
#     from sqlalchemy import func

#     # Get all active partners with their minimum vehicle price
#     partners = db.query(PartnerDB).filter(PartnerDB.is_active == 1).all()

#     # Calculate min price for each partner and sort
#     partners_with_min_price = []
#     for partner in partners:
#         # Get minimum price from all vehicles of this partner
#         min_price = db.query(func.min(VehicleDB.price_1_3_days)).filter(
#             VehicleDB.partner_id == partner.id,
#             VehicleDB.is_active == 1
#         ).scalar()
#         partners_with_min_price.append((partner, min_price or float('inf')))

#     # Sort by minimum price (cheapest first)
#     partners_with_min_price.sort(key=lambda x: x[1])

#     return [Partner.model_validate(p[0]) for p in partners_with_min_price]


# class AirtableVehicle(BaseModel):
#     id: str
#     group_code: str | None = None
#     description: str | None = None
#     category: str | None = None
#     price_1_3_days: float | None = None
#     is_active: bool = True
#     created_at: str | None = None
#     updated_at: str | None = None

# class AirtablePartnerWithVehicles(BaseModel):
#     id: str
#     name: str | None = None
#     contact_email: str | None = None
#     notes: str | None = None
#     is_active: bool = True
#     created_at: str | None = None
#     updated_at: str | None = None
#     vehicles: list[AirtableVehicle]

# @router.get("/partners/{partner_id}", response_model=AirtablePartnerWithVehicles)
# def get_partner(partner_id: str):
#     """Get a specific partner with all their vehicles from Airtable."""
#     from pydantic import ValidationError
#     # Fetch supplier (partner) from Airtable
#     fornecedores_table = Table(
#         os.getenv("AIRTABLE_TOKEN"),
#         os.getenv("AIRTABLE_BASE_ID"),
#         "tblnSH6ba9irqfB4h"  # Preços dos fornecedores
#     )
#     categorias_table = Table(
#         os.getenv("AIRTABLE_TOKEN"),
#         os.getenv("AIRTABLE_BASE_ID"),
#         "tblXEy4NCNVhO8eX2"  # Categorias de veículos
#     )

#     # Batch fetch all price records from Airtable and build a lookup dict
#     category_records = categorias_table.all()
#     price_records = fornecedores_table.all()
#     price_lookup = {rec['id']: rec for rec in price_records}

#     vehicles = []
#     for rec in category_records:
#         fields = rec.get('fields', {})
#         preco_ids = fields.get('Preços dos fornecedores', [])
#         found_for_supplier = False
#         for preco_id in preco_ids:
#             preco_rec = price_lookup.get(preco_id)
#             if not preco_rec:
#                 continue
#             preco_fields = preco_rec.get('fields', {})
#             fornecedores = preco_fields.get('Fornecedor', [])
#             if partner_id in fornecedores:
#                 found_for_supplier = True
#                 break
#         if found_for_supplier:
#             vehicles.append({
#                 'id': rec['id'],
#                 'group_code': fields.get('Códigos SIPP') or fields.get('Group Code') or fields.get('Grupo'),
#                 'description': fields.get('Modelos de exemplo') or fields.get('Description') or fields.get('Descrição'),
#                 'category': fields.get('Categoria'),
#                 'price_1_3_days': None,  # Not available at this level
#                 'is_active': True,
#                 'created_at': rec.get('createdTime'),
#                 'updated_at': None,
#             })

#     # Try to get partner name from the first matching vehicle's price record
#     partner_name = None
#     contact_email = None
#     notes = None
#     is_active = True
#     created_at = None
#     updated_at = None
#     # Find a price record for this partner to get name/email
#     for preco_rec in price_records:
#         preco_fields = preco_rec.get('fields', {})
#         fornecedores = preco_fields.get('Fornecedor', [])
#         if partner_id in fornecedores:
#             # Try to extract name/email/notes if available
#             full_label = preco_fields.get('Preços dos fornecedores', "")
#             if full_label:
#                 partner_name = full_label.split("—")[0].strip()
#             # Email/notes not available in this schema, unless you have a custom field
#             created_at = preco_rec.get('createdTime')
#             break

#     if not partner_name:
#         raise HTTPException(status_code=404, detail="Partner not found in Airtable")

#     # Compose PartnerWithVehicles response
#     from pydantic import parse_obj_as
#     try:
#         return AirtablePartnerWithVehicles(
#             id=partner_id,
#             name=partner_name,
#             contact_email=contact_email,
#             notes=notes,
#             is_active=is_active,
#             created_at=created_at,
#             updated_at=updated_at,
#             vehicles=[
#                 AirtableVehicle(
#                     id=v['id'],
#                     group_code=v['group_code'],
#                     description=v['description'],
#                     category=v['category'],
#                     price_1_3_days=v['price_1_3_days'],
#                     is_active=v['is_active'],
#                     created_at=v['created_at'],
#                     updated_at=v['updated_at'] if v['updated_at'] else v['created_at'],
#                 ) for v in vehicles
#             ]
#         )
#     except ValidationError as e:
#         raise HTTPException(status_code=500, detail=f"Airtable data error: {e}")


# @router.put("/partners/{partner_id}/notes")
# def update_partner_notes(partner_id: str, notes_update: NotesUpdate, db: Session = Depends(get_db)):
#     """Update internal notes for a partner."""
#     partner = db.query(PartnerDB).filter(PartnerDB.id == partner_id).first()
#     if not partner:
#         raise HTTPException(status_code=404, detail="Partner not found")

#     partner.notes = notes_update.notes
#     partner.updated_at = datetime.utcnow()
#     db.commit()

#     return {"status": "success", "message": "Partner notes updated"}



# # Airtable Vehicle model for API response



# # Table IDs for Airtable
# CATEGORIAS_VEICULOS_TABLE_ID = "tblXEy4NCNVhO8eX2"  # Categorias de veículos
# PRECOS_FORNECEDORES_TABLE_ID = "tblnSH6ba9irqfB4h"  # Preços dos fornecedores

# # --- Airtable Pydantic Models ---
# from pydantic import BaseModel



# class AirtablePartnerWithVehicles(BaseModel):
#     id: str
#     name: str | None = None
#     contact_email: str | None = None
#     notes: str | None = None
#     is_active: bool = True
#     created_at: str | None = None
#     updated_at: str | None = None
#     vehicles: list[AirtableVehicle]


# @router.get("/partners/{partner_id}/vehicles", response_model=list[AirtableVehicle])
# def list_partner_vehicles(
#     partner_id: str,  # Airtable supplier record ID
#     category: Optional[str] = None
# ):
#     """List all vehicle categories for a specific supplier (partner) from Airtable."""
#     categorias_table = Table(
#         os.getenv("AIRTABLE_TOKEN"),
#         os.getenv("AIRTABLE_BASE_ID"),
#         CATEGORIAS_VEICULOS_TABLE_ID
#     )
#     precos_fornecedores_table = Table(
#         os.getenv("AIRTABLE_TOKEN"),
#         os.getenv("AIRTABLE_BASE_ID"),
#         PRECOS_FORNECEDORES_TABLE_ID
#     )

#     # Fetch all vehicle categories
#     category_records = categorias_table.all()
#     vehicles = []
#     for rec in category_records:
#         fields = rec.get('fields', {})
#         if category and fields.get('Categoria') != category:
#             continue
#         preco_ids = fields.get('Preços dos fornecedores', [])
#         found_for_supplier = False
#         for preco_id in preco_ids:
#             preco_rec = precos_fornecedores_table.get(preco_id)
#             preco_fields = preco_rec.get('fields', {})
#             fornecedores = preco_fields.get('Fornecedor', [])
#             if partner_id in fornecedores:
#                 found_for_supplier = True
#                 break
#         if found_for_supplier:
#             vehicles.append(AirtableVehicle(
#                 id=rec['id'],
#                 group_code=fields.get('Códigos SIPP') or fields.get('Group Code') or fields.get('Grupo'),
#                 description=fields.get('Modelos de exemplo') or fields.get('Description') or fields.get('Descrição'),
#                 category=fields.get('Categoria'),
#                 price_1_3_days=None,  # Not available at this level, could be fetched from preco_fields if needed
#                 is_active=True,
#                 created_at=rec.get('createdTime'),
#                 updated_at=None,
#             ))
#     return vehicles


# @router.get("/partners/{partner_id}/categories")
# def list_partner_categories(partner_id: str, db: Session = Depends(get_db)):
#     """List all vehicle categories for a specific partner."""
#     partner = db.query(PartnerDB).filter(PartnerDB.id == partner_id).first()
#     if not partner:
#         raise HTTPException(status_code=404, detail="Partner not found")

#     categories = db.query(VehicleDB.category).filter(
#         VehicleDB.partner_id == partner_id,
#         VehicleDB.is_active == 1
#     ).distinct().all()

#     return [c[0] for c in categories]


# # ============== Vehicle Endpoints ==============

# @router.get("/vehicles", response_model=list[VehicleWithPartner])
# def list_all_vehicles(
#     category: Optional[str] = None,
#     partner_id: Optional[str] = None,
#     db: Session = Depends(get_db)
# ):
#     """List all vehicles across all partners with optional filters."""
#     query = db.query(VehicleDB).filter(VehicleDB.is_active == 1)

#     if category:
#         query = query.filter(VehicleDB.category == category)
#     if partner_id:
#         query = query.filter(VehicleDB.partner_id == partner_id)

#     vehicles = query.order_by(VehicleDB.partner_id, VehicleDB.category, VehicleDB.group_code).all()
#     return [VehicleWithPartner.model_validate(v) for v in vehicles]


# @router.get("/vehicles/{vehicle_id}", response_model=VehicleWithPartner)
# def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
#     """Get a specific vehicle with its partner info."""
#     vehicle = db.query(VehicleDB).filter(VehicleDB.id == vehicle_id).first()
#     if not vehicle:
#         raise HTTPException(status_code=404, detail="Vehicle not found")
#     return VehicleWithPartner.model_validate(vehicle)


# @router.get("/categories")
# def list_all_categories(db: Session = Depends(get_db)):
#     """List all unique vehicle categories across all partners."""
#     records = airtable.get_all(max_records=None)
    
#     # Extract and deduplicate categorias
#     categorias_set = set()
#     for record in records:
#         categoria = record.get('fields', {}).get('Categoria')
#         if categoria:  # Skip empty values
#             categorias_set.add(categoria)
    
#     categorias_list = sorted(list(categorias_set))
#     print(records)
#     return categorias_list
#     # categories = db.query(VehicleDB.category).filter(
#     #     VehicleDB.is_active == 1
#     # ).distinct().order_by(VehicleDB.category).all()
#     # return [c[0] for c in categories]


# class AirtableSupplier(BaseModel):
#     id: str
#     name: str | None = None
#     contact_email: str | None = None
#     notes: str | None = None
#     is_active: bool = True
#     created_at: str | None = None
#     updated_at: str | None = None

# @router.get("/categories/{category}/partners", response_model=list[AirtableSupplier])
# def list_partners_by_category(category: str):
#     """List partners (suppliers) from Airtable for the given category."""
#     categorias_table = Table(
#         os.getenv("AIRTABLE_TOKEN"),
#         os.getenv("AIRTABLE_BASE_ID"),
#         "tblXEy4NCNVhO8eX2"
#     )
#     fornecedores_table = Table(
#         os.getenv("AIRTABLE_TOKEN"),
#         os.getenv("AIRTABLE_BASE_ID"),
#         "tblnSH6ba9irqfB4h"
#     )

#     # Fetch all categories from Airtable
#     category_records = categorias_table.all()
#     categories = {rec['fields'].get('Categoria', '').strip(): rec['id'] for rec in category_records if rec['fields'].get('Categoria')}

#     normalized = category.strip().lower()
#     matched = {}
#     # Try exact match first
#     for name, rec_id in categories.items():
#         if name.lower() == normalized:
#             matched[name] = rec_id
#     # If no exact match, try prefix match (singular/plural)
#     if not matched:
#         if normalized.endswith('s'):
#             singular = normalized[:-1]
#             matched = {name: rec_id for name, rec_id in categories.items() if name.lower().startswith(singular)}
#         else:
#             matched = {name: rec_id for name, rec_id in categories.items() if name.lower().startswith(normalized)}

#     if not matched:
#         raise HTTPException(status_code=404, detail=f"No categories found matching '{category}'. Available: {list(categories.keys())}")

#     # Fetch and deduplicate suppliers across all matched categories
#     seen = set()
#     suppliers = []

#     for cat_name, category_id in matched.items():
#         cat_record = next((rec for rec in category_records if rec['id'] == category_id), None)
#         if not cat_record:
#             continue
#         supplier_price_ids = cat_record['fields'].get('Preços dos fornecedores', [])
#         if not supplier_price_ids:
#             continue
#         for price_id in supplier_price_ids:
#             record = fornecedores_table.get(price_id)
#             fields = record["fields"]
#             supplier_ids = fields.get("Fornecedor", [])
#             full_label = fields.get("Preços dos fornecedores", "")
#             supplier_name = full_label.split("—")[0].strip() if full_label else None

#             for supplier_id in supplier_ids:
#                 if supplier_id not in seen:
#                     seen.add(supplier_id)
#                     suppliers.append(AirtableSupplier(
#                         id=supplier_id,
#                         name=supplier_name,
#                         contact_email=None,
#                         notes=None,
#                         is_active=True,
#                         created_at=record["createdTime"],
#                         updated_at=None,
#                     ))

#     return suppliers
#     # from sqlalchemy import func

#     # # Get partners that have vehicles in this category
#     # partner_ids = db.query(VehicleDB.partner_id).filter(
#     #     VehicleDB.category == category,
#     #     VehicleDB.is_active == 1
#     # ).distinct().all()
#     # partner_ids = [p[0] for p in partner_ids]

#     # if not partner_ids:
#     #     return []

#     # # Get partners with their minimum price in this category
#     # partners_with_price = []
#     # for partner_id in partner_ids:
#     #     partner = db.query(PartnerDB).filter(
#     #         PartnerDB.id == partner_id,
#     #         PartnerDB.is_active == 1
#     #     ).first()
#     #     if partner:
#     #         min_price = db.query(func.min(VehicleDB.price_1_3_days)).filter(
#     #             VehicleDB.partner_id == partner_id,
#     #             VehicleDB.category == category,
#     #             VehicleDB.is_active == 1
#     #         ).scalar()
#     #         partners_with_price.append((partner, min_price or float('inf')))

#     # # Sort by minimum price (cheapest first)
#     # partners_with_price.sort(key=lambda x: x[1])

#     # return [Partner.model_validate(p[0]) for p in partners_with_price]


# # ============== Email Processing ==============

# @router.post("/process-emails")
# async def process_emails(
#     background_tasks: BackgroundTasks,
#     db: Session = Depends(get_db),
#     gmail: GmailService = Depends(get_gmail_service),
#     parser: EmailParserAgent = Depends(get_email_parser),
#     sheets: Optional[SheetsService] = Depends(get_sheets_service),
#     settings: Settings = Depends(get_settings),
# ):
#     """Process unread emails and create rental requests."""
#     print("📧 Processing emails...")

#     emails = gmail.fetch_unread_emails(mark_as_read=False)
#     print(f"Found {len(emails)} unread emails")

#     processed = []
#     for email in emails:
#         # Skip emails from ourselves
#         if email.from_address == settings.gmail_address:
#             continue

#         # Check if already processed
#         already_processed = db.query(ProcessedEmailDB).filter(
#             ProcessedEmailDB.email_id == email.id
#         ).first()
#         if already_processed:
#             continue

#         # Check if this is a reply (subject starts with Re:)
#         is_reply = email.subject.lower().startswith("re:")
#         email_body_for_ai = email.body

#         if is_reply:
#             print(f"📩 Reply detected: {email.subject[:40]}...")
#             print(f"  → From: {email.from_address}")

#             # First, check if this is an acceptance of a proposal
#             # Find if there's an existing request from this client with status PROPOSAL_SENT
#             existing_request = db.query(RentalRequestDB).filter(
#                 RentalRequestDB.client_email == email.from_address,
#                 RentalRequestDB.status == RequestStatus.PROPOSAL_SENT.value
#             ).first()

#             if existing_request:
#                 print(f"  → Found existing request {existing_request.id[:8]} with PROPOSAL_SENT status")
#                 # Check if this reply is an acceptance
#                 acceptance_result = parser.detect_acceptance(email.body, email.subject)
#                 print(f"  → Acceptance check: is_acceptance={acceptance_result.is_acceptance}, confidence={acceptance_result.confidence}")

#                 if acceptance_result.is_acceptance and acceptance_result.confidence > 0.7:
#                     print(f"  ✅ Proposal ACCEPTED by {email.from_address}")

#                     # Update request status
#                     existing_request.status = RequestStatus.ACCEPTED.value
#                     existing_request.updated_at = datetime.now()
#                     db.commit()

#                     # Track email as processed
#                     db.add(ProcessedEmailDB(email_id=email.id))
#                     db.commit()

#                     # Mark email as read
#                     gmail.mark_as_read(email.id)

#                     # Update Google Sheet
#                     if sheets:
#                         background_tasks.add_task(
#                             sheets.update_request_status,
#                             existing_request.id,
#                             RequestStatus.ACCEPTED.value,
#                         )

#                     processed.append({
#                         "id": existing_request.id,
#                         "client": email.from_address,
#                         "status": "accepted",
#                         "action": "proposal_accepted",
#                     })
#                     continue

#             if not existing_request:
#                 print(f"  → No existing PROPOSAL_SENT request found for {email.from_address}")

#             # Not an acceptance, fetch full thread for context
#             thread_emails = gmail.fetch_thread_emails(email.subject, email.from_address, gmail_thread_id=email.thread_id)
#             if thread_emails:
#                 print(f"  → Found {len(thread_emails)} emails in thread")
#                 # Build thread context from CLIENT messages only
#                 # Exclude IRWT auto-replies to avoid confusing the AI
#                 client_messages = []
#                 for t_email in sorted(thread_emails, key=lambda x: x.date):
#                     if t_email.from_address != settings.gmail_address:
#                         client_messages.append(t_email.body)
#                 if client_messages:
#                     email_body_for_ai = "\n\n---\n\n".join(client_messages)
#                     print(f"  → Using {len(client_messages)} client messages for context")
#         else:
#             print(f"📧 New email: {email.subject[:40]}...")

#         # Parse the email with AI
#         result = parser.parse_rental_request(
#             email_body=email_body_for_ai,
#             email_subject=email.subject,
#             from_address=email.from_address,
#             from_name=email.from_name,
#         )
#         print(f"  → is_rental: {result.is_rental_request}, confidence: {result.confidence}")

#         # Track this email as processed
#         db.add(ProcessedEmailDB(email_id=email.id))
#         db.commit()

#         # Skip if not a rental request or confidence too low
#         if not result.is_rental_request or result.confidence < 0.5:
#             gmail.mark_as_read(email.id)
#             continue

#         # If incomplete, send follow-up email but don't save to DB
#         if not result.complete and result.missing_fields:
#             print(f"  → Incomplete, sending follow-up for: {result.missing_fields}")
#             plain_text, html_text = parser.generate_missing_info_email(
#                 original_email=email.body,
#                 missing_fields=result.missing_fields,
#                 client_name=result.extracted_data.client_name,
#                 company_email=settings.gmail_address,
#             )
#             subject = f"Re: {email.subject}"
#             gmail.send_email(
#                 to_address=email.from_address,
#                 subject=subject,
#                 body_text=plain_text,
#                 body_html=html_text,
#                 reply_to_message_id=email.id,
#             )
#             gmail.mark_as_read(email.id)
#             continue

#         # Only save complete requests to database
#         request_id = str(uuid.uuid4())

#         def parse_date(date_str):
#             if not date_str:
#                 return None
#             try:
#                 from datetime import datetime as dt
#                 return dt.strptime(date_str, "%Y-%m-%d").date()
#             except (ValueError, TypeError):
#                 return None

#         new_request = RentalRequestDB(
#             id=request_id,
#             status=RequestStatus.PENDING_SELECTION.value,
#             client_name=result.extracted_data.client_name,
#             client_email=result.extracted_data.client_email,
#             client_vat=result.extracted_data.client_vat,
#             client_phone=result.extracted_data.client_phone,
#             pickup_date=parse_date(result.extracted_data.pickup_date),
#             return_date=parse_date(result.extracted_data.return_date),
#             pickup_location=result.extracted_data.pickup_location,
#             return_location=result.extracted_data.return_location,
#             vehicle_type=result.extracted_data.vehicle_type,
#             special_requests=result.extracted_data.special_requests,
#             driver_name=result.extracted_data.driver_name,
#             artist_project_event=result.extracted_data.artist_project_event,
#             destination_cities=result.extracted_data.destination_cities,
#             original_email_id=email.id,
#             original_email_subject=email.subject,
#             original_email_body=email.body,
#             thread_id=email.thread_id,
#         )

#         db.add(new_request)
#         db.commit()
#         print(f"  → Saved complete request: {request_id[:8]}...")

#         # Log to Google Sheets
#         if sheets:
#             background_tasks.add_task(
#                 sheets.log_request,
#                 request_id,
#                 result.extracted_data.client_name,
#                 result.extracted_data.client_email,
#                 result.extracted_data.client_vat,
#                 result.extracted_data.pickup_date,
#                 result.extracted_data.return_date,
#                 result.extracted_data.pickup_location,
#                 result.extracted_data.return_location,
#                 result.extracted_data.vehicle_type,
#                 None,  # partner
#                 None,  # price
#                 new_request.status,
#             )

#         # Mark email as read
#         gmail.mark_as_read(email.id)

#         processed.append({
#             "id": request_id,
#             "client": email.from_address,
#             "status": new_request.status,
#         })

#     print(f"📧 Processed {len(processed)} emails")
#     return {"processed": len(processed), "requests": processed}


# @router.post("/check-acceptances")
# async def check_acceptances(
#     db: Session = Depends(get_db),
#     gmail: GmailService = Depends(get_gmail_service),
#     parser: EmailParserAgent = Depends(get_email_parser),
# ):
#     """Check for proposal acceptance emails."""
#     # Get requests that are waiting for acceptance
#     pending = db.query(RentalRequestDB).filter(
#         RentalRequestDB.status == RequestStatus.PROPOSAL_SENT.value
#     ).all()

#     if not pending:
#         return {"checked": 0, "acceptances": []}

#     # Get email addresses to look for
#     pending_emails = {r.client_email: r for r in pending}

#     emails = gmail.fetch_unread_emails(mark_as_read=False)
#     acceptances = []

#     for email in emails:
#         if email.from_address not in pending_emails:
#             continue

#         request = pending_emails[email.from_address]

#         # Check if this is an acceptance
#         result = parser.detect_acceptance(email.body, email.subject)

#         if result.is_acceptance and result.confidence > 0.7:
#             request.status = RequestStatus.ACCEPTED.value
#             request.updated_at = datetime.now()
#             db.commit()

#             gmail.mark_as_read(email.id)

#             acceptances.append({
#                 "request_id": request.id,
#                 "client": email.from_address,
#                 "confidence": result.confidence,
#             })

#     return {"checked": len(pending), "acceptances": acceptances}

"""API routes for the van rental automation."""

import os
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models import (
    RentalRequest,
    RentalRequestCreate,
    RentalRequestDB,
    RequestStatus,
    PartnerSelection,
    NotesUpdate,
    ProcessedEmailDB,
    # Partner & Vehicle models
    PartnerDB,
    VehicleDB,
    Partner,
    PartnerCreate,
    Vehicle,
    VehicleWithPartner,
    VehicleCreate,
)
from fastapi import Response
from config import get_settings, Settings
from services import GmailService, SheetsService
from agents import EmailParserAgent, ProposalGenerator
from agents.email_templates import (
    generate_partner_request_html,
    generate_partner_request_plain_text,
    PARTNER_REQUEST_SUBJECT,
)
from airtable import Airtable
from pyairtable import Table


router = APIRouter()


# Airtable config
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_ID = os.getenv("AIRTABLE_TABLE_NAME")
API_KEY = os.getenv("AIRTABLE_TOKEN")

if not API_KEY:
    raise ValueError("AIRTABLE_API_KEY not set in environment")

airtable = Airtable(BASE_ID, TABLE_ID, api_key=API_KEY)

# Table IDs for Airtable
CATEGORIAS_VEICULOS_TABLE_ID = "tblXEy4NCNVhO8eX2"   # Categorias de veículos
PRECOS_FORNECEDORES_TABLE_ID = "tblnSH6ba9irqfB4h"   # Preços dos fornecedores


# ============== Airtable Pydantic Models ==============

class AirtableVehicle(BaseModel):
    id: str
    group_code: str | None = None
    description: str | None = None
    category: str | None = None
    price_1_3_days: float | None = None
    is_active: bool = True
    created_at: str | None = None
    updated_at: str | None = None


class AirtablePartnerWithVehicles(BaseModel):
    id: str
    name: str | None = None
    contact_email: str | None = None
    notes: str | None = None
    is_active: bool = True
    created_at: str | None = None
    updated_at: str | None = None
    vehicles: list[AirtableVehicle]


class AirtableSupplier(BaseModel):
    id: str
    name: str | None = None
    contact_email: str | None = None
    notes: str | None = None
    is_active: bool = True
    created_at: str | None = None
    updated_at: str | None = None


# ============== Dependencies ==============

def get_db():
    from main import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_gmail_service(settings: Settings = Depends(get_settings)) -> GmailService:
    return GmailService(settings.gmail_address, settings.gmail_app_password)


def get_sheets_service(settings: Settings = Depends(get_settings)) -> Optional[SheetsService]:
    if settings.google_sheets_id and settings.google_service_account_json:
        return SheetsService(settings.google_sheets_id, settings.google_service_account_json)
    return None


def get_email_parser(settings: Settings = Depends(get_settings)) -> EmailParserAgent:
    return EmailParserAgent(settings.openai_api_key)


def get_proposal_generator(settings: Settings = Depends(get_settings)) -> ProposalGenerator:
    return ProposalGenerator(settings.openai_api_key)


# ============== Request Endpoints ==============

@router.get("/requests", response_model=list[RentalRequest])
def list_requests(
    status: Optional[RequestStatus] = None,
    db: Session = Depends(get_db),
):
    """List all rental requests, optionally filtered by status."""
    query = db.query(RentalRequestDB)

    if status:
        query = query.filter(RentalRequestDB.status == status.value)

    requests = query.order_by(RentalRequestDB.created_at.desc()).all()
    return [RentalRequest.model_validate(r) for r in requests]


@router.get("/requests/{request_id}", response_model=RentalRequest)
def get_request(request_id: str, db: Session = Depends(get_db)):
    """Get a specific rental request."""
    request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return RentalRequest.model_validate(request)


@router.post("/requests/{request_id}/select-partner")
def select_partner(
    request_id: str,
    selection: PartnerSelection,
    db: Session = Depends(get_db),
):
    """Staff selects a rent-a-car partner and vehicle for a request.

    Both selection.partner_id and selection.vehicle_id must be Airtable
    string record IDs (e.g. 'recXXXXXXXXXXXXXX').
    """
    request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    # FIX: selection.partner_id and selection.vehicle_id are now Airtable string
    # IDs. Verify the vehicle exists and belongs to the stated partner in one
    # query — no name-based Airtable lookup needed.
    vehicle = db.query(VehicleDB).filter(
        VehicleDB.id == selection.vehicle_id,
        VehicleDB.partner_id == selection.partner_id,
    ).first()
    if not vehicle:
        raise HTTPException(
            status_code=400,
            detail="Vehicle not found or does not belong to the specified partner",
        )

    # Resolve a display name from the local DB if available; fall back to the
    # Airtable ID so the field is never empty.
    partner = db.query(PartnerDB).filter(PartnerDB.id == selection.partner_id).first()
    partner_name = partner.name if partner else selection.partner_id

    request.selected_partner_id = selection.partner_id
    request.selected_vehicle_id = selection.vehicle_id
    request.selected_partner_name = partner_name
    request.selected_vehicle_description = f"{vehicle.group_code} - {vehicle.description}"
    request.cost_price = selection.cost_price
    request.price = selection.price
    request.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(request)

    return {
        "status": "success",
        "message": (
            f"Partner {partner_name} selected with vehicle "
            f"{vehicle.description} — Cost: €{selection.cost_price}, "
            f"Client: €{selection.price}"
        ),
    }


@router.post("/requests/{request_id}/send-partner-request")
async def send_partner_request(
    request_id: str,
    db: Session = Depends(get_db),
    gmail: GmailService = Depends(get_gmail_service),
):
    """Send a confirmation request email to the selected rent-a-car partner."""
    request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if not request.selected_partner_id:
        raise HTTPException(status_code=400, detail="Partner must be selected first")

    # Get partner info — selected_partner_id is now an Airtable string ID.
    partner = db.query(PartnerDB).filter(PartnerDB.id == request.selected_partner_id).first()
    if not partner:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Selected partner '{request.selected_partner_id}' not found in local DB. "
                "Ensure PartnerDB rows are synced with Airtable string IDs."
            ),
        )

    if not partner.contact_email:
        raise HTTPException(status_code=400, detail="Partner has no contact email configured")

    pickup_datetime = request.pickup_date.strftime("%d/%m/%Y") if request.pickup_date else "A confirmar"
    return_datetime = request.return_date.strftime("%d/%m/%Y") if request.return_date else "A confirmar"

    html_body = generate_partner_request_html(
        vehicle_type=request.selected_vehicle_description or request.vehicle_type or "A confirmar",
        pickup_location=request.pickup_location or "A confirmar",
        return_location=request.return_location or request.pickup_location or "A confirmar",
        pickup_datetime=pickup_datetime,
        return_datetime=return_datetime,
        driver_name=request.client_name or "A confirmar",
        destination_cities=None,
    )

    plain_text = generate_partner_request_plain_text(
        vehicle_type=request.selected_vehicle_description or request.vehicle_type or "A confirmar",
        pickup_location=request.pickup_location or "A confirmar",
        return_location=request.return_location or request.pickup_location or "A confirmar",
        pickup_datetime=pickup_datetime,
        return_datetime=return_datetime,
        driver_name=request.client_name or "A confirmar",
        destination_cities=None,
    )

    success = gmail.send_email(
        to_address=partner.contact_email,
        subject=PARTNER_REQUEST_SUBJECT,
        body_text=plain_text,
        body_html=html_body,
    )

    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email to partner")

    return {
        "status": "success",
        "message": f"Confirmation request sent to {partner.name} ({partner.contact_email})",
    }


@router.post("/requests/{request_id}/send-proposal")
async def send_proposal(
    request_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    gmail: GmailService = Depends(get_gmail_service),
    proposal_gen: ProposalGenerator = Depends(get_proposal_generator),
    sheets: Optional[SheetsService] = Depends(get_sheets_service),
    settings: Settings = Depends(get_settings),
):
    """Send a rental proposal to the client."""
    request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if not request.selected_partner_id or not request.price:
        raise HTTPException(status_code=400, detail="Partner and price must be selected first")

    if not request.pickup_date or not request.return_date:
        raise HTTPException(status_code=400, detail="Pickup and return dates are required")

    vehicle_info = request.selected_vehicle_description or request.vehicle_type or "van"

    plain_text, html = proposal_gen.generate_proposal(
        client_name=request.client_name or "Valued Customer",
        client_email=request.client_email,
        pickup_date=request.pickup_date,
        return_date=request.return_date,
        pickup_location=request.pickup_location or "TBD",
        return_location=request.return_location or request.pickup_location or "TBD",
        vehicle_type=vehicle_info,
        partner_name=request.selected_partner_name or "Partner",
        price=request.price,
        special_requests=request.special_requests,
    )

    original_subject = request.original_email_subject or f"Van Rental - {request.pickup_location}"
    subject = original_subject if original_subject.lower().startswith("re:") else f"Re: {original_subject}"

    success = gmail.send_email(
        to_address=request.client_email,
        subject=subject,
        body_text=plain_text,
        body_html=html,
        reply_to_message_id=request.original_email_id,
    )

    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email")

    request.status = RequestStatus.PROPOSAL_SENT.value
    request.updated_at = datetime.utcnow()
    db.commit()

    if sheets:
        background_tasks.add_task(
            sheets.update_request_status,
            request_id,
            RequestStatus.PROPOSAL_SENT.value,
            request.selected_partner_name,
            request.price,
        )

    return {"status": "success", "message": "Proposal sent to client"}


@router.post("/requests/{request_id}/confirm")
async def confirm_booking(
    request_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    gmail: GmailService = Depends(get_gmail_service),
    proposal_gen: ProposalGenerator = Depends(get_proposal_generator),
    sheets: Optional[SheetsService] = Depends(get_sheets_service),
    settings: Settings = Depends(get_settings),
):
    """Confirm a booking after client acceptance."""
    request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if request.status != RequestStatus.ACCEPTED.value:
        raise HTTPException(status_code=400, detail="Request must be in accepted status")

    request.status = RequestStatus.INVOICED.value
    request.updated_at = datetime.utcnow()
    db.commit()

    vehicle_info = request.selected_vehicle_description or request.vehicle_type or "van"

    plain_text, html = proposal_gen.generate_confirmation_email(
        client_name=request.client_name or "Valued Customer",
        pickup_date=request.pickup_date,
        return_date=request.return_date,
        pickup_location=request.pickup_location or "TBD",
        return_location=request.return_location or request.pickup_location or "TBD",
        vehicle_type=vehicle_info,
        partner_name=request.selected_partner_name or "Partner",
        price=request.price,
        invoice_number=None,
    )

    subject = f"Reserva Confirmada - IRWT {request.pickup_date}"
    gmail.send_email(
        to_address=request.client_email,
        subject=subject,
        body_text=plain_text,
        body_html=html,
    )

    if sheets:
        background_tasks.add_task(
            sheets.update_request_status,
            request_id,
            RequestStatus.INVOICED.value,
        )

    return {"status": "success", "message": "Booking confirmed"}


@router.post("/requests/{request_id}/mark-accepted")
def mark_accepted(request_id: str, db: Session = Depends(get_db)):
    """Manually mark a request as accepted (after client accepts via email)."""
    request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    request.status = RequestStatus.ACCEPTED.value
    request.updated_at = datetime.utcnow()
    db.commit()

    return {"status": "success", "message": "Request marked as accepted"}


@router.put("/requests/{request_id}/notes")
def update_notes(request_id: str, notes_update: NotesUpdate, db: Session = Depends(get_db)):
    """Update internal notes for a request."""
    request = db.query(RentalRequestDB).filter(RentalRequestDB.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    request.internal_notes = notes_update.notes
    request.updated_at = datetime.utcnow()
    db.commit()

    return {"status": "success", "message": "Notes updated"}


# ============== Partner Endpoints ==============

@router.get("/partners", response_model=list[Partner])
def list_partners(db: Session = Depends(get_db)):
    """List all active partners, sorted by cheapest vehicle price."""
    from sqlalchemy import func

    partners = db.query(PartnerDB).filter(PartnerDB.is_active == 1).all()

    partners_with_min_price = []
    for partner in partners:
        min_price = db.query(func.min(VehicleDB.price_1_3_days)).filter(
            VehicleDB.partner_id == partner.id,
            VehicleDB.is_active == 1,
        ).scalar()
        partners_with_min_price.append((partner, min_price or float("inf")))

    partners_with_min_price.sort(key=lambda x: x[1])
    return [Partner.model_validate(p[0]) for p in partners_with_min_price]


@router.get("/partners/{partner_id}", response_model=AirtablePartnerWithVehicles)
def get_partner(partner_id: str):
    """Get a specific partner with all their vehicles from Airtable."""
    from pydantic import ValidationError

    fornecedores_table = Table(
        os.getenv("AIRTABLE_TOKEN"),
        os.getenv("AIRTABLE_BASE_ID"),
        PRECOS_FORNECEDORES_TABLE_ID,
    )
    categorias_table = Table(
        os.getenv("AIRTABLE_TOKEN"),
        os.getenv("AIRTABLE_BASE_ID"),
        CATEGORIAS_VEICULOS_TABLE_ID,
    )

    category_records = categorias_table.all()
    price_records = fornecedores_table.all()
    price_lookup = {rec["id"]: rec for rec in price_records}

    vehicles = []
    for rec in category_records:
        fields = rec.get("fields", {})
        preco_ids = fields.get("Preços dos fornecedores", [])
        found_for_supplier = False
        for preco_id in preco_ids:
            preco_rec = price_lookup.get(preco_id)
            if not preco_rec:
                continue
            preco_fields = preco_rec.get("fields", {})
            if partner_id in preco_fields.get("Fornecedor", []):
                found_for_supplier = True
                break
        if found_for_supplier:
            vehicles.append({
                "id": rec["id"],
                "group_code": fields.get("Códigos SIPP") or fields.get("Group Code") or fields.get("Grupo"),
                "description": fields.get("Modelos de exemplo") or fields.get("Description") or fields.get("Descrição"),
                "category": fields.get("Categoria"),
                "price_1_3_days": None,
                "is_active": True,
                "created_at": rec.get("createdTime"),
                "updated_at": None,
            })

    partner_name = None
    contact_email = None
    created_at = None
    for preco_rec in price_records:
        preco_fields = preco_rec.get("fields", {})
        if partner_id in preco_fields.get("Fornecedor", []):
            full_label = preco_fields.get("Preços dos fornecedores", "")
            if full_label:
                partner_name = full_label.split("—")[0].strip()
            created_at = preco_rec.get("createdTime")
            break

    if not partner_name:
        raise HTTPException(status_code=404, detail="Partner not found in Airtable")

    try:
        return AirtablePartnerWithVehicles(
            id=partner_id,
            name=partner_name,
            contact_email=contact_email,
            notes=None,
            is_active=True,
            created_at=created_at,
            updated_at=None,
            vehicles=[
                AirtableVehicle(
                    id=v["id"],
                    group_code=v["group_code"],
                    description=v["description"],
                    category=v["category"],
                    price_1_3_days=v["price_1_3_days"],
                    is_active=v["is_active"],
                    created_at=v["created_at"],
                    updated_at=v["updated_at"] or v["created_at"],
                )
                for v in vehicles
            ],
        )
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Airtable data error: {e}")


@router.put("/partners/{partner_id}/notes")
def update_partner_notes(partner_id: str, notes_update: NotesUpdate, db: Session = Depends(get_db)):
    """Update internal notes for a partner."""
    partner = db.query(PartnerDB).filter(PartnerDB.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    partner.notes = notes_update.notes
    partner.updated_at = datetime.utcnow()
    db.commit()

    return {"status": "success", "message": "Partner notes updated"}


@router.get("/partners/{partner_id}/vehicles", response_model=list[AirtableVehicle])
def list_partner_vehicles(
    partner_id: str,
    category: Optional[str] = None,
):
    """List all vehicle categories for a specific supplier (partner) from Airtable."""
    categorias_table = Table(
        os.getenv("AIRTABLE_TOKEN"),
        os.getenv("AIRTABLE_BASE_ID"),
        CATEGORIAS_VEICULOS_TABLE_ID,
    )
    precos_fornecedores_table = Table(
        os.getenv("AIRTABLE_TOKEN"),
        os.getenv("AIRTABLE_BASE_ID"),
        PRECOS_FORNECEDORES_TABLE_ID,
    )

    category_records = categorias_table.all()
    vehicles = []
    for rec in category_records:
        fields = rec.get("fields", {})
        if category and fields.get("Categoria") != category:
            continue
        preco_ids = fields.get("Preços dos fornecedores", [])
        found_for_supplier = False
        for preco_id in preco_ids:
            preco_rec = precos_fornecedores_table.get(preco_id)
            preco_fields = preco_rec.get("fields", {})
            if partner_id in preco_fields.get("Fornecedor", []):
                found_for_supplier = True
                break
        if found_for_supplier:
            vehicles.append(AirtableVehicle(
                id=rec["id"],
                group_code=fields.get("Códigos SIPP") or fields.get("Group Code") or fields.get("Grupo"),
                description=fields.get("Modelos de exemplo") or fields.get("Description") or fields.get("Descrição"),
                category=fields.get("Categoria"),
                price_1_3_days=None,
                is_active=True,
                created_at=rec.get("createdTime"),
                updated_at=None,
            ))
    return vehicles


@router.get("/partners/{partner_id}/categories")
def list_partner_categories(partner_id: str, db: Session = Depends(get_db)):
    """List all vehicle categories for a specific partner."""
    partner = db.query(PartnerDB).filter(PartnerDB.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    categories = db.query(VehicleDB.category).filter(
        VehicleDB.partner_id == partner_id,
        VehicleDB.is_active == 1,
    ).distinct().all()

    return [c[0] for c in categories]


# ============== Vehicle Endpoints ==============

@router.get("/vehicles", response_model=list[VehicleWithPartner])
def list_all_vehicles(
    category: Optional[str] = None,
    partner_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List all vehicles across all partners with optional filters."""
    query = db.query(VehicleDB).filter(VehicleDB.is_active == 1)

    if category:
        query = query.filter(VehicleDB.category == category)
    if partner_id:
        query = query.filter(VehicleDB.partner_id == partner_id)

    vehicles = query.order_by(VehicleDB.partner_id, VehicleDB.category, VehicleDB.group_code).all()
    return [VehicleWithPartner.model_validate(v) for v in vehicles]


@router.get("/vehicles/{vehicle_id}", response_model=VehicleWithPartner)
def get_vehicle(vehicle_id: str, db: Session = Depends(get_db)):  # FIX: int → str
    """Get a specific vehicle with its partner info."""
    vehicle = db.query(VehicleDB).filter(VehicleDB.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return VehicleWithPartner.model_validate(vehicle)


# ============== Category Endpoints ==============

@router.get("/categories")
def list_all_categories(db: Session = Depends(get_db)):
    """List all unique vehicle categories from Airtable."""
    records = airtable.get_all(max_records=None)

    categorias_set = set()
    for record in records:
        categoria = record.get("fields", {}).get("Categoria")
        if categoria:
            categorias_set.add(categoria)

    return sorted(categorias_set)


@router.get("/categories/{category}/partners", response_model=list[AirtableSupplier])
def list_partners_by_category(category: str):
    """List partners (suppliers) from Airtable for the given category."""
    categorias_table = Table(
        os.getenv("AIRTABLE_TOKEN"),
        os.getenv("AIRTABLE_BASE_ID"),
        CATEGORIAS_VEICULOS_TABLE_ID,
    )
    fornecedores_table = Table(
        os.getenv("AIRTABLE_TOKEN"),
        os.getenv("AIRTABLE_BASE_ID"),
        PRECOS_FORNECEDORES_TABLE_ID,
    )

    category_records = categorias_table.all()
    categories = {
        rec["fields"].get("Categoria", "").strip(): rec["id"]
        for rec in category_records
        if rec["fields"].get("Categoria")
    }

    normalized = category.strip().lower()
    matched = {name: rec_id for name, rec_id in categories.items() if name.lower() == normalized}
    if not matched:
        # Prefix fallback (handles simple singular/plural differences)
        stem = normalized[:-1] if normalized.endswith("s") else normalized
        matched = {name: rec_id for name, rec_id in categories.items() if name.lower().startswith(stem)}

    if not matched:
        raise HTTPException(
            status_code=404,
            detail=f"No categories found matching '{category}'. Available: {list(categories.keys())}",
        )

    seen: set[str] = set()
    suppliers: list[AirtableSupplier] = []

    for cat_name, category_id in matched.items():
        cat_record = next((rec for rec in category_records if rec["id"] == category_id), None)
        if not cat_record:
            continue
        supplier_price_ids = cat_record["fields"].get("Preços dos fornecedores", [])
        for price_id in supplier_price_ids:
            record = fornecedores_table.get(price_id)
            fields = record["fields"]
            supplier_ids = fields.get("Fornecedor", [])
            full_label = fields.get("Preços dos fornecedores", "")
            supplier_name = full_label.split("—")[0].strip() if full_label else None

            for supplier_id in supplier_ids:
                if supplier_id not in seen:
                    seen.add(supplier_id)
                    suppliers.append(AirtableSupplier(
                        id=supplier_id,
                        name=supplier_name,
                        contact_email=None,
                        notes=None,
                        is_active=True,
                        created_at=record["createdTime"],
                        updated_at=None,
                    ))

    return suppliers


# ============== Email Processing ==============

@router.post("/process-emails")
async def process_emails(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    gmail: GmailService = Depends(get_gmail_service),
    parser: EmailParserAgent = Depends(get_email_parser),
    sheets: Optional[SheetsService] = Depends(get_sheets_service),
    settings: Settings = Depends(get_settings),
):
    """Process unread emails and create rental requests."""
    print("📧 Processing emails...")

    emails = gmail.fetch_unread_emails(mark_as_read=False)
    print(f"Found {len(emails)} unread emails")

    processed = []
    for email in emails:
        if email.from_address == settings.gmail_address:
            continue

        already_processed = db.query(ProcessedEmailDB).filter(
            ProcessedEmailDB.email_id == email.id
        ).first()
        if already_processed:
            continue

        is_reply = email.subject.lower().startswith("re:")
        email_body_for_ai = email.body

        if is_reply:
            print(f"📩 Reply detected: {email.subject[:40]}...")
            print(f"  → From: {email.from_address}")

            existing_request = db.query(RentalRequestDB).filter(
                RentalRequestDB.client_email == email.from_address,
                RentalRequestDB.status == RequestStatus.PROPOSAL_SENT.value,
            ).first()

            if existing_request:
                print(f"  → Found existing request {existing_request.id[:8]} with PROPOSAL_SENT status")
                acceptance_result = parser.detect_acceptance(email.body, email.subject)
                print(f"  → Acceptance check: is_acceptance={acceptance_result.is_acceptance}, confidence={acceptance_result.confidence}")

                if acceptance_result.is_acceptance and acceptance_result.confidence > 0.7:
                    print(f"  ✅ Proposal ACCEPTED by {email.from_address}")

                    existing_request.status = RequestStatus.ACCEPTED.value
                    existing_request.updated_at = datetime.utcnow()
                    db.commit()

                    db.add(ProcessedEmailDB(email_id=email.id))
                    db.commit()

                    gmail.mark_as_read(email.id)

                    if sheets:
                        background_tasks.add_task(
                            sheets.update_request_status,
                            existing_request.id,
                            RequestStatus.ACCEPTED.value,
                        )

                    processed.append({
                        "id": existing_request.id,
                        "client": email.from_address,
                        "status": "accepted",
                        "action": "proposal_accepted",
                    })
                    continue

            if not existing_request:
                print(f"  → No existing PROPOSAL_SENT request found for {email.from_address}")

            thread_emails = gmail.fetch_thread_emails(
                email.subject, email.from_address, gmail_thread_id=email.thread_id
            )
            if thread_emails:
                print(f"  → Found {len(thread_emails)} emails in thread")
                client_messages = [
                    t_email.body
                    for t_email in sorted(thread_emails, key=lambda x: x.date)
                    if t_email.from_address != settings.gmail_address
                ]
                if client_messages:
                    email_body_for_ai = "\n\n---\n\n".join(client_messages)
                    print(f"  → Using {len(client_messages)} client messages for context")
        else:
            print(f"📧 New email: {email.subject[:40]}...")

        result = parser.parse_rental_request(
            email_body=email_body_for_ai,
            email_subject=email.subject,
            from_address=email.from_address,
            from_name=email.from_name,
        )
        print(f"  → is_rental: {result.is_rental_request}, confidence: {result.confidence}")

        db.add(ProcessedEmailDB(email_id=email.id))
        db.commit()

        if not result.is_rental_request or result.confidence < 0.5:
            gmail.mark_as_read(email.id)
            continue

        if not result.complete and result.missing_fields:
            print(f"  → Incomplete, sending follow-up for: {result.missing_fields}")
            plain_text, html_text = parser.generate_missing_info_email(
                original_email=email.body,
                missing_fields=result.missing_fields,
                client_name=result.extracted_data.client_name,
                company_email=settings.gmail_address,
            )
            gmail.send_email(
                to_address=email.from_address,
                subject=f"Re: {email.subject}",
                body_text=plain_text,
                body_html=html_text,
                reply_to_message_id=email.id,
            )
            gmail.mark_as_read(email.id)
            continue

        request_id = str(uuid.uuid4())

        def parse_date(date_str):
            if not date_str:
                return None
            try:
                from datetime import datetime as dt
                return dt.strptime(date_str, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                return None

        new_request = RentalRequestDB(
            id=request_id,
            status=RequestStatus.PENDING_SELECTION.value,
            client_name=result.extracted_data.client_name,
            client_email=result.extracted_data.client_email,
            client_vat=result.extracted_data.client_vat,
            client_phone=result.extracted_data.client_phone,
            pickup_date=parse_date(result.extracted_data.pickup_date),
            return_date=parse_date(result.extracted_data.return_date),
            pickup_location=result.extracted_data.pickup_location,
            return_location=result.extracted_data.return_location,
            vehicle_type=result.extracted_data.vehicle_type,
            special_requests=result.extracted_data.special_requests,
            driver_name=result.extracted_data.driver_name,
            artist_project_event=result.extracted_data.artist_project_event,
            destination_cities=result.extracted_data.destination_cities,
            original_email_id=email.id,
            original_email_subject=email.subject,
            original_email_body=email.body,
            thread_id=email.thread_id,
        )

        db.add(new_request)
        db.commit()
        print(f"  → Saved complete request: {request_id[:8]}...")

        if sheets:
            background_tasks.add_task(
                sheets.log_request,
                request_id,
                result.extracted_data.client_name,
                result.extracted_data.client_email,
                result.extracted_data.client_vat,
                result.extracted_data.pickup_date,
                result.extracted_data.return_date,
                result.extracted_data.pickup_location,
                result.extracted_data.return_location,
                result.extracted_data.vehicle_type,
                None,
                None,
                new_request.status,
            )

        gmail.mark_as_read(email.id)

        processed.append({
            "id": request_id,
            "client": email.from_address,
            "status": new_request.status,
        })

    print(f"📧 Processed {len(processed)} emails")
    return {"processed": len(processed), "requests": processed}


@router.post("/check-acceptances")
async def check_acceptances(
    db: Session = Depends(get_db),
    gmail: GmailService = Depends(get_gmail_service),
    parser: EmailParserAgent = Depends(get_email_parser),
):
    """Check for proposal acceptance emails."""
    pending = db.query(RentalRequestDB).filter(
        RentalRequestDB.status == RequestStatus.PROPOSAL_SENT.value
    ).all()

    if not pending:
        return {"checked": 0, "acceptances": []}

    pending_emails = {r.client_email: r for r in pending}
    emails = gmail.fetch_unread_emails(mark_as_read=False)
    acceptances = []

    for email in emails:
        if email.from_address not in pending_emails:
            continue

        request = pending_emails[email.from_address]
        result = parser.detect_acceptance(email.body, email.subject)

        if result.is_acceptance and result.confidence > 0.7:
            request.status = RequestStatus.ACCEPTED.value
            request.updated_at = datetime.utcnow()
            db.commit()

            gmail.mark_as_read(email.id)

            acceptances.append({
                "request_id": request.id,
                "client": email.from_address,
                "confidence": result.confidence,
            })

    return {"checked": len(pending), "acceptances": acceptances}