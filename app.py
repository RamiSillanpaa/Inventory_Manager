from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Tires, StockLocations, TireStock, Logs  # Move this import after `db` is defined

@app.route('/')
def hello_world():
    return 'Hello, World!'
