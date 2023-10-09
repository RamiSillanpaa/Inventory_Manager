from flask import Blueprint, request, render_template, redirect, url_for
from factory import db
from models.logs import Logs

logs_blueprint = Blueprint('/logs', __name__)

# Log view
@logs_blueprint.route('/logs')
def view_logs():
    logs = Logs.query.all()  # Fetch all logs from the database
    return render_template('logs.html', logs=logs)