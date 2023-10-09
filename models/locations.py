from factory import db

class StockLocations(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Unique location name
    is_flexible = db.Column(db.Boolean, default=True)  # By default, it's flexible
    is_occupied = db.Column(db.Boolean, default=False)  # Is this spot occupied?
    
    # Relationships
    tire_id = db.Column(db.Integer, db.ForeignKey('tires.tire_id'), nullable=True)
    tire = db.relationship('Tires', back_populates='stock_location')