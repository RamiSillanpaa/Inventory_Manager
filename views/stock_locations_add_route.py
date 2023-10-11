from flask import Blueprint, request, render_template, redirect, url_for
from factory import db
from models.locations import StockLocations
from services.crud_operations import add_location

add_stock_location_blueprint = Blueprint('add', __name__, url_prefix='/stock-locations')

# Add a new stock location
@add_stock_location_blueprint.route('/add', methods=['GET', 'POST'])
def add_stock_location():
    if request.method == 'POST':
        stock_type=request.form['location_name']

        add_location(stock_type)

        return redirect(url_for('stock-locations.list_stock_locations'))
    return render_template('add_stock_location.html')