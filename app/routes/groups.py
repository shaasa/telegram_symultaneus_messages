from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Group, User, MessageLog, MessageTemplate, TemplateMessage
from app import db

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/')
def list_groups():
    """Lista tutti i gruppi"""
    groups = Group.query.order_by(Group.created_at.desc()).all()
    return render_template('groups.html', groups=groups)

@groups_bp.route('/create', methods=['GET', 'POST'])
def create_group():
    """Crea un nuovo gruppo"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        if not name:
            flash('Il nome del gruppo è obbligatorio', 'error')
            return redirect(url_for('groups.list_groups'))

        # Verifica che il nome non esista già
        if Group.query.filter_by(name=name).first():
            flash('Un gruppo con questo nome esiste già', 'error')
            return redirect(url_for('groups.list_groups'))

        group = Group(name=name, description=description)
        db.session.add(group)
        db.session.commit()

        flash(f'Gruppo "{name}" creato con successo', 'success')
        return redirect(url_for('groups.group_detail', group_id=group.id))

    return redirect(url_for('groups.list_groups'))

@groups_bp.route('/<int:group_id>')
def group_detail(group_id):
    """Dettaglio gruppo con lista utenti e form per messaggi"""
    group = Group.query.get_or_404(group_id)
    available_users = User.query.filter(~User.id.in_([u.id for u in group.users])).all()

    return render_template('group_detail.html',
                           group=group,
                           available_users=available_users)

@groups_bp.route('/<int:group_id>/add_user', methods=['POST'])
def add_user_to_group(group_id):
    """Aggiunge un utente al gruppo"""
    group = Group.query.get_or_404(group_id)
    user_id = request.form.get('user_id')

    if not user_id:
        flash('Seleziona un utente da aggiungere', 'error')
        return redirect(url_for('groups.group_detail', group_id=group_id))

    user = User.query.get_or_404(user_id)

    if user in group.users:
        flash(f'L\'utente {user.full_name} è già nel gruppo', 'warning')
    else:
        group.users.append(user)
        db.session.commit()
        flash(f'Utente {user.full_name} aggiunto al gruppo', 'success')

    return redirect(url_for('groups.group_detail', group_id=group_id))

@groups_bp.route('/<int:group_id>/remove_user/<int:user_id>', methods=['POST'])
def remove_user_from_group(group_id, user_id):
    """Rimuove un utente dal gruppo"""
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(user_id)

    if user in group.users:
        group.users.remove(user)
        db.session.commit()
        flash(f'Utente {user.full_name} rimosso dal gruppo', 'success')
    else:
        flash('Utente non trovato nel gruppo', 'error')

    return redirect(url_for('groups.group_detail', group_id=group_id))
# Sostituisci la funzione send_messages nel tuo groups.py con questa versione debug:

@groups_bp.route('/<int:group_id>/send_messages', methods=['POST'])
def send_messages(group_id):
    """Invia messaggi personalizzati agli utenti del gruppo con debug esteso"""
    group = Group.query.get_or_404(group_id)

    if not group.users:
        flash('Il gruppo non ha utenti', 'error')
        return redirect(url_for('groups.group_detail', group_id=group_id))

    messages_sent = 0
    messages_failed = 0
    debug_info = []

    # Importa la funzione di invio
    from app.utils.telegram_helper import send_telegram_message

    for user in group.users:
        message_text = request.form.get(f'message_{user.id}', '').strip()

        if not message_text:
            debug_info.append(f"⏭️ {user.full_name}: messaggio vuoto, saltato")
            continue

        debug_info.append(f"📝 Preparazione messaggio per {user.full_name} (ID: {user.telegram_id})")

        # Crea log del messaggio
        message_log = MessageLog(
            group_id=group.id,
            user_id=user.id,
            message_text=message_text,
            status='pending'
        )
        db.session.add(message_log)
        db.session.flush()  # Per ottenere l'ID del log

        debug_info.append(f"💾 Log creato con ID: {message_log.id}")

        # Invia messaggio via Telegram
        try:
            debug_info.append(f"🚀 Tentativo invio a {user.full_name}...")

            result = send_telegram_message(user.telegram_id, message_text)

            debug_info.append(f"📨 Risultato per {user.full_name}: {result}")

            if result and isinstance(result, dict) and result.get('success'):
                message_log.status = 'sent'
                message_log.telegram_message_id = result.get('message_id')
                messages_sent += 1
                debug_info.append(f"✅ {user.full_name}: INVIATO (Message ID: {result.get('message_id')})")
            elif result and isinstance(result, dict):
                # Risultato con errore
                message_log.status = 'failed'
                message_log.error_message = result.get('error', 'Errore sconosciuto')
                messages_failed += 1
                debug_info.append(f"❌ {user.full_name}: FALLITO - {result.get('error')}")
            elif result is True:
                # Vecchio formato (True/False)
                message_log.status = 'sent'
                messages_sent += 1
                debug_info.append(f"✅ {user.full_name}: INVIATO (formato vecchio)")
            elif result is False:
                # Vecchio formato (True/False)
                message_log.status = 'failed'
                message_log.error_message = 'Invio fallito (nessun dettaglio disponibile)'
                messages_failed += 1
                debug_info.append(f"❌ {user.full_name}: FALLITO (formato vecchio)")
            else:
                # Risultato inaspettato
                message_log.status = 'failed'
                message_log.error_message = f'Risultato inaspettato: {result}'
                messages_failed += 1
                debug_info.append(f"❓ {user.full_name}: RISULTATO INASPETTATO - {result}")

        except Exception as e:
            message_log.status = 'failed'
            message_log.error_message = f"Eccezione Python: {str(e)}"
            messages_failed += 1
            debug_info.append(f"💥 {user.full_name}: ECCEZIONE - {str(e)}")

    # Salva tutti i log
    db.session.commit()
    debug_info.append(f"💾 Tutti i log salvati nel database")

    # Debug completo
    debug_info.append(f"📊 RISULTATI FINALI:")
    debug_info.append(f"📊 Messaggi inviati: {messages_sent}")
    debug_info.append(f"📊 Messaggi falliti: {messages_failed}")

    # Mostra debug info come flash messages
    for info in debug_info:
        if "✅" in info or "INVIATO" in info:
            flash(info, 'success')
        elif "❌" in info or "FALLITO" in info or "💥" in info:
            flash(info, 'error')
        else:
            flash(info, 'info')

    # Messaggi di feedback riassuntivi
    if messages_sent > 0:
        flash(f'🎉 SUCCESSO: {messages_sent} messaggi inviati con successo', 'success')
    if messages_failed > 0:
        flash(f'⚠️ PROBLEMI: {messages_failed} messaggi non inviati. Controlla i dettagli sopra.', 'error')

    if messages_sent == 0 and messages_failed == 0:
        flash('ℹ️ Nessun messaggio da inviare (tutti i campi erano vuoti)', 'warning')

    return redirect(url_for('groups.group_detail', group_id=group_id))

@groups_bp.route('/<int:group_id>/delete', methods=['POST'])
def delete_group(group_id):
    """Elimina un gruppo"""
    group = Group.query.get_or_404(group_id)
    group_name = group.name

    # Rimuovi prima i messaggi associati
    MessageLog.query.filter_by(group_id=group_id).delete()

    db.session.delete(group)
    db.session.commit()

    flash(f'Gruppo "{group_name}" eliminato con successo', 'success')
    return redirect(url_for('groups.list_groups'))
# Aggiungi queste route alla fine del tuo file groups.py esistente
# Aggiungi anche questo import all'inizio del file:
# from app.models import Group, User, MessageLog, MessageTemplate, TemplateMessage

@groups_bp.route('/<int:group_id>/templates')
def list_templates(group_id):
    """Lista dei template di messaggi salvati per un gruppo"""
    from app.models import MessageTemplate

    group = Group.query.get_or_404(group_id)
    templates = MessageTemplate.query.filter_by(
        group_id=group_id,
        is_active=True
    ).order_by(MessageTemplate.created_at.asc()).all()

    return render_template('groups/templates.html', group=group, templates=templates)

@groups_bp.route('/<int:group_id>/templates/create', methods=['GET', 'POST'])
def create_template(group_id):
    """Crea un nuovo template di messaggi"""
    from app.models import MessageTemplate, TemplateMessage

    group = Group.query.get_or_404(group_id)

    if not group.users:
        flash('Il gruppo deve avere almeno un utente per creare un template', 'error')
        return redirect(url_for('groups.group_detail', group_id=group_id))

    if request.method == 'POST':
        template_name = request.form.get('template_name', '').strip()
        template_description = request.form.get('template_description', '').strip()

        if not template_name:
            flash('Il nome del template è obbligatorio', 'error')
            return render_template('groups/create_template.html', group=group)

        # Verifica che non esista già un template con questo nome per il gruppo
        existing_template = MessageTemplate.query.filter_by(
            group_id=group_id,
            name=template_name,
            is_active=True
        ).first()

        if existing_template:
            flash('Esiste già un template con questo nome per questo gruppo', 'error')
            return render_template('groups/create_template.html', group=group)

        # Crea il template
        template = MessageTemplate(
            name=template_name,
            description=template_description,
            group_id=group_id
        )
        db.session.add(template)
        db.session.flush()  # Per ottenere l'ID

        # Salva i messaggi per ogni utente
        messages_saved = 0
        for user in group.users:
            message_text = request.form.get(f'message_{user.id}', '').strip()
            if message_text:
                template_message = TemplateMessage(
                    template_id=template.id,
                    user_id=user.id,
                    message_text=message_text,
                    order_index=messages_saved
                )
                db.session.add(template_message)
                messages_saved += 1

        if messages_saved == 0:
            db.session.rollback()
            flash('Devi inserire almeno un messaggio per salvare il template', 'error')
            return render_template('groups/create_template.html', group=group)

        db.session.commit()
        flash(f'Template "{template_name}" salvato con {messages_saved} messaggi', 'success')
        return redirect(url_for('groups.list_templates', group_id=group_id))

    return render_template('groups/create_template.html', group=group)

@groups_bp.route('/<int:group_id>/templates/<int:template_id>')
def view_template(group_id, template_id):
    """Visualizza un template di messaggi"""
    from app.models import MessageTemplate

    group = Group.query.get_or_404(group_id)
    template = MessageTemplate.query.filter_by(
        id=template_id,
        group_id=group_id,
        is_active=True
    ).first_or_404()

    return render_template('groups/view_template.html', group=group, template=template)

@groups_bp.route('/<int:group_id>/templates/<int:template_id>/load')
def load_template(group_id, template_id):
    """Carica un template nella pagina di invio messaggi"""
    from app.models import MessageTemplate

    group = Group.query.get_or_404(group_id)
    template = MessageTemplate.query.filter_by(
        id=template_id,
        group_id=group_id,
        is_active=True
    ).first_or_404()

    # Crea un dizionario con i messaggi per ogni utente
    template_data = {}
    for template_msg in template.template_messages:
        template_data[template_msg.user_id] = template_msg.message_text

    return render_template('group_detail.html',
                           group=group,
                           template=template,
                           template_data=template_data,
                           available_users=User.query.filter(~User.id.in_([u.id for u in group.users])).all())

@groups_bp.route('/<int:group_id>/templates/<int:template_id>/send', methods=['POST'])
def send_template_messages(group_id, template_id):
    """Invia i messaggi di un template"""
    from app.models import MessageTemplate

    group = Group.query.get_or_404(group_id)
    template = MessageTemplate.query.filter_by(
        id=template_id,
        group_id=group_id,
        is_active=True
    ).first_or_404()

    messages_sent = 0
    messages_failed = 0

    # Importa qui per evitare import circolari
    from app.utils.telegram_helper import send_telegram_message

    for template_msg in template.template_messages:
        # Crea log del messaggio
        message_log = MessageLog(
            group_id=group.id,
            user_id=template_msg.user_id,
            message_text=template_msg.message_text,
            status='pending'
        )
        db.session.add(message_log)

        # Invia messaggio via Telegram
        try:
            success = send_telegram_message(template_msg.user.telegram_id, template_msg.message_text)
            if success:
                message_log.status = 'sent'
                messages_sent += 1
            else:
                message_log.status = 'failed'
                message_log.error_message = 'Errore nell\'invio del messaggio'
                messages_failed += 1
        except Exception as e:
            message_log.status = 'failed'
            message_log.error_message = str(e)
            messages_failed += 1

    db.session.commit()

    if messages_sent > 0:
        flash(f'Template "{template.name}": {messages_sent} messaggi inviati con successo', 'success')
    if messages_failed > 0:
        flash(f'Template "{template.name}": {messages_failed} messaggi non inviati', 'error')

    return redirect(url_for('groups.group_detail', group_id=group_id))

@groups_bp.route('/<int:group_id>/templates/<int:template_id>/delete', methods=['POST'])
def delete_template(group_id, template_id):
    """Elimina un template (soft delete)"""
    from app.models import MessageTemplate

    group = Group.query.get_or_404(group_id)
    template = MessageTemplate.query.filter_by(
        id=template_id,
        group_id=group_id,
        is_active=True
    ).first_or_404()

    template_name = template.name
    template.is_active = False  # Soft delete
    db.session.commit()

    flash(f'Template "{template_name}" eliminato', 'success')
    return redirect(url_for('groups.list_templates', group_id=group_id))

@groups_bp.route('/<int:group_id>/message_history')
def message_history(group_id):
    """Cronologia dei messaggi inviati per un gruppo usando la tabella message_logs esistente"""
    group = Group.query.get_or_404(group_id)

    # Filtri opzionali
    status_filter = request.args.get('status', '')
    user_filter = request.args.get('user_id', '', type=int)

    # Query base
    query = MessageLog.query.filter_by(group_id=group_id)

    # Applica filtri
    if status_filter:
        query = query.filter(MessageLog.status == status_filter)
    if user_filter:
        query = query.filter(MessageLog.user_id == user_filter)

    # Paginazione per evitare problemi con molti messaggi
    page = request.args.get('page', 1, type=int)
    per_page = 50

    messages = query.order_by(MessageLog.sent_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    # Statistiche rapide
    total_messages = MessageLog.query.filter_by(group_id=group_id).count()
    sent_messages = MessageLog.query.filter_by(group_id=group_id, status='sent').count()
    failed_messages = MessageLog.query.filter_by(group_id=group_id, status='failed').count()

    stats = {
        'total': total_messages,
        'sent': sent_messages,
        'failed': failed_messages,
        'success_rate': round((sent_messages / total_messages * 100) if total_messages > 0 else 0, 1)
    }

    return render_template('groups/message_history.html',
                           group=group,
                           messages=messages,
                           stats=stats,
                           current_status=status_filter,
                           current_user=user_filter)
# Aggiungi queste route alla fine del tuo groups.py:

@groups_bp.route('/<int:group_id>/debug_bot')
def debug_bot(group_id):
    """Route di debug completo per il bot"""
    group = Group.query.get_or_404(group_id)

    from app.utils.telegram_helper import test_bot_connection, get_bot_token
    import os

    # Test token
    token = get_bot_token()
    token_status = {
        'found': bool(token),
        'length': len(token) if token else 0,
        'env_var': bool(os.environ.get('TELEGRAM_BOT_TOKEN')),
        'preview': f"{token[:10]}...{token[-4:]}" if token and len(token) > 14 else token
    }

    # Test connessione
    bot_test = test_bot_connection()

    # Mostra risultati
    flash(f"🔑 Token trovato: {token_status['found']} (lunghezza: {token_status['length']})", 'info')
    flash(f"🌍 Da variabile ambiente: {token_status['env_var']}", 'info')

    if token_status['found']:
        flash(f"👁️ Preview token: {token_status['preview']}", 'info')

    if bot_test['success']:
        bot_info = bot_test['bot_info']
        flash(f"✅ Bot connesso: @{bot_info.get('username')} ({bot_info.get('first_name')})", 'success')
        flash(f"🤖 Bot ID: {bot_info.get('id')}", 'info')
    else:
        flash(f"❌ Errore connessione bot: {bot_test['error']}", 'error')

    return redirect(url_for('groups.group_detail', group_id=group_id))

@groups_bp.route('/<int:group_id>/test_message/<int:user_id>')
def test_single_message(group_id, user_id):
    """Testa invio a un singolo utente con debug completo"""
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(user_id)

    from app.utils.telegram_helper import send_telegram_message
    from datetime import datetime

    test_message = f"🧪 Test message sent at {datetime.now().strftime('%H:%M:%S')} from {group.name}"

    flash(f"🚀 Tentativo invio a {user.full_name} (ID: {user.telegram_id})", 'info')

    # Crea log
    message_log = MessageLog(
        group_id=group.id,
        user_id=user.id,
        message_text=test_message,
        status='pending'
    )
    db.session.add(message_log)
    db.session.flush()

    # Invia con logging dettagliato
    result = send_telegram_message(user.telegram_id, test_message)

    # Aggiorna log con risultato dettagliato
    if result['success']:
        message_log.status = 'sent'
        message_log.telegram_message_id = result['message_id']
        flash(f"✅ Messaggio inviato! Message ID: {result['message_id']}", 'success')
    else:
        message_log.status = 'failed'
        message_log.error_message = result['error']
        flash(f"❌ ERRORE: {result['error']}", 'error')
        if result['error_code']:
            flash(f"🔢 Codice errore: {result['error_code']}", 'error')

    db.session.commit()

    return redirect(url_for('groups.group_detail', group_id=group_id))
# Aggiungi questa route al tuo groups.py per test diretto:

@groups_bp.route('/<int:group_id>/raw_test/<int:user_id>')
def raw_test_message(group_id, user_id):
    """Test diretto della funzione send_telegram_message senza database"""
    group = Group.query.get_or_404(group_id)
    user = User.query.get_or_404(user_id)

    from app.utils.telegram_helper import send_telegram_message, get_bot_token
    from datetime import datetime
    import os

    # Info preliminari
    token = get_bot_token()
    flash(f"🔑 Token presente: {bool(token)}", 'info')
    flash(f"🎯 Target: {user.full_name} (ID: {user.telegram_id})", 'info')

    # Test message
    test_message = f"🔧 RAW TEST {datetime.now().strftime('%H:%M:%S')}"
    flash(f"📝 Messaggio: {test_message}", 'info')

    try:
        # Chiamata diretta
        flash("🚀 Chiamata diretta send_telegram_message...", 'info')
        result = send_telegram_message(user.telegram_id, test_message)

        # Analisi risultato
        flash(f"📊 Tipo risultato: {type(result)}", 'info')
        flash(f"📊 Valore risultato: {result}", 'info')

        if isinstance(result, dict):
            flash(f"📊 Success: {result.get('success')}", 'info')
            flash(f"📊 Message ID: {result.get('message_id')}", 'info')
            flash(f"📊 Error: {result.get('error')}", 'info')

            if result.get('success'):
                flash("✅ La funzione dice che è andato a buon fine!", 'success')
            else:
                flash(f"❌ La funzione dice che è fallito: {result.get('error')}", 'error')
        elif result is True:
            flash("✅ Risultato True (formato vecchio)", 'success')
        elif result is False:
            flash("❌ Risultato False (formato vecchio)", 'error')
        else:
            flash(f"❓ Risultato inaspettato: {result}", 'warning')

    except Exception as e:
        flash(f"💥 Eccezione durante test: {str(e)}", 'error')
        import traceback
        flash(f"🔍 Traceback: {traceback.format_exc()}", 'error')

    return redirect(url_for('groups.group_detail', group_id=group_id))

@groups_bp.route('/<int:group_id>/check_logs')
def check_recent_logs(group_id):
    """Controlla gli ultimi log di messaggi per questo gruppo"""
    group = Group.query.get_or_404(group_id)

    # Ultimi 10 messaggi
    recent_logs = MessageLog.query.filter_by(group_id=group_id) \
        .order_by(MessageLog.sent_at.desc()) \
        .limit(10).all()

    flash(f"📊 Ultimi {len(recent_logs)} messaggi del gruppo:", 'info')

    for log in recent_logs:
        timestamp = log.sent_at.strftime('%H:%M:%S')
        user_name = log.user.full_name if log.user else f"User ID {log.user_id}"

        if log.status == 'sent':
            msg = f"✅ {timestamp} - {user_name}: INVIATO"
            if log.telegram_message_id:
                msg += f" (Msg ID: {log.telegram_message_id})"
            flash(msg, 'success')
        elif log.status == 'failed':
            msg = f"❌ {timestamp} - {user_name}: FALLITO"
            if log.error_message:
                msg += f" - {log.error_message}"
            flash(msg, 'error')
        else:
            flash(f"⏳ {timestamp} - {user_name}: {log.status.upper()}", 'warning')

    if not recent_logs:
        flash("📭 Nessun messaggio trovato per questo gruppo", 'info')

    return redirect(url_for('groups.group_detail', group_id=group_id))
# Aggiungi questa route temporanea al tuo groups.py per debug:

@groups_bp.route('/<int:group_id>/debug_env')
def debug_environment(group_id):
    """Debug delle variabili ambiente"""
    import os

    # Controlla tutte le variabili del .env
    env_vars = {
        'TELEGRAM_BOT_TOKEN': os.environ.get('TELEGRAM_BOT_TOKEN'),
        'SECRET_KEY': os.environ.get('SECRET_KEY'),
        'DB_HOST': os.environ.get('DB_HOST'),
        'DB_USER': os.environ.get('DB_USER'),
        'DB_PASSWORD': os.environ.get('DB_PASSWORD'),
        'DB_NAME': os.environ.get('DB_NAME'),
    }

    flash("🔍 DEBUG VARIABILI AMBIENTE:", 'info')

    for var_name, var_value in env_vars.items():
        if var_value:
            if 'TOKEN' in var_name or 'PASSWORD' in var_name or 'KEY' in var_name:
                # Per variabili sensibili, mostra solo info generali
                preview = f"{var_value[:6]}...{var_value[-4:]}" if len(var_value) > 10 else "***"
                flash(f"✅ {var_name}: PRESENTE (lunghezza: {len(var_value)}, preview: {preview})", 'success')
            else:
                flash(f"✅ {var_name}: {var_value}", 'success')
        else:
            flash(f"❌ {var_name}: NON TROVATA", 'error')

    # Test diretto import dotenv
    try:
        from dotenv import load_dotenv
        flash("✅ Modulo dotenv importato correttamente", 'success')

        # Prova a ricaricare
        load_dotenv()
        token_dopo_reload = os.environ.get('TELEGRAM_BOT_TOKEN')
        flash(f"🔄 Token dopo reload: {'PRESENTE' if token_dopo_reload else 'ASSENTE'}", 'info')

    except ImportError:
        flash("❌ Modulo dotenv NON INSTALLATO!", 'error')

    # Controlla se il file .env esiste
    import os
    env_file_path = os.path.join(os.getcwd(), '.env')
    env_exists = os.path.exists(env_file_path)
    flash(f"📁 File .env esiste: {env_exists} ({env_file_path})", 'info')

    if env_exists:
        with open(env_file_path, 'r') as f:
            content = f.read()
            has_token = 'TELEGRAM_BOT_TOKEN' in content
            flash(f"🔍 File .env contiene TELEGRAM_BOT_TOKEN: {has_token}", 'info')

    return redirect(url_for('groups.group_detail', group_id=group_id))
# Aggiungi questa route al tuo groups.py

@groups_bp.route('/<int:group_id>/templates/<int:template_id>/edit', methods=['GET', 'POST'])
def edit_template(group_id, template_id):
    """Modifica un template esistente"""
    from app.models import MessageTemplate, TemplateMessage

    group = Group.query.get_or_404(group_id)
    template = MessageTemplate.query.filter_by(
        id=template_id,
        group_id=group_id,
        is_active=True
    ).first_or_404()

    if request.method == 'POST':
        # Aggiorna nome e descrizione del template
        template_name = request.form.get('template_name', '').strip()
        template_description = request.form.get('template_description', '').strip()

        if not template_name:
            flash('Il nome del template è obbligatorio', 'error')
            return render_template('groups/edit_template.html', group=group, template=template)

        # Verifica che non esista già un template con questo nome per il gruppo (escludendo se stesso)
        existing_template = MessageTemplate.query.filter_by(
            group_id=group_id,
            name=template_name,
            is_active=True
        ).filter(MessageTemplate.id != template_id).first()

        if existing_template:
            flash('Esiste già un template con questo nome per questo gruppo', 'error')
            return render_template('groups/edit_template.html', group=group, template=template)

        # Aggiorna il template
        template.name = template_name
        template.description = template_description

        # Elimina tutti i messaggi esistenti del template
        TemplateMessage.query.filter_by(template_id=template.id).delete()

        # Salva i nuovi messaggi per ogni utente
        messages_saved = 0
        for user in group.users:
            message_text = request.form.get(f'message_{user.id}', '').strip()
            if message_text:
                template_message = TemplateMessage(
                    template_id=template.id,
                    user_id=user.id,
                    message_text=message_text,
                    order_index=messages_saved
                )
                db.session.add(template_message)
                messages_saved += 1

        if messages_saved == 0:
            flash('Devi inserire almeno un messaggio per salvare il template', 'error')
            return render_template('groups/edit_template.html', group=group, template=template)

        db.session.commit()
        flash(f'Template "{template_name}" aggiornato con {messages_saved} messaggi', 'success')
        return redirect(url_for('groups.view_template', group_id=group_id, template_id=template.id))

    # GET - Prepara i dati per la modifica
    # Crea un dizionario con i messaggi esistenti per ogni utente
    existing_messages = {}
    for template_msg in template.template_messages:
        existing_messages[template_msg.user_id] = template_msg.message_text

    return render_template('groups/edit_template.html',
                         group=group,
                         template=template,
                         existing_messages=existing_messages)