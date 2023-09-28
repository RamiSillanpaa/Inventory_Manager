#Ensure that models.py only contains database models and related functions or classes.
from app import db

class Tires(db.Model):
    tire_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

class StockLocations(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    stock_type = db.Column(db.String(10), nullable=False)  # Either 'inside' or 'outside'
    shelf = db.Column(db.String(20), nullable=False)
    column = db.Column(db.String(20), nullable=False)
    row = db.Column(db.String(20), nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)

class TireStock(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    tire_id = db.Column(db.Integer, db.ForeignKey('tires.tire_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('stock_locations.location_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Logs(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    tire_id = db.Column(db.Integer, db.ForeignKey('tires.tire_id'), nullable=False)
    details = db.Column(db.String(200))
