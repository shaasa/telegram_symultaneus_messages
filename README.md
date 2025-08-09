# Telegram Group Manager

Un'applicazione web per gestire gruppi di utenti e inviare messaggi personalizzati tramite bot Telegram.

## Funzionalità

- **Gestione Gruppi**: Crea e gestisci gruppi di utenti
- **Messaggi Personalizzati**: Invia messaggi diversi a ogni utente del gruppo
- **Importazione Utenti**: Importa automaticamente utenti che hanno interagito con il bot
- **Interfaccia Web**: Dashboard moderna e responsive con Bootstrap
- **Database Locale**: Utilizza SQLite per memorizzare dati localmente

## Struttura del Progetto

```
telegram-group-manager/
├── app/
│   ├── __init__.py              # Inizializzazione app Flask
│   ├── models.py                # Modelli database (Group, User, MessageLog)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py              # Route homepage e dashboard
│   │   ├── groups.py            # Route gestione gruppi
│   │   └── telegram_bot.py      # Route operazioni bot Telegram
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css       # Stili personalizzati
│   │   └── js/
│   │       └── main.js          # JavaScript personalizzato
│   ├── templates/
│   │   ├── base.html            # Template base
│   │   ├── index.html           # Homepage/Dashboard
│   │   ├── groups.html          # Lista gruppi
│   │   └── group_detail.html    # Dettaglio gruppo e invio messaggi
│   └── utils/
│       ├── __init__.py
│       └── telegram_helper.py   # Funzioni helper per API Telegram
├── instance/
│   └── database.db              # Database SQLite (generato automaticamente)
├── .env                         # Variabili d'ambiente (TOKEN BOT)
├── .gitignore                   # File da ignorare in Git
├── config.py                    # Configurazione applicazione
├── requirements.txt             # Dipendenze Python
├── run.py                       # Entry point applicazione
└── README.md                    # Questo file
```

## Installazione

### Prerequisiti

- Python 3.8 o superiore
- MySQL 5.7 o superiore (o MariaDB 10.2+)
- Bot Telegram creato tramite @BotFather
- Token del bot Telegram

### Setup Database MySQL

1. **Installa MySQL**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install mysql-server
   
   # macOS con Homebrew
   brew install mysql
   
   # Windows: Scarica da https://dev.mysql.com/downloads/mysql/
   ```

2. **Configura MySQL**
   ```bash
   # Accedi a MySQL
   sudo mysql -u root -p
   
   # Crea utente dedicato (raccomandato)
   CREATE USER 'telegram_user'@'localhost' IDENTIFIED BY 'strong_password';
   
   # Concedi permessi
   GRANT ALL PRIVILEGES ON telegram_manager.* TO 'telegram_user'@'localhost';
   FLUSH PRIVILEGES;
   
   # Esci
   EXIT;
   ```

### Setup Applicazione

1. **Clona o scarica il progetto**
   ```bash
   cd telegram-group-manager
   ```

2. **Crea ambiente virtuale** (raccomandato)
   ```bash
   python -m venv venv
   
   # Su Linux/Mac
   source venv/bin/activate
   
   # Su Windows
   venv\Scripts\activate
   ```

3. **Installa dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura variabili d'ambiente**

   Modifica il file `.env` con i tuoi dati:
   ```env
   # Bot Telegram
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   
   # Database MySQL
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=telegram_manager
   DB_USER=telegram_user
   DB_PASSWORD=strong_password
   
   # Sicurezza
   SECRET_KEY=your_very_long_random_secret_key_here
   
   # Ambiente
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

5. **Setup database**
   ```bash
   # Esegui script automatico di setup
   python setup_database.py
   
   # Oppure manualmente:
   # 1. Crea database: CREATE DATABASE telegram_manager;
   # 2. Avvia app: python run.py (creerà le tabelle automaticamente)
   ```

6. **Avvia l'applicazione**
   ```bash
   python run.py
   ```

7. **Accedi all'applicazione**

   Apri il browser e vai su: `http://127.0.0.1:5000`

## Configurazione Bot Telegram

### Creazione Bot

