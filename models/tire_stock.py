from factory import db

class TireStock(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    tire_id = db.Column(db.Integer, db.ForeignKey('tires.tire_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('stock_locations.location_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)