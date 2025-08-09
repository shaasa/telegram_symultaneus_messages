#!/usr/bin/env python3
"""
Script per migrare il database aggiungendo nuove colonne
"""

import os
import sys
from dotenv import load_dotenv
import pymysql
from sqlalchemy import text

def connect_to_database():
    """Connessione diretta al database MySQL"""
    load_dotenv()

    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'telegram_manager'),
        'charset': 'utf8mb4'
    }

    return pymysql.connect(**config)

def check_column_exists(connection, table, column):
    """Verifica se una colonna esiste in una tabella"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = '{table}' 
                AND COLUMN_NAME = '{column}'
            """)
            result = cursor.fetchone()
            return result[0] > 0
    except Exception as e:
        print(f"Errore nel controllo colonna {table}.{column}: {e}")
        return False

def add_language_code_column(connection):
    """Aggiunge la colonna language_code alla tabella users"""
    try:
        with connection.cursor() as cursor:
            print("📝 Aggiunta colonna language_code alla tabella users...")

            # Aggiungi la colonna
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN language_code VARCHAR(5) DEFAULT 'it' AFTER display_name
            """)

            # Aggiorna tutti gli utenti esistenti con 'it'
            cursor.execute("""
                UPDATE users 
                SET language_code = 'it' 
                WHERE language_code IS NULL
            """)

            connection.commit()
            print("✅ Colonna language_code aggiunta con successo")
            return True

    except Exception as e:
        print(f"❌ Errore nell'aggiunta colonna language_code: {e}")
        connection.rollback()
        return False

def verify_migration(connection):
    """Verifica che la migrazione sia andata a buon fine"""
    try:
        with connection.cursor() as cursor:
            # Controlla struttura tabella users
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()

            print("\n📊 Struttura attuale tabella users:")
            for column in columns:
                field, type_, null, key, default, extra = column
                print(f"  - {field}: {type_} (Default: {default})")

            # Conta utenti con language_code
            cursor.execute("SELECT COUNT(*) FROM users WHERE language_code = 'it'")
            count = cursor.fetchone()[0]
            print(f"\n✅ {count} utenti hanno language_code = 'it'")

            return True

    except Exception as e:
        print(f"❌ Errore nella verifica: {e}")
        return False

def migrate_with_flask():
    """Migrazione usando Flask-SQLAlchemy (alternativa)"""
    try:
        from app import create_app, db
        from sqlalchemy import text

        app = create_app()
        with app.app_context():
            # Verifica se la colonna esiste
            result = db.session.execute(text("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'language_code'
            """)).scalar()

            if result == 0:
                print("📝 Aggiunta colonna language_code con Flask-SQLAlchemy...")

                # Aggiungi colonna
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN language_code VARCHAR(5) DEFAULT 'it' AFTER display_name
                """))

                # Aggiorna utenti esistenti
                db.session.execute(text("""
                    UPDATE users 
                    SET language_code = 'it' 
                    WHERE language_code IS NULL
                """))

                db.session.commit()
                print("✅ Migrazione completata con Flask-SQLAlchemy")
                return True
            else:
                print("ℹ️  Colonna language_code già esistente")
                return True

    except Exception as e:
        print(f"❌ Errore migrazione Flask: {e}")
        return False

def main():
    print("🔄 MIGRAZIONE DATABASE - Telegram Group Manager")
    print("=" * 60)

    # Metodo 1: Prova con connessione diretta MySQL
    try:
        print("Metodo 1: Connessione diretta MySQL...")
        connection = connect_to_database()

        # Verifica se la colonna esiste già
        if check_column_exists(connection, 'users', 'language_code'):
            print("ℹ️  Colonna language_code già esistente")
            verify_migration(connection)
            connection.close()
            return True

        # Esegui migrazione
        success = add_language_code_column(connection)
        if success:
            verify_migration(connection)

        connection.close()
        return success

    except Exception as e:
        print(f"❌ Errore connessione MySQL diretta: {e}")
        print("\nProvo Metodo 2: Flask-SQLAlchemy...")

        # Metodo 2: Usa Flask-SQLAlchemy
        return migrate_with_flask()

if __name__ == '__main__':
    success = main()

    if success:
        print("\n🎉 MIGRAZIONE COMPLETATA!")
        print("\nPuoi ora avviare l'applicazione:")
        print("python run.py")
    else:
        print("\n💥 MIGRAZIONE FALLITA!")
        print("\nSoluzione manuale:")
        print("1. Accedi a MySQL: mysql -u telegram_user -p telegram_manager")
        print("2. Esegui: ALTER TABLE users ADD COLUMN language_code VARCHAR(5) DEFAULT 'it' AFTER display_name;")
        print("3. Esegui: UPDATE users SET language_code = 'it' WHERE language_code IS NULL;")

    sys.exit(0 if success else 1)