1. Apri Telegram e cerca `@BotFather`
2. Invia `/newbot` e segui le istruzioni
3. Ottieni il token del bot (formato: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
4. Inserisci il token nel file `.env`

### Preparazione Bot per Importazione Utenti

Per importare utenti dal bot, gli utenti devono aver interagito almeno una volta con il bot. Puoi:

1. **Condividere il bot** con i tuoi utenti
2. **Impostare comandi base** nel bot tramite @BotFather:
   ```
   /setcommands
   start - Inizia conversazione
   help - Mostra aiuto
   ```

3. **Chiedere agli utenti** di inviare `/start` al bot

## Utilizzo

### 1. Dashboard
- Visualizza statistiche generali
- Azioni rapide per creare gruppi e importare utenti
- Lista gruppi recenti

### 2. Gestione Gruppi
- **Crea Gruppo**: Nome e descrizione opzionale
- **Aggiungi Utenti**: Seleziona da lista utenti disponibili
- **Rimuovi Utenti**: Rimuovi utenti dal gruppo

### 3. Invio Messaggi
- **Messaggi Personalizzati**: Scrivi messaggio diverso per ogni utente
- **Messaggio Globale**: Compila tutti i campi con lo stesso messaggio
- **Anteprima**: Vedi utenti e messaggi prima dell'invio
- **Log**: Tracciamento messaggi inviati/falliti

### 4. Importazione Utenti
- **Automatica**: Importa utenti che hanno scritto al bot
- **Manuale**: Aggiungi utenti inserendo ID Telegram
- **Aggiornamento**: Aggiorna dati utenti esistenti

## Struttura Database

### Configurazione MySQL

Il progetto utilizza MySQL come database principale per garantire:
- **Persistenza**: Dati sicuri e permanenti
- **Performance**: Gestione efficiente di molti utenti e gruppi
- **Relazioni**: Struttura relazionale ottimizzata
- **Backup**: Facilità di backup e restore

### Tabelle Principali

**groups**
- `id`: ID primario
- `name`: Nome gruppo (univoco, max 100 char)
- `description`: Descrizione opzionale (TEXT)
- `created_at`: Data creazione (DATETIME)
- `updated_at`: Ultimo aggiornamento (DATETIME)

**users**
- `id`: ID primario
- `telegram_id`: ID Telegram utente (VARCHAR(20), univoco, indicizzato)
- `username`: Username Telegram (VARCHAR(100), indicizzato)
- `first_name`, `last_name`: Nome e cognome (VARCHAR(100))
- `display_name`: Nome di visualizzazione (VARCHAR(200))
- `is_active`: Stato attivo (BOOLEAN)
- `created_at`: Data creazione (DATETIME)
- `updated_at`: Ultimo aggiornamento (DATETIME)
- `last_interaction`: Ultima interazione con bot (DATETIME)

**message_logs**
- `id`: ID primario
- `group_id`: Riferimento al gruppo (FK, indicizzato)
- `user_id`: Riferimento all'utente (FK, indicizzato)
- `message_text`: Testo messaggio (TEXT)
- `sent_at`: Data/ora invio (DATETIME)
- `status`: Stato (VARCHAR(20): pending, sent, failed, indicizzato)
- `error_message`: Messaggio errore se fallito (TEXT)
- `telegram_message_id`: ID messaggio Telegram (VARCHAR(50))

**group_users** (Tabella associazione)
- `group_id`: FK verso groups
- `user_id`: FK verso users
- Chiave primaria composta (group_id, user_id)

### Relazioni e Indici

- **Group ↔ User**: Many-to-Many via group_users
- **MessageLog**: Collegato a Group e User con FK
- **Indici**: Su telegram_id, username, status, group_id, user_id per performance
- **Charset**: utf8mb4 per supporto emoji e caratteri unicode

### Configurazioni Performance

```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,        # Test connessione prima dell'uso
    'pool_recycle': 3600,         # Ricicla connessioni ogni ora
    'pool_size': 10,              # Pool di 10 connessioni
    'max_overflow': 20,           # Max 20 connessioni extra
    'connect_args': {
        'charset': 'utf8mb4',     # Supporto Unicode completo
        'use_unicode': True
    }
}
``` ID primario
- `telegram_id`: ID Telegram utente
- `username`: Username Telegram
- `first_name`, `last_name`: Nome e cognome
- `display_name`: Nome di visualizzazione
- `is_active`: Stato attivo
- `last_interaction`: Ultima interazione con bot

**MessageLog**
- `id`: ID primario
- `group_id`: Riferimento al gruppo
- `user_id`: Riferimento all'utente
- `message_text`: Testo messaggio
- `sent_at`: Data/ora invio
- `status`: Stato (pending, sent, failed)
- `error_message`: Messaggio errore se fallito

### Relazioni
- **Group ↔ User**: Many-to-Many (un utente può essere in più gruppi)
- **MessageLog**: Collegato a Group e User

## API Endpoints

### Main Routes
- `GET /` - Dashboard principale
- `GET /dashboard` - Redirect a dashboard

### Groups Routes
- `GET /groups/` - Lista tutti i gruppi
- `POST /groups/create` - Crea nuovo gruppo
- `GET /groups/<id>` - Dettaglio gruppo
- `POST /groups/<id>/add_user` - Aggiungi utente a gruppo
- `POST /groups/<id>/remove_user/<user_id>` - Rimuovi utente da gruppo
- `POST /groups/<id>/send_messages` - Invia messaggi a gruppo
- `POST /groups/<id>/delete` - Elimina gruppo

### Telegram Routes
- `POST /telegram/import_users` - Importa utenti dal bot
- `POST /telegram/create_user` - Crea utente manuale
- `GET /telegram/users` - API lista utenti
- `GET /telegram/test_connection` - Testa connessione bot

## Funzionalità Avanzate

### Auto-save
- I messaggi vengono salvati automaticamente nel browser
- Recupero automatico in caso di chiusura accidentale
- Pulizia automatica dopo invio riuscito

### Validazione
- Controllo token bot Telegram
- Validazione form lato client e server
- Gestione errori con messaggi informativi

### Responsive Design
- Interfaccia ottimizzata per desktop e mobile
- Bootstrap 5 per layout responsive
- CSS personalizzato per miglior UX

### Sicurezza
- Configurazione separata per sviluppo/produzione
- Gestione errori senza esposizione dati sensibili
- Validazione input per prevenire XSS

## Risoluzione Problemi

### Errori Comuni

**"Token bot non configurato"**
- Verifica che il token sia corretto nel file `.env`
- Assicurati che il file `.env` sia nella directory principale

**"Errore connessione bot"**
- Controlla la connessione internet
- Verifica che il token sia valido su @BotFather
- Testa manualmente: `https://api.telegram.org/bot<TOKEN>/getMe`

**"Nessun utente importato"**
- Gli utenti devono aver interagito con il bot almeno una volta
- Verifica che il bot non sia bloccato dagli utenti
- Controlla che il bot abbia permessi di lettura messaggi

### Risoluzione Problemi

#### Errori Database MySQL

**"Can't connect to MySQL server"**
- Verifica che MySQL sia avviato: `sudo systemctl status mysql`
- Controlla host e porta nel file `.env`
- Testa connessione: `mysql -h localhost -u telegram_user -p`

**"Access denied for user"**
- Verifica username e password nel file `.env`
- Controlla permessi utente MySQL:
  ```sql
  SHOW GRANTS FOR 'telegram_user'@'localhost';
  ```
- Ricrea utente se necessario

**"Unknown database 'telegram_manager'"**
- Esegui `python setup_database.py` per creare il database
- Oppure crea manualmente:
  ```sql
  CREATE DATABASE telegram_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```

**"Table doesn't exist"**
- Le tabelle vengono create automaticamente al primo avvio
- Forza creazione:
  ```python
  from app import create_app, db
  app = create_app()
  with app.app_context():
      db.create_all()
  ```

**Errori charset/encoding**
- Assicurati che il database usi `utf8mb4`
- Verifica: `SHOW CREATE DATABASE telegram_manager;`
- Ricrea con charset corretto se necessario

#### Errori Telegram Bot

**"Token bot non configurato"**
- Verifica che il token sia corretto nel file `.env`
- Assicurati che il file `.env` sia nella directory principale

**"Errore connessione bot"**
- Controlla la connessione internet
- Verifica che il token sia valido su @BotFather
- Testa manualmente: `https://api.telegram.org/bot<TOKEN>/getMe`

**"Nessun utente importato"**
- Gli utenti devono aver interagito con il bot almeno una volta
- Verifica che il bot non sia bloccato dagli utenti
- Controlla che il bot abbia permessi di lettura messaggi

**"Errore invio messaggio"**
- L'utente potrebbe aver bloccato il bot
- Verifica che l'ID Telegram sia corretto
- Controlla rate limits API Telegram (30 msg/sec)

### Backup e Restore

#### Backup Database

```bash
# Backup completo
mysqldump -u telegram_user -p telegram_manager > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup solo dati (senza struttura)
mysqldump -u telegram_user -p --no-create-info telegram_manager > data_backup.sql

# Backup compresso
mysqldump -u telegram_user -p telegram_manager | gzip > backup.sql.gz
```

#### Restore Database

```bash
# Restore completo
mysql -u telegram_user -p telegram_manager < backup_20250809_143000.sql

# Restore da file compresso
gunzip < backup.sql.gz | mysql -u telegram_user -p telegram_manager
```

#### Backup Automatico (Cron)

```bash
# Aggiungi a crontab (crontab -e)
# Backup giornaliero alle 2:00
0 2 * * * /usr/bin/mysqldump -u telegram_user -p'password' telegram_manager > /backups/telegram_$(date +\%Y\%m\%d).sql
```

### Performance e Ottimizzazione

#### Configurazioni MySQL Consigliate

```sql
-- my.cnf o my.ini
[mysqld]
innodb_buffer_pool_size = 256M
innodb_log_file_size = 64M
max_connections = 200
query_cache_size = 64M
tmp_table_size = 64M
max_heap_table_size = 64M
```

#### Monitoraggio Performance

```sql
-- Query lente
SHOW PROCESSLIST;

-- Statistiche tabelle
SELECT table_name, table_rows, data_length, index_length 
FROM information_schema.tables 
WHERE table_schema = 'telegram_manager';

-- Indici utilizzati
SHOW INDEX FROM users;
SHOW INDEX FROM groups;
SHOW INDEX FROM message_logs;
```

### Migrazione da SQLite (se necessario)

Se hai dati esistenti in SQLite:

```python
# Script di migrazione
import sqlite3
import pymysql
from app import create_app, db
from app.models import User, Group, MessageLog

def migrate_from_sqlite():
    # Connetti a SQLite
    sqlite_conn = sqlite3.connect('instance/database.db')
    sqlite_conn.row_factory = sqlite3.Row
    
    # Connetti a MySQL via Flask
    app = create_app()
    with app.app_context():
        # Migra utenti
        sqlite_users = sqlite_conn.execute('SELECT * FROM user').fetchall()
        for row in sqlite_users:
            user = User(
                telegram_id=row['telegram_id'],
                username=row['username'],
                first_name=row['first_name'],
                # ... altri campi
            )
            db.session.add(user)
        
        # Migra gruppi e messaggi...
        db.session.commit()
```

### Sicurezza

#### Configurazioni Produzione

```python
# config.py - ProductionConfig
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # SSL/TLS per MySQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'sslmode': 'require',
            'sslcert': '/path/to/client-cert.pem',
            'sslkey': '/path/to/client-key.pem',
            'sslrootcert': '/path/to/ca-cert.pem'
        }
    }
```

#### Permessi MySQL Minimi

```sql
-- Crea utente con permessi limitati per produzione
CREATE USER 'telegram_app'@'%' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON telegram_manager.* TO 'telegram_app'@'%';
FLUSH PRIVILEGES;
```

### Monitoring e Logging

#### Log Applicazione

```python
# Aggiungi a config.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/telegram_app.log', 
                                     maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

#### Monitoring MySQL

```bash
# Tool per monitorare MySQL
sudo apt install mytop
mytop -u telegram_user -p

# Log query lente
# Aggiungi a my.cnf:
# slow_query_log = 1
# slow_query_log_file = /var/log/mysql/slow.log
# long_query_time = 2
```

### Scalabilità

Per applicazioni con molti utenti considera:

#### Database Replication

```sql
-- Master-Slave setup per read scaling
-- Master per scritture, Slave per letture
```

#### Connection Pooling

```python
# Configurazione pool avanzata
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 20,
    'max_overflow': 50,
    'pool_pre_ping': True,
    'pool_recycle': 3600,
}
```

#### Caching

```python
# Redis per cache sessioni
pip install redis flask-caching

# config.py
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = 'redis://localhost:6379/0'
```

---

**Versione**: 1.0.0  
**Database**: MySQL 5.7+ / MariaDB 10.2+  
**Ultimo aggiornamento**: Agosto 2025  
**Compatibilità**: Python 3.8+, Flask 2.3+, Bootstrap 5