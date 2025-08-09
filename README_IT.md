# Telegram Group Manager

## Premessa del Progetto

Questo progetto nasce per una mia esigenza di Dungeon Master di D&D per inviare simultaneamente messaggi ai miei giocatori, preparati precedentemente, ed è stato anche il mio primo esperimento di sviluppo di un intero software generato con l'AI Claude 4. Sono andata per tentativi ma sono soddisfatta del lavoro fin qui svolto, anche se ha ancora ampi margini di miglioramento.

Il software è completamente **AI-generated** e rappresenta un esempio di come l'intelligenza artificiale possa trasformare un'idea specifica in un'applicazione web completa e funzionale.

---

Un'applicazione web avanzata per gestire gruppi di utenti e inviare messaggi personalizzati tramite bot Telegram con supporto per template e cronologia dettagliata.

## Funzionalità Principali

### Core Features
- **Gestione Gruppi**: Crea e gestisci gruppi di utenti con interfaccia intuitiva
- **Messaggi Personalizzati**: Invia messaggi diversi a ogni utente del gruppo
- **Template Messaggi**: Prepara e salva liste di messaggi per uso futuro
- **Cronologia Avanzata**: Visualizza messaggi inviati con filtri e statistiche
- **Importazione Utenti**: Importa automaticamente utenti che hanno interagito con il bot
- **Interfaccia Multilingua**: Supporto per 5 lingue (Italiano, Inglese, Francese, Tedesco, Spagnolo)
- **Database MySQL**: Persistenza affidabile con backup e performance ottimizzate

### Nuove Funzionalità v2.0

#### 🎯 **Template di Messaggi**
- **Creazione Template**: Prepara liste di messaggi personalizzati con nome e descrizione
- **Salvataggio Automatico**: I template vengono salvati nel database per riutilizzo futuro
- **Caricamento Rapido**: Carica template esistenti nel form di invio messaggi
- **Invio Diretto**: Invia tutti i messaggi di un template con un solo click
- **Gestione Template**: Visualizza, modifica ed elimina template salvati

#### 📊 **Cronologia Messaggi Avanzata**
- **Filtri Intelligenti**: Filtra per stato (inviato/fallito) e per utente specifico
- **Statistiche Real-time**: Visualizza tassi di successo e metriche di performance
- **Paginazione**: Gestione efficiente di grandi quantità di messaggi
- **Dettagli Errori**: Visualizza errori specifici per diagnosticare problemi
- **Vista Completa**: Espandi messaggi lunghi per visualizzazione completa

#### 🌍 **Supporto Multilingua**
- **5 Lingue Supportate**: Italiano (default), Inglese, Francese, Tedesco, Spagnolo
- **Cambio Dinamico**: Cambia lingua con un click, memorizzata in sessione
- **Interfaccia Completa**: Tutti i testi dell'interfaccia sono tradotti
- **File .po**: Gestione traduzioni tramite file Gettext standard

#### 🔧 **Strumenti di Debug**
- **Test Connessione Bot**: Verifica configurazione token e stato bot
- **Test Messaggi Singoli**: Invia messaggi di prova a utenti specifici
- **Debug Ambiente**: Controlla variabili .env e configurazione
- **Log Dettagliati**: Tracciamento completo di errori e successi

## Struttura del Progetto

```
telegram-group-manager/
├── app/
│   ├── __init__.py              # Inizializzazione app Flask con Babel
│   ├── models.py                # Modelli database estesi
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py              # Route homepage e dashboard
│   │   ├── groups.py            # Route gestione gruppi e template
│   │   ├── telegram_bot.py      # Route operazioni bot Telegram
│   │   └── i18n.py              # Route gestione lingue
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css       # Stili personalizzati
│   │   └── js/
│   │       └── main.js          # JavaScript personalizzato
│   ├── templates/
│   │   ├── base.html            # Template base con selettore lingua
│   │   ├── index.html           # Homepage/Dashboard
│   │   ├── group_detail.html    # Dettaglio gruppo con strumenti avanzati
│   │   └── groups/              # Template per funzionalità gruppi
│   │       ├── templates.html   # Lista template salvati
│   │       ├── create_template.html  # Creazione nuovo template
│   │       ├── view_template.html    # Visualizzazione template
│   │       └── message_history.html # Cronologia messaggi avanzata
│   ├── utils/
│   │   ├── __init__.py
│   │   └── telegram_helper.py   # Funzioni helper per API Telegram
│   └── translations/            # File traduzioni
│       ├── en/LC_MESSAGES/      # Inglese
│       ├── fr/LC_MESSAGES/      # Francese
│       ├── de/LC_MESSAGES/      # Tedesco
│       └── es/LC_MESSAGES/      # Spagnolo
├── instance/
├── .env                         # Variabili d'ambiente
├── babel.cfg                    # Configurazione Babel
├── requirements.txt             # Dipendenze Python aggiornate
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
   
   # Crea utente dedicato
   CREATE USER 'telegram_user'@'localhost' IDENTIFIED BY 'your_password';
   
   # Crea database
   CREATE DATABASE telegram_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   # Concedi permessi
   GRANT ALL PRIVILEGES ON telegram_manager.* TO 'telegram_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

### Setup Applicazione

1. **Clona o scarica il progetto**
   ```bash
   cd telegram-group-manager
   ```

2. **Crea ambiente virtuale**
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

   Modifica il file `.env`:
   ```env
   # Bot Telegram
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   
   # Database MySQL
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=telegram_manager
   DB_USER=telegram_user
   DB_PASSWORD=your_password
   
   # Sicurezza
   SECRET_KEY=your_very_long_random_secret_key_here
   
   # Ambiente
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

