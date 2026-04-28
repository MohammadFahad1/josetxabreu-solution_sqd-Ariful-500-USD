"""
Re-sync partners table from Airtable after schema migration.

Fetches all unique supplier IDs and names from the 'Preços dos fornecedores'
table (tblnSH6ba9irqfB4h) and upserts them into the local partners table
using Airtable record IDs as the primary key.

Run inside the api container:
    docker compose exec api python scripts/resync_partners_from_airtable.py
"""
import os
import sys
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Allow running from backend root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Base, PartnerDB

DATABASE_URL = os.environ.get("DATABASE_URL", "")
AIRTABLE_TOKEN = os.environ.get("AIRTABLE_TOKEN", "")
AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "")
PRECOS_FORNECEDORES_TABLE_ID = "tblnSH6ba9irqfB4h"  # Preços dos fornecedores

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    sys.exit(1)
if not AIRTABLE_TOKEN or not AIRTABLE_BASE_ID:
    print("ERROR: AIRTABLE_TOKEN or AIRTABLE_BASE_ID not set")
    sys.exit(1)


def run():
    from pyairtable import Table

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Fetching price records from Airtable…")
    precos_table = Table(AIRTABLE_TOKEN, AIRTABLE_BASE_ID, PRECOS_FORNECEDORES_TABLE_ID)
    price_records = precos_table.all()
    print(f"  Found {len(price_records)} price records")

    # Build unique supplier map: supplier_airtable_id → name
    supplier_map: dict[str, str] = {}
    for rec in price_records:
        fields = rec.get("fields", {})
        supplier_ids = fields.get("Fornecedor", [])
        full_label = fields.get("Preços dos fornecedores", "")
        partner_name = full_label.split("—")[0].strip() if full_label else None
        if not partner_name:
            continue
        for supplier_id in supplier_ids:
            if supplier_id not in supplier_map:
                supplier_map[supplier_id] = partner_name

    print(f"  Found {len(supplier_map)} unique suppliers")

    upserted = 0
    for supplier_id, name in supplier_map.items():
        existing = session.query(PartnerDB).filter(PartnerDB.id == supplier_id).first()
        if existing:
            existing.name = name
            existing.updated_at = datetime.utcnow()
            print(f"  Updated: {name} ({supplier_id})")
        else:
            partner = PartnerDB(
                id=supplier_id,
                name=name,
                is_active=1,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(partner)
            print(f"  Inserted: {name} ({supplier_id})")
        upserted += 1

    session.commit()
    session.close()
    print(f"\nDone — {upserted} partners synced.")


if __name__ == "__main__":
    run()
