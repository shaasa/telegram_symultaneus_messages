#!/usr/bin/env python3
"""
Script per il setup iniziale del database MySQL
Esegui questo script dopo aver configurato MySQL e il file .env
"""

import os
import sys
from dotenv import load_dotenv
import pymysql

def create_user_and_database():
    """Crea utente e database se non esistono"""
    load_dotenv()

    # Parametri di connessione
    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', 3306))
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'telegram_manager')

    print(f"Connessione a MySQL su {host}:{port}")
    print(f"Utente app: {user}")
    print(f"Database da creare: {database}")

    # Prima prova con l'utente specificato
    try:
        print(f"\n1. Tentativo connessione con utente '{user}'...")
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4'
        )

        with connection.cursor() as cursor:
            # Verifica se il database esiste
            cursor.execute(f"SHOW DATABASES LIKE '{database}'")
            exists = cursor.fetchone()

            if exists:
                print(f"✓ Database '{database}' esiste già")
            else:
                # Crea il database
                cursor.execute(f"CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✓ Database '{database}' creato con successo")

        connection.close()
        return True

    except pymysql.Error as e:
        if e.args[0] == 1045:  # Access denied
            print(f"✗ Accesso negato per utente '{user}'")
            print("Provo a creare l'utente con root...")
            return create_user_with_root(host, port, user, password, database)
        elif e.args[0] == 1141:  # No such grant
            print(f"✗ Grant non definiti per '{user}'")
            print("Provo a creare l'utente con root...")
            return create_user_with_root(host, port, user, password, database)
        else:
            print(f"✗ Errore MySQL: {e}")
            return False

def create_user_with_root(host, port, app_user, app_password, database):
    """Crea utente e database usando account root"""

    # Chiedi credenziali root
    print(f"\nPer creare l'utente '{app_user}' serve l'accesso root a MySQL")
    root_password = input("Inserisci password root MySQL (Enter se vuota): ")

    try:
        print("Connessione come root...")
        root_connection = pymysql.connect(
            host=host,
            port=port,
            user='root',
            password=root_password,
            charset='utf8mb4'
        )

        with root_connection.cursor() as cursor:
            # Verifica se l'utente esiste
            cursor.execute(f"SELECT User FROM mysql.user WHERE User = '{app_user}' AND Host = 'localhost'")
            user_exists = cursor.fetchone()

            if not user_exists:
                print(f"Creazione utente '{app_user}'...")
                cursor.execute(f"CREATE USER '{app_user}'@'localhost' IDENTIFIED BY '{app_password}'")
                print(f"✓ Utente '{app_user}' creato")
            else:
                print(f"✓ Utente '{app_user}' esiste già")

            # Verifica se il database esiste
            cursor.execute(f"SHOW DATABASES LIKE '{database}'")
            db_exists = cursor.fetchone()

            if not db_exists:
                print(f"Creazione database '{database}'...")
                cursor.execute(f"CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✓ Database '{database}' creato")
            else:
                print(f"✓ Database '{database}' esiste già")

            # Concedi permessi
            print(f"Configurazione permessi per '{app_user}'...")
            cursor.execute(f"GRANT ALL PRIVILEGES ON {database}.* TO '{app_user}'@'localhost'")
            cursor.execute("FLUSH PRIVILEGES")
            print(f"✓ Permessi concessi")

        root_connection.close()

        # Test connessione con nuovo utente
        print(f"\nTest connessione con '{app_user}'...")
        test_connection = pymysql.connect(
            host=host,
            port=port,
            user=app_user,
            password=app_password,
            database=database,
            charset='utf8mb4'
        )
        test_connection.close()
        print(f"✓ Connessione con '{app_user}' riuscita")

        return True

    except pymysql.Error as e:
        print(f"✗ Errore durante setup con root: {e}")
        print("\nSoluzioni alternative:")
        print("1. Verifica che MySQL sia avviato")
        print("2. Controlla password root")
        print("3. Crea manualmente utente e database:")
        print(f"   mysql -u root -p")
        print(f"   CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"   CREATE USER '{app_user}'@'localhost' IDENTIFIED BY '{app_password}';")
        print(f"   GRANT ALL PRIVILEGES ON {database}.* TO '{app_user}'@'localhost';")
        print(f"   FLUSH PRIVILEGES;")
        return False

def create_tables():
    """Crea le tabelle usando Flask-SQLAlchemy"""
    print("\nCreazione tabelle...")

    try:
        from app import create_app, db

        app = create_app()
        with app.app_context():
            # Crea tutte le tabelle
            db.create_all()
            print("✓ Tabelle create con successo")

            # Verifica tabelle create
            from sqlalchemy import text
            result = db.session.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]

            print(f"✓ Tabelle trovate: {', '.join(tables)}")

            # Verifica struttura tabelle principali
            expected_tables = ['users', 'groups', 'group_users', 'message_logs']
            missing_tables = [t for t in expected_tables if t not in tables]

            if missing_tables:
                print(f"⚠ Tabelle mancanti: {', '.join(missing_tables)}")
            else:
                print("✓ Tutte le tabelle principali sono presenti")

        return True

    except Exception as e:
        print(f"✗ Errore nella creazione tabelle: {e}")
        print("\nDettagli errore:")
        import traceback
        traceback.print_exc()
        return False

