import uuid
from datetime import datetime
from typing import List

from fastapi import FastAPI, Response, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="B2B Fleet Aggregator API",
    description="CarTrawler-style API connecting logistics platforms to commercial rental suppliers.",
    version="1.0.0"
)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Response:
    """Silences the browser's default favicon request error."""
    return Response(status_code=204)


@app.get("/", tags=["System"])
async def root() -> dict:
    """Health check endpoint to verify the API is online."""
    return {
        "status": "Online",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }


@app.post("/api/v1/vehicles", response_model=schemas.VehicleResponse, tags=["Fleet Management"])
async def add_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    """Registers a new commercial vehicle into the supplier database."""
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@app.get("/api/v1/vehicles", response_model=List[schemas.VehicleResponse], tags=["Fleet Management"])
async def get_all_vehicles(db: Session = Depends(get_db)):
    """Fetches the entire catalog of available supplier vehicles."""
    return db.query(models.Vehicle).all()


@app.post("/api/v1/fleet/search", response_model=List[schemas.VehicleResponse], tags=["Aggregation Engine"])
async def search_fleet_capacity(request: schemas.SearchRequest, db: Session = Depends(get_db)):
    """Simulates searching the supplier network for available vehicles based on route criteria."""
    available_vehicles = db.query(models.Vehicle).filter(
        models.Vehicle.availability_status == "Available"
    ).all()

    if not available_vehicles:
        raise HTTPException(status_code=404, detail="No available vehicles found for this route.")

    return available_vehicles


@app.post("/api/v1/bookings", response_model=schemas.BookingResponse, tags=["Booking Engine"])
async def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    """Executes a secure B2B fleet booking and generates a confirmation reference."""
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == booking.vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found in supplier catalog.")
    if vehicle.availability_status != "Available":
        raise HTTPException(status_code=400, detail="Vehicle is no longer available for booking.")

    delta = booking.end_date - booking.start_date
    days = max(delta.days, 1)
    total_price = days * vehicle.daily_rate_eur

    booking_ref = f"CONF-{uuid.uuid4().hex[:6].upper()}"

    new_booking = models.Booking(
        booking_reference=booking_ref,
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
    """Retrieves all active fleet reservations for a specific B2B partner."""
    bookings = db.query(models.Booking).filter(models.Booking.partner_id == partner_id).all()

    if not bookings:
        raise HTTPException(status_code=404, detail="No active bookings found for this partner.")

    return bookings


@app.patch("/api/v1/bookings/{booking_reference}/cancel", response_model=schemas.BookingResponse,
           tags=["Booking Engine"])
async def cancel_booking(booking_reference: str, db: Session = Depends(get_db)):
    """Cancels an active booking and releases the vehicle back into the available fleet pool."""
    booking = db.query(models.Booking).filter(models.Booking.booking_reference == booking_reference).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking reference not found.")
    if booking.status == "Cancelled":
        raise HTTPException(status_code=400, detail="Booking is already cancelled.")

    booking.status = "Cancelled"

    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == booking.vehicle_id).first()
    if vehicle:
        vehicle.availability_status = "Available"

    db.commit()
    db.refresh(booking)

    return booking


@app.get("/api/v1/fleet/utilization", tags=["System Analytics"])
async def get_fleet_utilization(db: Session = Depends(get_db)):
    """Calculates real-time fleet utilization rates and availability metrics."""
    total_vehicles = db.query(models.Vehicle).count()
    available_vehicles = db.query(models.Vehicle).filter(models.Vehicle.availability_status == "Available").count()
    active_bookings = db.query(models.Booking).filter(models.Booking.status == "Confirmed").count()

    utilization_rate = 0.0
    if total_vehicles > 0:
        utilization_rate = ((total_vehicles - available_vehicles) / total_vehicles) * 100

    return {
        "total_vehicles": total_vehicles,
        "available_vehicles": available_vehicles,
        "active_bookings": active_bookings,
        "utilization_rate_percentage": round(utilization_rate, 2)
    }


@app.delete("/api/v1/vehicles/{vehicle_id}", tags=["Fleet Management"])
async def retire_vehicle(vehicle_id: str, db: Session = Depends(get_db)):
    """Safely retires a vehicle from the active catalog if it has no active bookings."""
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found.")

    active_booking = db.query(models.Booking).filter(
        models.Booking.vehicle_id == vehicle_id,
        models.Booking.status == "Confirmed"
    ).first()

    if active_booking:
        raise HTTPException(status_code=400, detail="Cannot retire a vehicle with an active booking.")

    db.delete(vehicle)
    db.commit()

    return {"detail": f"Vehicle {vehicle_id} successfully retired from the fleet."}