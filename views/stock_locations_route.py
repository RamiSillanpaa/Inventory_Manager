from flask import Blueprint, request, render_template, redirect, url_for
from factory import db
from models.locations import StockLocations

list_stock_locations_blueprint = Blueprint('/stock-locations', __name__)

# List all stock locations
@list_stock_locations_blueprint.route('/stock-locations', methods=['GET'])
def list_stock_locations():
    locations = StockLocations.query.all()
    return render_template('list_stock_locations.html', locations=locations)