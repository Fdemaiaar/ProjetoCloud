# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    # Importar modelos
    from .models import User
    
    # Configuração de Logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Carregar variáveis de ambiente
    load_dotenv()

    app = Flask(__name__)

    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    
    

    # Registrar blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
