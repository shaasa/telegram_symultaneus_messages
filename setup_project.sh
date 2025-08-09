#!/bin/bash

# Script per creare la struttura del progetto Telegram Group Manager
# Per Linux/Mac

echo "Creazione struttura progetto Telegram Group Manager..."

# Crea struttura cartelle
mkdir -p app/routes
mkdir -p app/static/css
mkdir -p app/static/js
mkdir -p app/templates
mkdir -p app/utils
mkdir -p instance

# Crea file Python
touch app/__init__.py
touch app/models.py
touch app/routes/__init__.py
touch app/routes/main.py
touch app/routes/groups.py
touch app/routes/telegram_bot.py
touch app/utils/__init__.py
touch app/utils/telegram_helper.py
touch config.py
touch run.py

# Crea file HTML
touch app/templates/base.html
touch app/templates/index.html
touch app/templates/groups.html
touch app/templates/group_detail.html

# Crea file CSS e JS
touch app/static/css/custom.css
touch app/static/js/main.js

# Crea file di configurazione
touch requirements.txt
touch README.md
touch .env
touch .gitignore

echo "Struttura creata con successo!"
echo ""
echo "Struttura del progetto:"
tree . 2>/dev/null || find . -type f | sort

echo ""
echo "Per procedere:"
echo "1. cd telegram-group-manager"
echo "2. Copia il codice negli appositi file"
echo "3. pip install -r requirements.txt"
echo "4. python run.py"