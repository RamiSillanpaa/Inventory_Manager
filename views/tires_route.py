from flask import Blueprint, request, render_template, redirect, url_for
from factory import db
from models.tires import Tires

list_tires_blueprint = Blueprint('/tires', __name__)

# List all tires 
@list_tires_blueprint.route('/tires', methods=['GET'])
def list_tires():
    tires = Tires.query.all()
    return render_template('list_tires.html', tires=tires)