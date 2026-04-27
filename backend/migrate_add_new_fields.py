"""Migration script to add new fields to the database.

For production (PostgreSQL), run inside the container:
  docker compose exec api python migrate_add_new_fields.py

Or connect to PostgreSQL directly and run:
  ALTER TABLE rental_requests ADD COLUMN IF NOT EXISTS driver_name VARCHAR;
  ALTER TABLE rental_requests ADD COLUMN IF NOT EXISTS artist_project_event VARCHAR;
  ALTER TABLE rental_requests ADD COLUMN IF NOT EXISTS destination_cities VARCHAR;

For local development (SQLite), the schema is created automatically on startup.
"""

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./data/rental_automation.db")

def migrate():
    """Add new columns to rental_requests table."""
    print(f"Migrating database...")

    engine = create_engine(DATABASE_URL)

    # Columns to add
    columns = [
        "driver_name",
        "artist_project_event",
        "destination_cities",
    ]

    with engine.connect() as conn:
        for column in columns:
            try:
                if "postgresql" in DATABASE_URL:
                    # PostgreSQL syntax
                    conn.execute(text(f"ALTER TABLE rental_requests ADD COLUMN IF NOT EXISTS {column} VARCHAR"))
                else:
                    # SQLite syntax (no IF NOT EXISTS support)
                    conn.execute(text(f"ALTER TABLE rental_requests ADD COLUMN {column} VARCHAR"))
                conn.commit()
                print(f"Added column: {column}")
            except Exception as e:
                if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                    print(f"Column {column} already exists")
                else:
                    print(f"Error adding {column}: {e}")

    print("Migration complete!")

if __name__ == "__main__":
    migrate()
