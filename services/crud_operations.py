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
    # Create a log after adding the tire to database
    create_log("Added new tire to database", new_tire.tire_id, f"Added a new tire of type {tire_type}, brand {tire_brand}, size {tire_size}")


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
    tire_stock = TireStock(tire_id=tire.tire_id, location_id=location.location_id, quantity=quantity)
    db.session.add(tire_stock)
    db.session.commit()

    # Create a log after adding tire to the stock
    create_log("Added new tire to stock", tire_stock.location_id, f"Added a tire {tire_id}, into location {tire_stock.location_id}, {quantity} pieces.")


def add_location(location_name):
    # First, check if a location with this name already exists to avoid duplicates
    existing_location = StockLocations.query.filter_by(name=location_name).first()
    if existing_location:
        return "Location with this name already exists."

    new_location = StockLocations(name=location_name)
    db.session.add(new_location)
    db.session.commit()
    return "Stock location added successfully!"

    # Create a log after adding new stock location to database
    create_log("Added new stock location to database", new_location.location_id, f"Added a new stock location {name}.")

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

    # Create a log after updating tire quantity at location
    create_log("Updated quantity of tire at location", tire_stock.tire_id, f"Updated quantity of {tire_type}, brand {tire_brand}, size {tire_size} at location {location_name}")

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

    # Create a log after removing tire from stock
    create_log("Removed tire from stock", location_name.tire_id, f"Removed {tire_type}, brand {tire_brand}, size {tire_size} from location {location_name}")


def create_log(action_type, tire_id, details=None):
    log = Logs(action_type=action_type, tire_id=tire_id, details=details)
    db.session.add(log)
    db.session.commit()