from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Carica configurazione basata su ambiente
    config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config.get(config_name, config['default']))

    # Inizializza estensioni
    db.init_app(app)

    # Registra blueprints
    from app.routes.main import main_bp
    from app.routes.groups import groups_bp
    from app.routes.telegram_bot import telegram_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(groups_bp, url_prefix='/groups')
    app.register_blueprint(telegram_bp, url_prefix='/telegram')

    return app