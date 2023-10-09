from factory import db

class Tires(db.Model):
    tire_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    stock_location = db.relationship('StockLocations', back_populates='tire')