5. **Crea le tabelle aggiuntive**
   ```bash
   python create_message_templates.py
   ```

6. **Avvia l'applicazione**
   ```bash
   python run.py
   ```

7. **Accedi all'applicazione**

   Apri il browser: `http://127.0.0.1:5000`

## Configurazione Bot Telegram

### Creazione Bot

1. Apri Telegram e cerca `@BotFather`
2. Invia `/newbot` e segui le istruzioni
3. Ottieni il token del bot
4. Inserisci il token nel file `.env`

### Test Configurazione

Usa gli strumenti di debug integrati:
- `/groups/{group_id}/debug_bot` - Testa token e connessione
- `/groups/{group_id}/test_message/{user_id}` - Testa invio singolo messaggio

## Utilizzo delle Nuove Funzionalità

### 🎯 Template di Messaggi

#### Creazione Template
1. Vai al dettaglio di un gruppo
2. Clicca su **"Nuovo Template"** nella sezione Strumenti Avanzati
3. Inserisci nome e descrizione del template
4. Compila i messaggi personalizzati per ogni utente
5. Clicca **"Salva Template"**

#### Utilizzo Template
1. Vai a **"Vedi Template"** per visualizzare template salvati
2. Clicca **"Carica & Invia"** per caricare un template nel form
3. Modifica i messaggi se necessario
4. Invia normalmente o usa **"Invia Diretto"** dal template

#### Gestione Template
- **Visualizza**: Vedi tutti i messaggi di un template
- **Carica**: Carica nel form per modifiche
- **Invia Diretto**: Invia immediatamente senza modifiche
- **Elimina**: Rimuovi template non più necessari

### 📊 Cronologia Messaggi Avanzata

#### Visualizzazione
1. Vai al dettaglio gruppo
2. Clicca **"Cronologia Messaggi"** negli Strumenti Avanzati
3. Visualizza statistiche di successo in tempo reale

#### Filtri Disponibili
- **Per Stato**: Tutti, Inviati, Falliti, In Attesa
- **Per Utente**: Filtra messaggi di un utente specifico
- **Combinati**: Usa entrambi i filtri insieme

#### Funzionalità
- **Paginazione**: Naviga tra pagine di messaggi
- **Dettagli Errori**: Clicca su "Errore" per vedere dettagli specifici
- **Messaggi Completi**: Espandi messaggi lunghi troncati
- **Reset Filtri**: Torna alla vista completa

### 🌍 Cambio Lingua

1. Usa il selettore lingua nell'header (in alto a destra)
2. La lingua viene memorizzata nella sessione
3. Ricarica la pagina per vedere tutti i testi tradotti

#### Lingue Supportate
- 🇮🇹 **Italiano** (default)
- 🇬🇧 **English**
- 🇫🇷 **Français**
- 🇩🇪 **Deutsch**
- 🇪🇸 **Español**

## Struttura Database Aggiornata

### Nuove Tabelle

**message_templates**
- `id`: ID primario
- `name`: Nome template (max 200 char)
- `description`: Descrizione opzionale
- `group_id`: Riferimento al gruppo (FK)
- `created_at`: Data creazione
- `updated_at`: Ultimo aggiornamento
- `is_active`: Flag per soft delete

**template_messages**
- `id`: ID primario
- `template_id`: Riferimento al template (FK)
- `user_id`: Riferimento all'utente (FK)
- `message_text`: Testo messaggio personalizzato
- `order_index`: Ordine nel template
- `created_at`: Data creazione

