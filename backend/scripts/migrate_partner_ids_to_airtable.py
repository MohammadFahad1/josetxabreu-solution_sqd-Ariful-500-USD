import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import PartnerDB, VehicleDB, RentalRequestDB, Base
from pyairtable import Table

# --- CONFIG ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_PARTNER_TABLE_ID = "tblnSH6ba9irqfB4h"  # Preços dos fornecedores

# --- DB Setup ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_airtable_partner_id_map():
    """Return a dict mapping partner name to Airtable record ID."""
    table = Table(AIRTABLE_TOKEN, AIRTABLE_BASE_ID, AIRTABLE_PARTNER_TABLE_ID)
    records = table.all()
    name_to_id = {}
    for rec in records:
        fields = rec.get('fields', {})
        # Use the label before '—' as the name (as in your API logic)
        full_label = fields.get('Preços dos fornecedores', "")
        if full_label:
            name = full_label.split("—")[0].strip()
            name_to_id[name] = rec['id']
    return name_to_id

def migrate():
    session = SessionLocal()
    name_to_airtable_id = get_airtable_partner_id_map()
    print(f"Found {len(name_to_airtable_id)} Airtable partners.")

    # Update PartnerDB and clean up legacy partners
    partners = session.query(PartnerDB).all()
    airtable_ids = set(name_to_airtable_id.values())
    for partner in partners:
        airtable_id = name_to_airtable_id.get(partner.name)
        if airtable_id and partner.id != airtable_id:
            print(f"Updating Partner '{partner.name}' ID: {partner.id} -> {airtable_id}")
            old_id = partner.id
            partner.id = airtable_id
            # Update all vehicles
            vehicles = session.query(VehicleDB).filter(VehicleDB.partner_id == old_id).all()
            for v in vehicles:
                v.partner_id = airtable_id
            # Update all rental requests
            requests = session.query(RentalRequestDB).filter(RentalRequestDB.selected_partner_id == old_id).all()
            for r in requests:
                r.selected_partner_id = airtable_id

    # Delete partners not in Airtable
    legacy_partners = session.query(PartnerDB).filter(~PartnerDB.id.in_(airtable_ids)).all()
    for legacy in legacy_partners:
        print(f"Deleting legacy partner: {legacy.name} (ID: {legacy.id})")
        # Find all vehicles for this partner
        vehicles = session.query(VehicleDB).filter(VehicleDB.partner_id == legacy.id).all()
        vehicle_ids = [v.id for v in vehicles]
        if vehicle_ids:
            # Set selected_vehicle_id to NULL in rental requests referencing these vehicles
            session.query(RentalRequestDB).filter(RentalRequestDB.selected_vehicle_id.in_(vehicle_ids)).update({RentalRequestDB.selected_vehicle_id: None}, synchronize_session=False)
            # Delete vehicles
            for v in vehicles:
                session.delete(v)
        # Set selected_partner_id to NULL in rental requests referencing this partner
        session.query(RentalRequestDB).filter(RentalRequestDB.selected_partner_id == legacy.id).update({RentalRequestDB.selected_partner_id: None}, synchronize_session=False)
        session.delete(legacy)

    session.commit()
    print("Migration complete. Legacy partners removed.")
    session.close()

if __name__ == "__main__":
    migrate()
