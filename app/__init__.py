from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask import session, request
from dotenv import load_dotenv
import os

# Carica le variabili dal file .env
load_dotenv()

# Inizializzazione delle estensioni
db = SQLAlchemy()
babel = Babel()

def get_locale():
    """Funzione per determinare la lingua corrente"""
    # Se c'è una lingua nella sessione, usala
    if 'language' in session:
        return session['language']
    # Altrimenti usa quella di default
    return 'it'

def create_app():
    app = Flask(__name__)

    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    print(f"DEBUG: Token da .env = {bool(token)} (lunghezza: {len(token) if token else 0})")
    if token:
        print(f"DEBUG: Token preview = {token[:10]}...{token[-4:]}")
    # La tua configurazione originale - MySQL con le tue variabili .env
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Costruisci URL database dalle tue variabili .env
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configurazione Babel originale
    app.config['LANGUAGES'] = {
        'it': 'Italiano',
        'en': 'English',
        'fr': 'Français',
        'de': 'Deutsch',
        'es': 'Español'
    }
    app.config['BABEL_DEFAULT_LOCALE'] = 'it'
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

    # Inizializzazione estensioni
    db.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    # Rendi get_locale disponibile nei template
    @app.context_processor
    def inject_conf_vars():
        return {
            'get_locale': get_locale,
            'LANGUAGES': app.config.get('LANGUAGES', {})
        }

    # I tuoi blueprint originali
    from app.routes.main import main_bp
    from app.routes.telegram_bot import telegram_bp
    from app.routes.i18n import i18n_bp
    from app.routes.groups import groups_bp  # Questo era quello mancante!

    app.register_blueprint(main_bp)
    app.register_blueprint(telegram_bp, url_prefix='/telegram')
    app.register_blueprint(i18n_bp, url_prefix='/i18n')
    app.register_blueprint(groups_bp, url_prefix='/groups')

    # Creazione tabelle database
    with app.app_context():
        db.create_all()

    return app