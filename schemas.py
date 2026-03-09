from datetime import date
from pydantic import BaseModel, ConfigDict


class SearchRequest(BaseModel):
    location_code: str
    pickup_date: date
    dropoff_date: date
    vehicle_type: str = "Any"


class VehicleBase(BaseModel):
    supplier_name: str
    vehicle_model: str
    daily_rate_eur: float
    emissions_co2_kg: float
    availability_status: str = "Available"


class VehicleCreate(VehicleBase):
    id: str


class VehicleResponse(VehicleBase):
    id: str
    model_config = ConfigDict(from_attributes=True)


class BookingBase(BaseModel):
    vehicle_id: str
    partner_id: str
    start_date: date
    end_date: date


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    booking_reference: str
    total_price: float
    status: str = "Confirmed"
    model_config = ConfigDict(from_attributes=True)