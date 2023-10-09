from flask import Blueprint, request, render_template, redirect, url_for
from factory import db
from models.locations import StockLocations

add_stock_location_blueprint = Blueprint('/stock-locations/add', __name__)

# Add a new stock location
@add_stock_location_blueprint.route('/stock-locations/add', methods=['GET', 'POST'])
def add_stock_location():
    if request.method == 'POST':
        new_location = StockLocations(
            stock_type=request.form['stock_type'],
            shelf=request.form['shelf'],
            column=request.form['column'],
            row=request.form['row']
        )
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('list_stock_locations'))
    return render_template('add_stock_location.html')