### Tabelle Esistenti (Aggiornate)

**message_logs** (migliorata)
- Ora include `error_message` dettagliato
- `telegram_message_id` per tracciamento Telegram
- Migliori indici per performance filtri

**users** (estesa)
- `language_code`: Lingua preferita utente
- `display_name`: Nome visualizzazione migliorato
- Indici ottimizzati per ricerche

**groups** (ottimizzata)
- Relazione con `message_templates`
- Timestamp aggiornamento automatico
- Performance query migliorate

## API Endpoints Aggiornati

### Template Routes
- `GET /groups/<id>/templates` - Lista template gruppo
- `POST /groups/<id>/templates/create` - Crea nuovo template
- `GET /groups/<id>/templates/<template_id>` - Visualizza template
- `GET /groups/<id>/templates/<template_id>/load` - Carica template nel form
- `POST /groups/<id>/templates/<template_id>/send` - Invia messaggi template
- `POST /groups/<id>/templates/<template_id>/delete` - Elimina template

### Cronologia Routes
- `GET /groups/<id>/message_history` - Cronologia con filtri
- Query params: `status`, `user_id`, `page` per filtri e paginazione

### Debug Routes
- `GET /groups/<id>/debug_bot` - Test configurazione bot
- `GET /groups/<id>/test_message/<user_id>` - Test messaggio singolo
- `GET /groups/<id>/debug_env` - Debug variabili ambiente

### Lingua Routes
- `GET /i18n/set/<language>` - Cambia lingua interfaccia
- Supporta: `it`, `en`, `fr`, `de`, `es`

## Funzionalità Avanzate

### Template Intelligence
- **Statistiche Real-time**: Conteggio messaggi compilati durante creazione
- **Preview Intelligente**: Anteprima messaggi prima del salvataggio
- **Azioni Rapide**: Riempimento automatico per tutti gli utenti
- **Validazione Smart**: Controlla completezza template prima del salvataggio

### Cronologia Analytics
- **Tassi di Successo**: Calcolo percentuale successo invii
- **Filtri Combinati**: Combina più filtri per analisi dettagliate
- **Export Ready**: Struttura dati pronta per export CSV/Excel
- **Trend Analysis**: Visualizza andamento invii nel tempo

### Performance Ottimizzate
- **Query Efficienti**: Indici ottimizzati per filtri cronologia
- **Paginazione Smart**: Caricamento progressivo per grandi dataset
- **Cache Session**: Memorizzazione preferenze utente
- **Lazy Loading**: Caricamento componenti solo quando necessari

## Risoluzione Problemi Aggiornata

### Errori Template

**"Template non salvato"**
- Verifica che almeno un messaggio sia compilato
- Controlla che il nome template non esista già
- Assicurati che il gruppo abbia utenti

**"Template non caricato"**
- Controlla che il template esista e sia attivo
- Verifica permessi accesso gruppo
- Aggiorna la pagina se necessario

### Errori Cronologia

**"Cronologia vuota"**
- Controlla che siano stati inviati messaggi
- Verifica filtri applicati (potrebbe nascondere risultati)
- Controlla connessione database

**"Filtri non funzionano"**
- Usa il pulsante "Reset" per tornare alla vista completa
- Verifica che gli utenti selezionati abbiano messaggi
- Controlla che i stati filtrati esistano

### Errori Multilingua

**"Testi non tradotti"**
- Verifica che i file .mo siano compilati
- Controlla che la lingua sia supportata
- Riavvia applicazione dopo modifiche traduzioni

**"Cambio lingua non funziona"**
- Controlla che il route i18n sia registrato
- Verifica che le sessioni Flask funzionino
- Controlla permessi file traduzioni

### Debug Bot Migliorato

**Token non trovato**
```bash
# Verifica file .env
cat .env | grep TELEGRAM_BOT_TOKEN

# Test manuale token
curl "https://api.telegram.org/bot<TOKEN>/getMe"
```

**Messaggi non arrivano**
```bash
# Usa debug route
/groups/{group_id}/debug_env
/groups/{group_id}/test_message/{user_id}

# Controlla log dettagliati in console
```

## Backup e Sicurezza

### Backup Template
I template sono salvati in `message_templates` e `template_messages`:

```sql
-- Backup solo template
mysqldump -u telegram_user -p telegram_manager message_templates template_messages > templates_backup.sql

-- Restore template
mysql -u telegram_user -p telegram_manager < templates_backup.sql
```

