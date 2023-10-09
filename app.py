from flask import render_template, request, redirect, url_for
from factory import create_app, db

app = create_app()

from models.tires import Tires
from models.tire_stock import TireStock
from models.logs import Logs
from models.locations import StockLocations
from services.crud_operations import add_tire, add_tire_to_stock, get_tires_from_location, update_tire_quantity_at_location, remove_tire_from_location

from views.add_new_tire_route import add_tire_blueprint
from views.dashboard_route import dashboard_blueprint
from views.logs_route import logs_blueprint
from views.move_tire_route import move_tire_blueprint
from views.stock_locations_add_route import add_stock_location_blueprint
from views.stock_locations_route import list_stock_locations_blueprint
from views.tires_route import list_tires_blueprint

# Register the blueprints
app.register_blueprint(add_tire_blueprint)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(logs_blueprint)
app.register_blueprint(move_tire_blueprint)
app.register_blueprint(add_stock_location_blueprint)
app.register_blueprint(list_stock_locations_blueprint)
app.register_blueprint(list_tires_blueprint)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def test_route():
    return "This is a test route"

if __name__ == "__main__":
    app.run(debug=True)
