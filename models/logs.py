from factory import db

class Logs(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    tire_id = db.Column(db.Integer, db.ForeignKey('tires.tire_id'), nullable=False)
    details = db.Column(db.String(200))