import logging
import os
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

from fastapi import FastAPI, Response, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import APIKeyHeader
from sqlalchemy import text, func
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("fleet-aggregator")

models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages application lifecycle and persistent connections."""
    logger.info("B2B Fleet Aggregator API starting up.")
    yield
    logger.info("B2B Fleet Aggregator API shutting down.")


app = FastAPI(
    title="🤖 B2B Fleet Aggregator API",
    description="Middleware bridging macro-strategic forecasting with micro-tactical fleet execution.",
    version="1.0.0",
    contact={
        "name": "Sandesh Hegde",
        "url": "https://github.com/sandesh-s-hegde/b2b-fleet-aggregator-api",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Tracks request latency and injects telemetry into response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time-Sec"] = str(round(process_time, 4))
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catches unhandled server errors to prevent stack trace leakage."""
    logger.error(f"Unhandled systemic anomaly on {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected anomaly occurred. Engineering has been notified.",
            "path": request.url.path
        }
    )


async def verify_api_key(api_key: str = Depends(api_key_header)):
    """Validates partner API keys against environment secrets."""
    expected_key = os.getenv("B2B_API_KEY", "PARTNER-PROD-KEY-99")
    if api_key != expected_key:
        raise HTTPException(status_code=403, detail="Invalid or missing B2B API Key")


@app.get("/", include_in_schema=False)
async def root_redirect():
    """Routes root traffic to API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Response:
    return Response(status_code=204)


@app.get("/api/v1/health", tags=["System"])
async def health_check(db: Session = Depends(get_db)) -> dict:
    """Verifies API uptime and active database connectivity."""
    try:
        db.execute(text("SELECT 1"))
        db_status = "Connected"
    except Exception:
        db_status = "Disconnected"
        raise HTTPException(status_code=503, detail="Database connection failed")

    return {
        "api_status": "Online",
        "database_status": db_status,
        "timestamp": datetime.now(),
        "version": app.version
    }


@app.post("/api/v1/vehicles", response_model=schemas.VehicleResponse, tags=["Fleet Management"])
async def add_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    """Provisions a single vehicle into the supplier catalog."""
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@app.post("/api/v1/vehicles/batch", response_model=dict, tags=["Fleet Management"])
async def add_vehicles_batch(vehicles: List[schemas.VehicleCreate], db: Session = Depends(get_db)):
    """Ingests a bulk payload of vehicles for high-volume onboarding."""
    db_vehicles = [models.Vehicle(**v.model_dump()) for v in vehicles]
    db.add_all(db_vehicles)
    db.commit()
    return {"detail": f"Successfully ingested {len(vehicles)} vehicles into the fleet catalog."}


@app.get("/api/v1/vehicles", response_model=List[schemas.VehicleResponse], tags=["Fleet Management"])
async def get_all_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieves paginated supplier catalog."""
    return db.query(models.Vehicle).offset(skip).limit(limit).all()


@app.post("/api/v1/fleet/search", response_model=List[schemas.VehicleResponse], tags=["Aggregation Engine"])
async def search_fleet_capacity(request: schemas.SearchRequest, db: Session = Depends(get_db)):
    """Filters available fleet capacity, prioritizing low-emission assets."""
    query = db.query(models.Vehicle).filter(models.Vehicle.availability_status == "Available")

    if request.vehicle_type:
        query = query.filter(models.Vehicle.vehicle_model.contains(request.vehicle_type))

    vehicles = query.all()

    if not vehicles:
        raise HTTPException(status_code=404, detail="No available vehicles found for this configuration.")

    return sorted(vehicles, key=lambda v: (v.emissions_co2_kg, v.daily_rate_eur))


