from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShipmentBase(BaseModel):
    tracking_number: str
    sender: str
    recipient: str
    origin: str
    destination: str
    weight: Optional[float] = None
    status: Optional[str] = "Pending"
    delivered: Optional[bool] = False

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentUpdate(BaseModel):
    status: Optional[str] = None
    delivered: Optional[bool] = None

class Shipment(ShipmentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
