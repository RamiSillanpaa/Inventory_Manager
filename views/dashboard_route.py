from flask import Blueprint, render_template
from factory import db
from models.tires import Tires
from models.locations import StockLocations

dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route('/dashboard', methods=['GET'])
def dashboard():
    total_tires = Tires.query.count()
    return render_template('dashboard.html', total=total_tires)
