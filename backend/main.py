"""Main FastAPI application for van rental automation."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx

from config import get_settings
from models import get_engine, get_session_maker, init_db
from api import router

# Global database session
settings = get_settings()
engine = get_engine(settings.database_url)
SessionLocal = get_session_maker(engine)

# Scheduler for periodic email checking
scheduler = AsyncIOScheduler()


async def check_emails_job():
    """Background job to check for new emails."""
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{settings.api_url}/api/process-emails", timeout=60)
    except Exception as e:
        print(f"Email check failed: {e}")


async def check_acceptances_job():
    """Background job to check for acceptances."""
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{settings.api_url}/api/check-acceptances", timeout=60)
    except Exception as e:
        print(f"Acceptance check failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Initialize database
    init_db(engine)

    # Start scheduler
    scheduler.add_job(check_emails_job, "interval", seconds=20, id="check_emails")
    scheduler.add_job(check_acceptances_job, "interval", minutes=5, id="check_acceptances")
    scheduler.start()

    print("Van Rental Automation started!")
    print(f"API running at {settings.api_url}")

    yield

    # Shutdown
    scheduler.shutdown()


app = FastAPI(
    title="Van Rental Automation",
    description="Automated van rental email processing and invoicing",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        settings.frontend_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {
        "name": "Van Rental Automation",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
