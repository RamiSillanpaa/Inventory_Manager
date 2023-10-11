from flask import Blueprint, request, render_template, redirect, url_for
from factory import db
from models.tires import Tires
from models.locations import StockLocations
from models.tire_stock import TireStock
from services.crud_operations import add_tire_to_stock, remove_tire_from_location

move_tire_blueprint = Blueprint('move_tire', __name__, url_prefix='/tires')

# Move tires
@move_tire_blueprint.route('/move', methods=['GET', 'POST'])
def move_tire():
    if request.method == 'POST':
        tire_id = request.form['tire_id']
        new_location_name = request.form['destination']
        
        # Check if the tire is already at a location
        current_location = TireStock.query.filter_by(tire_id=tire_id).first()
        
        if current_location:
            # Remove tire from current location
            remove_tire_from_location(tire_id, current_location.location_id)
        
        # Add tire to the new location
        add_tire_to_stock(tire_id, new_location_name, 1)  # Assuming 1 as quantity. Modify if needed.

        return redirect(url_for('dashboard.dashboard'))

    tires = Tires.query.all()  # Fetch all tires to display in a dropdown for the user to select
    locations = StockLocations.query.all()  # Fetch all locations to show as destinations
    return render_template('move_tire.html', tires=tires, locations=locations)