### Sicurezza Multilingua
- File traduzioni protetti da accesso diretto
- Validazione input per prevenire injection
- Sanitizzazione parametri lingua

### Performance Template
- Indici ottimizzati per ricerche template
- Cache in memoria per template frequenti
- Cleanup automatico template non utilizzati

## Roadmap Futura

### V2.1 (Prossimo)
- **Export Cronologia**: Esporta messaggi in CSV/Excel
- **Template Condivisi**: Condividi template tra gruppi
- **Scheduled Messages**: Programmazione invio messaggi
- **Rich Text Editor**: Editor avanzato per messaggi

### V2.2 (Futuro)
- **Dashboard Analytics**: Grafici e metriche avanzate
- **API REST**: Endpoint pubblici per integrazione
- **Webhook Support**: Notifiche in tempo reale
- **Mobile App**: App companion per iOS/Android

### V3.0 (Visione)
- **Multi-Bot Support**: Gestione bot multipli
- **Team Collaboration**: Condivisione gruppi tra utenti
- **Advanced Automation**: Workflow automatizzati
- **Enterprise Features**: SSO, audit logs, compliance

## Common Error Solutions

### Database Connection Issues

**"Can't connect to MySQL server"**
- Verify MySQL is running: `sudo systemctl status mysql`
- Check host and port in `.env` file
- Test connection: `mysql -h localhost -u telegram_user -p`

**"Access denied for user"**
- Verify username and password in `.env` file
- Check MySQL user permissions:
  ```sql
  SHOW GRANTS FOR 'telegram_user'@'localhost';
  ```
- Recreate user if necessary

**"Unknown database 'telegram_manager'"**
- Run `python setup_database.py` to create database
- Or create manually:
  ```sql
  CREATE DATABASE telegram_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```

### Bot Configuration Issues

**"Bot token not configured"**
- Verify token is correct in `.env` file
- Ensure `.env` file is in main directory
- Check token format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

**"Bot connection error"**
- Check internet connection
- Verify token is valid with @BotFather
- Test manually: `https://api.telegram.org/bot<TOKEN>/getMe`

**"No users imported"**
- Users must have interacted with bot at least once
- Verify bot is not blocked by users
- Check bot has message reading permissions

**"Message sending error"**
- User might have blocked the bot
- Verify Telegram ID is correct
- Check Telegram API rate limits (30 msg/sec)

### Performance Optimization

#### MySQL Configuration

```sql
-- my.cnf or my.ini
[mysqld]
innodb_buffer_pool_size = 256M
innodb_log_file_size = 64M
max_connections = 200
query_cache_size = 64M
tmp_table_size = 64M
max_heap_table_size = 64M
```

#### Query Monitoring

```sql
-- Slow queries
SHOW PROCESSLIST;

-- Table statistics
SELECT table_name, table_rows, data_length, index_length 
FROM information_schema.tables 
WHERE table_schema = 'telegram_manager';

-- Used indexes
SHOW INDEX FROM users;
SHOW INDEX FROM groups;
SHOW INDEX FROM message_logs;
```

## Requirements

### System Requirements
- **Operating System**: Linux, macOS, Windows
- **Python**: 3.8+ (recommended 3.9+)
- **Database**: MySQL 5.7+ or MariaDB 10.2+
- **Memory**: Minimum 512MB RAM (recommended 1GB+)
- **Storage**: 100MB + database storage

### Python Dependencies
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Babel==3.1.0
python-dotenv==1.0.0
PyMySQL==1.1.0
requests==2.31.0
```

### Browser Support
- **Chrome**: 80+
- **Firefox**: 75+
- **Safari**: 13+
- **Edge**: 80+

## Security Considerations

### Production Deployment
- Change `SECRET_KEY` to a strong random value
- Use environment variables for all sensitive data
- Enable HTTPS/SSL for web traffic
- Restrict database access to application only
- Regular security updates for dependencies

### Bot Security
- Keep bot token confidential
- Use webhook instead of polling for production
- Implement rate limiting for API calls
- Monitor bot usage and logs

### Data Protection
- Regular database backups
- Encrypt sensitive data at rest
- Implement proper access controls
- Log security events

---

**Versione**: 2.0.0  
**Database**: MySQL 5.7+ / MariaDB 10.2+  
**Ultimo aggiornamento**: Agosto 2025  
**Compatibilità**: Python 3.8+, Flask 2.3+, Bootstrap 5  
**Nuove Features**: Template Messaggi, Cronologia Avanzata, Supporto Multilingua