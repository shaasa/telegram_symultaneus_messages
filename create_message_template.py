#!/usr/bin/env python3
"""
Script standalone per creare solo le tabelle dei template
NON importa l'app Flask per evitare problemi di import
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()

def create_template_tables():
    """Crea le tabelle dei template direttamente con MySQL"""
    try:
        # Connetti al database usando le tue variabili .env
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            port=int(os.environ.get('DB_PORT')),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )

        cursor = connection.cursor()

        # SQL per creare la tabella dei template
        template_sql = """
        CREATE TABLE IF NOT EXISTS message_templates (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            description TEXT,
            group_id INT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            INDEX ix_message_templates_group_id (group_id),
            FOREIGN KEY (group_id) REFERENCES `groups` (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """

        # SQL per creare la tabella dei messaggi del template
        template_messages_sql = """
        CREATE TABLE IF NOT EXISTS template_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            template_id INT NOT NULL,
            user_id INT NOT NULL,
            message_text TEXT NOT NULL,
            order_index INT DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX ix_template_messages_template_id (template_id),
            INDEX ix_template_messages_user_id (user_id),
            FOREIGN KEY (template_id) REFERENCES message_templates (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """

        # Esegui le query
        print("🚀 Creazione tabella message_templates...")
        cursor.execute(template_sql)
        print("✅ Tabella message_templates creata!")

        print("🚀 Creazione tabella template_messages...")
        cursor.execute(template_messages_sql)
        print("✅ Tabella template_messages creata!")

        # Verifica che le tabelle siano state create
        cursor.execute("SHOW TABLES LIKE 'message_templates'")
        if cursor.fetchone():
            print("✅ Verifica: tabella 'message_templates' esistente")

        cursor.execute("SHOW TABLES LIKE 'template_messages'")
        if cursor.fetchone():
            print("✅ Verifica: tabella 'template_messages' esistente")

        connection.commit()
        print("🎉 Migrazione completata con successo!")

        return True

    except mysql.connector.Error as e:
        print(f"❌ Errore MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Errore generico: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Connessione database chiusa")

if __name__ == '__main__':
    print("🚀 Creazione tabelle per i template di messaggi...")
    print("📋 La tabella message_logs esiste già e non sarà modificata")

    if create_template_tables():
        print("\n🎉 Migrazione completata!")
        print("📝 Ora puoi aggiungere i modelli MessageTemplate e TemplateMessage al file models.py")
    else:
        print("\n💥 Migrazione fallita!")