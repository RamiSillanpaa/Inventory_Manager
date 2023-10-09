# services/crud_operations.py

from models.tires import Tires
from models.locations import StockLocations
from models.tire_stock import TireStock
from models.logs import Logs
from factory import db

# All the CRUD functions go here...

def add_tire(tire_type, tire_brand, tire_size):
    new_tire = Tires(type=tire_type, brand=tire_brand, size=tire_size)
    db.session.add(new_tire)
    db.session.commit()


# For this, we need to ensure:
# - The stock location exists.
# - The stock location isn't occupied if it's not flexible.
# - The tire exists.
def add_tire_to_stock(tire_id, location_name, quantity):
    location = StockLocations.query.filter_by(name=location_name).first()
    tire = Tires.query.get(tire_id)
    
    if not location or not tire:
        return "Invalid location or tire"

    if location.is_occupied and not location.is_flexible:
        return "Location is occupied"

    location.is_occupied = True
    tire_stock = TireStock(tire_id=tire.tire_id, location_id=location.id, quantity=quantity)
    db.session.add(tire_stock)
    db.session.commit()

def get_tires_from_location(location_name):
    location = StockLocations.query.filter_by(name=location_name).first()
    if not location:
        return "Invalid location"

    tires = TireStock.query.filter_by(location_id=location.id).all()
    return tires

def update_tire_quantity_at_location(tire_id, location_name, new_quantity):
    location = StockLocations.query.filter_by(name=location_name).first()
    if not location:
        return "Invalid location"

    tire_stock = TireStock.query.filter_by(tire_id=tire_id, location_id=location.id).first()
    if not tire_stock:
        return "Tire not found at this location"

    tire_stock.quantity = new_quantity
    db.session.commit()

def remove_tire_from_location(tire_id, location_name):
    location = StockLocations.query.filter_by(name=location_name).first()
    if not location:
        return "Invalid location"

    tire_stock = TireStock.query.filter_by(tire_id=tire_id, location_id=location.id).first()
    if not tire_stock:
        return "Tire not found at this location"

    db.session.delete(tire_stock)
    
    if not location.is_flexible:
        location.is_occupied = False

    db.session.commit()