@app.post("/api/v1/bookings", response_model=schemas.BookingResponse, tags=["Booking Engine"])
async def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db),
                         api_key: str = Depends(verify_api_key)):
    """Executes a secure B2B transaction with dynamic surge pricing calculation."""
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == booking.vehicle_id).first()

    if not vehicle or vehicle.availability_status != "Available":
        raise HTTPException(status_code=400, detail="Vehicle is unavailable or does not exist.")

    total_fleet = db.query(models.Vehicle).count()
    available_fleet = db.query(models.Vehicle).filter(models.Vehicle.availability_status == "Available").count()

    utilization = (total_fleet - available_fleet) / total_fleet if total_fleet > 0 else 0.0
    surge_multiplier = 1.2 if utilization > 0.8 else 1.0

    days = max((booking.end_date - booking.start_date).days, 1)
    total_price = days * vehicle.daily_rate_eur * surge_multiplier

    new_booking = models.Booking(
        booking_reference=f"CONF-{uuid.uuid4().hex[:6].upper()}",
        vehicle_id=booking.vehicle_id,
        partner_id=booking.partner_id,
        start_date=booking.start_date,
        end_date=booking.end_date,
        total_price=total_price,
        status="Confirmed"
    )

    vehicle.availability_status = "Booked"
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


@app.get("/api/v1/bookings/{partner_id}", response_model=List[schemas.BookingResponse], tags=["Booking Engine"])
async def get_partner_bookings(partner_id: str, db: Session = Depends(get_db)):
    """Retrieves all active reservations associated with a specific B2B partner."""
    bookings = db.query(models.Booking).filter(models.Booking.partner_id == partner_id).all()
    if not bookings:
        raise HTTPException(status_code=404, detail="No active bookings found for this partner.")
    return bookings


@app.patch("/api/v1/bookings/{booking_reference}/cancel", response_model=schemas.BookingResponse,
           tags=["Booking Engine"])
async def cancel_booking(booking_reference: str, db: Session = Depends(get_db)):
    """Voids an active transaction and releases the underlying asset."""
    booking = db.query(models.Booking).filter(models.Booking.booking_reference == booking_reference).first()

    if not booking or booking.status == "Cancelled":
        raise HTTPException(status_code=400, detail="Booking is invalid or already cancelled.")

    booking.status = "Cancelled"
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == booking.vehicle_id).first()
    if vehicle:
        vehicle.availability_status = "Available"

    db.commit()
    db.refresh(booking)
    return booking


@app.get("/api/v1/fleet/utilization", tags=["System Analytics"])
async def get_fleet_utilization(db: Session = Depends(get_db)):
    """Calculates macro-level fleet utilization metrics."""
    total_vehicles = db.query(models.Vehicle).count()
    available_vehicles = db.query(models.Vehicle).filter(models.Vehicle.availability_status == "Available").count()
    active_bookings = db.query(models.Booking).filter(models.Booking.status == "Confirmed").count()

    utilization_rate = ((total_vehicles - available_vehicles) / total_vehicles) * 100 if total_vehicles > 0 else 0.0

    return {
        "total_vehicles": total_vehicles,
        "available_vehicles": available_vehicles,
        "active_bookings": active_bookings,
        "utilization_rate_percentage": round(utilization_rate, 2)
    }


@app.get("/api/v1/fleet/revenue", tags=["System Analytics"])
async def get_financial_metrics(db: Session = Depends(get_db)):
    """Aggregates transactional volume across all active bookings."""
    total_revenue = db.query(func.sum(models.Booking.total_price)).filter(
        models.Booking.status == "Confirmed"
    ).scalar() or 0.0

    return {
        "currency": "EUR",
        "total_revenue_generated": round(total_revenue, 2),
        "timestamp": datetime.now()
    }


@app.delete("/api/v1/vehicles/{vehicle_id}", tags=["Fleet Management"])
async def retire_vehicle(vehicle_id: str, db: Session = Depends(get_db)):
    """Safely decommissions a vehicle from the catalog if no active bookings exist."""
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found.")

    active_booking = db.query(models.Booking).filter(
        models.Booking.vehicle_id == vehicle_id,
        models.Booking.status == "Confirmed"
    ).first()

    if active_booking:
        raise HTTPException(status_code=400, detail="Cannot retire asset with active transactions.")

    db.delete(vehicle)
    db.commit()

    return {"detail": f"Vehicle {vehicle_id} decommissioned successfully."}