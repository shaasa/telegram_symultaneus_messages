from app import create_app, db
from app.models import Group, User

app = create_app()

def create_tables():
    """Crea le tabelle del database se non esistono"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")

if __name__ == '__main__':
    # Crea le tabelle al primo avvio
    create_tables()

    # Avvia l'applicazione
    app.run(host='127.0.0.1', port=5000, debug=True)