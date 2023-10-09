from flask import Blueprint, request, render_template, redirect, url_for
from factory import db
from models.tires import Tires

add_tire_blueprint = Blueprint('add_tire', __name__, url_prefix='/tires')

# Add new tire
@add_tire_blueprint.route('/add', methods=['GET', 'POST'])
def add_tire_route():
    if request.method == 'POST':
        tire_type=request.form['type'],
        tire_brand=request.form['brand'],
        tire_size=request.form['size']
        
        add_tire(tire_type, tire_brand, tire_size)

        return redirect(url_for('list_tires'))
    return render_template('add_tire.html')