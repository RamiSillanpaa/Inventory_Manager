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
    create_log("Added new tire to database", new_tire.tire_id, f"Added a new tire of type {tire_type}, brand {tire_brand}, size {tire_size} into database")


# - The stock location exists.
# - The stock location isn't occupied if it's not flexible.
# - The tire exists.
def add_tire_to_stock(tire_id, location_name, quantity):
    location = StockLocations.query.filter_by(name=location_name).first()
    tire = Tires.query.get(tire_id)
    
    if location.is_occupied and not location.is_flexible:
        return "Location is occupied"

    location.is_occupied = True

    if not location or not tire:
        return "Invalid location or tire"
    
    tire_stock_record = TireStock.query.filter_by(tire_id=tire_id, location_id=location_name).first()
    
    if tire_stock_record:
        tire_stock_record.quantity += quantity
    else:
        tire_stock = TireStock(tire_id=tire.tire_id, location_id=location_name, quantity=quantity)
        db.session.add(tire_stock)

    db.session.commit()

    # Create a log after adding tire to the stock
    create_log("Added new tire to stock", tire_id, f"Added a tire {tire_id} into location {location_name} {quantity} pieces.")


def move_tires(tire_id, from_location_name, to_location_name, quantity):
    # Fetching locations
    from_location = StockLocations.query.filter_by(name=from_location_name).first()
    to_location = StockLocations.query.filter_by(name=to_location_name).first()

    if not from_location or not to_location:
        return "Invalid source or destination location"

    # Fetching tire stock records for both locations
    from_tire_stock = TireStock.query.filter_by(tire_id=tire_id, location_id=from_location.id).first()
    to_tire_stock = TireStock.query.filter_by(tire_id=tire_id, location_id=to_location.id).first()

    # Check if there's enough quantity in the source location
    if not from_tire_stock or from_tire_stock.quantity < quantity:
        return "Not enough tires in source location"

    # Deduct quantity from source location
    from_tire_stock.quantity -= quantity
    
    # Add to destination location
    if to_tire_stock:
        to_tire_stock.quantity += quantity
    else:
        new_tire_stock = TireStock(tire_id=tire_id, location_id=to_location.id, quantity=quantity)
        db.session.add(new_tire_stock)

    db.session.commit()

    # Create a log after adding moving tire inside stock
    create_log("Moved tire inside stock", tire_id, f"Moved tire {tire_id} from location {from_location_name} into location {to_location_name} {quantity} pieces.")



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
    create_log("Added new stock location to database", new_location.location_id, f"Added a new stock location {location_name}.")

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
    create_log("Updated quantity of tire at location", tire_id, f"Updated quantity of {tire_id} at location {location_name}. New quantity at this location {new_quantity}")

def remove_tire_from_location(tire_id, location_name):
    location = StockLocations.query.filter_by(name=location_name).first()
    if not location:
        return "Invalid location"

    tire_stock = TireStock.query.filter_by(tire_id=tire_id, location_id=location.id).first()
    if not tire_stock:
        return "Tire not found at this location"

    # Fetch the tire details for logging
    tire = Tires.query.get(tire_id)
    if not tire:
        return "Tire details not found for logging"

    db.session.delete(tire_stock)
    
    if not location.is_flexible:
        location.is_occupied = False

    db.session.commit()

    # Create a log after removing tire from stock
    create_log("Removed tire from stock", tire_id, f"Removed {tire_id} from location {location_name}")



def create_log(action_type, tire_id, details=None):
    log = Logs(action_type=action_type, tire_id=tire_id, details=details)
    db.session.add(log)
    db.session.commit()