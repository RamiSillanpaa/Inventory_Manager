from flask import Blueprint, request, render_template, redirect, url_for
from factory import db
from models.tires import Tires
from models.locations import StockLocations

move_tire_blueprint = Blueprint('/tires/move', __name__)

# Move tires
@move_tire_blueprint.route('/tires/move', methods=['GET', 'POST'])
def move_tire():
    if request.method == 'POST':
        tire_id = request.form['tire_id']
        destination = request.form['destination']

        tire = Tires.query.get(tire_id)

        if destination == "inside":
            # Find an unoccupied spot in the inside stock
            spot = StockLocations.query.filter_by(stock_type="inside", is_occupied=False).first()
            if spot:
                # Update the tire's location to this spot
                tire.location = spot.id
                # Mark the spot as occupied
                spot.is_occupied = True
            else:
                return "No available spot in inside stock.", 400

        elif destination == "outside":
            # Record the tire's general location in outside stock
            shelf = request.form.get('shelf')
            column = request.form.get('column')
            row = request.form.get('row')
            
            # Store these details for the tire's location
            tire.location = None  # or however you want to denote it's in the outside stock
            tire.shelf = shelf
            tire.column = column
            tire.row = row

        # Save changes to the database
        db.session.commit()

        return redirect(url_for('dashboard'))

    tires = Tires.query.all()  # Fetch all tires to display in a dropdown for the user to select
    return render_template('move_tire.html', tires=tires)