from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/raine/Github/Inventory_Manager/instance/inventory.db'

    db.init_app(app)
    
    # You can also register blueprints here, if you're using them.
    
    return app