def test_connection():
    """Testa la connessione completa"""
    print("\nTest connessione completa...")

    try:
        from app import create_app, db
        from app.models import User, Group, MessageLog

        app = create_app()
        with app.app_context():
            # Test query semplice
            user_count = User.query.count()
            group_count = Group.query.count()
            log_count = MessageLog.query.count()

            print(f"✓ Connessione database OK")
            print(f"  - Utenti: {user_count}")
            print(f"  - Gruppi: {group_count}")
            print(f"  - Log messaggi: {log_count}")

        return True

    except Exception as e:
        print(f"✗ Errore test connessione: {e}")
        return False

def verify_mysql_service():
    """Verifica che MySQL sia avviato"""
    import subprocess

    try:
        # Linux/Mac
        result = subprocess.run(['systemctl', 'is-active', 'mysql'],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Servizio MySQL attivo")
            return True
    except:
        pass

    try:
        # Alternativa: prova connessione diretta
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('localhost', 3306))
        sock.close()

        if result == 0:
            print("✓ MySQL risponde sulla porta 3306")
            return True
        else:
            print("✗ MySQL non risponde sulla porta 3306")
            return False
    except:
        print("⚠ Impossibile verificare stato MySQL")
        return True  # Procedi comunque

def main():
    print("=== Setup Database Telegram Group Manager ===\n")

    # Verifica file .env
    if not os.path.exists('.env'):
        print("✗ File .env non trovato!")
        print("Crea il file .env con le configurazioni del database")
        return False

    # Verifica variabili ambiente
    load_dotenv()
    required_vars = ['DB_HOST', 'DB_USER', 'DB_NAME']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"✗ Variabili ambiente mancanti: {', '.join(missing_vars)}")
        print("Configura il file .env con:")
        for var in missing_vars:
            print(f"  {var}=...")
        return False

    print("✓ Configurazione ambiente OK")

    # Verifica MySQL
    verify_mysql_service()

    # Step 1: Crea utente e database
    if not create_user_and_database():
        print("\n✗ Setup fallito nella creazione database/utente")
        return False

    # Step 2: Crea tabelle
    if not create_tables():
        print("\n✗ Setup fallito nella creazione tabelle")
        return False

    # Step 3: Test finale
    if not test_connection():
        print("\n✗ Setup fallito nel test finale")
        return False

    print("\n🎉 Setup database completato con successo!")
    print("\nPuoi ora avviare l'applicazione con: python run.py")

    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)