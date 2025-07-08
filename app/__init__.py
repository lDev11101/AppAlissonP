from flask import Flask
from app.routes import register_blueprints
from config import DevelopmentConfig
from app.db.conexion import close_db
from flask_cors import CORS


def crear_aplicacion():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(DevelopmentConfig)

    app.teardown_appcontext(close_db)

    register_blueprints(app)
    return app
