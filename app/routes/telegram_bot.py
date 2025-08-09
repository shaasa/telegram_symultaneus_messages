from flask import Blueprint, request, redirect, url_for, flash, jsonify, render_template
from app.models import User
from app import db
from datetime import datetime

telegram_bp = Blueprint('telegram', __name__)

@telegram_bp.route('/import_users', methods=['POST'])
def import_users():
    """Importa utenti dal bot Telegram"""
    try:
        from app.utils.telegram_helper import get_bot_users

        bot_users = get_bot_users()
        imported_count = 0
        updated_count = 0

        if not bot_users:
            flash('Nessun utente trovato negli updates recenti del bot. Prova ad aggiungere utenti manualmente.', 'warning')
            return redirect(url_for('main.index'))

        for user_data in bot_users:
            telegram_id = str(user_data.get('id'))
            username = user_data.get('username')
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')

            # Cerca se l'utente esiste già
            existing_user = User.query.filter_by(telegram_id=telegram_id).first()

            if existing_user:
                # Aggiorna i dati esistenti
                existing_user.username = username
                existing_user.first_name = first_name
                existing_user.last_name = last_name
                existing_user.last_interaction = datetime.utcnow()
                updated_count += 1
            else:
                # Crea nuovo utente
                new_user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    display_name=f"{first_name} {last_name}".strip() or username or f"User {telegram_id}",
                    last_interaction=datetime.utcnow()
                )
                db.session.add(new_user)
                imported_count += 1

        db.session.commit()

        message = f"Importazione completata: {imported_count} nuovi utenti, {updated_count} aggiornati"
        flash(message, 'success')

    except Exception as e:
        flash(f'Errore durante l\'importazione: {str(e)}', 'error')

    return redirect(url_for('main.index'))

@telegram_bp.route('/add_user_by_chat_id', methods=['POST'])
def add_user_by_chat_id():
    """Aggiunge un utente specifico tramite chat_id"""
    chat_id = request.form.get('chat_id', '').strip()

    if not chat_id:
        flash('Inserisci un Chat ID valido', 'error')
        return redirect(url_for('main.index'))

    try:
        from app.utils.telegram_helper import manual_add_user_from_chat_id

        user_data = manual_add_user_from_chat_id(chat_id)

        if not user_data:
            flash(f'Impossibile recuperare informazioni per Chat ID {chat_id}. Verifica che sia corretto e che il bot possa accedere alla chat.', 'error')
            return redirect(url_for('main.index'))

        telegram_id = str(user_data.get('id'))

        # Verifica che l'utente non esista già
        existing_user = User.query.filter_by(telegram_id=telegram_id).first()

        if existing_user:
            flash(f'L\'utente {existing_user.full_name} esiste già nel database', 'warning')
            return redirect(url_for('main.index'))

        # Crea nuovo utente
        new_user = User(
            telegram_id=telegram_id,
            username=user_data.get('username'),
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            display_name=f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip() or user_data.get('username') or f"User {telegram_id}",
            last_interaction=datetime.utcnow()
        )

        db.session.add(new_user)
        db.session.commit()

        flash(f'Utente {new_user.full_name} aggiunto con successo!', 'success')

    except Exception as e:
        flash(f'Errore nell\'aggiunta dell\'utente: {str(e)}', 'error')

    return redirect(url_for('main.index'))

@telegram_bp.route('/create_user', methods=['POST'])
def create_user():
    """Crea un nuovo utente manualmente"""
    telegram_id = request.form.get('telegram_id', '').strip()
    username = request.form.get('username', '').strip()
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    display_name = request.form.get('display_name', '').strip()

    if not telegram_id:
        flash('L\'ID Telegram è obbligatorio', 'error')
        return redirect(url_for('main.index'))

    # Verifica che l'utente non esista già
    if User.query.filter_by(telegram_id=telegram_id).first():
        flash('Un utente con questo ID Telegram esiste già', 'error')
        return redirect(url_for('main.index'))

    # Se non c'è un display_name, crealo dai dati disponibili
    if not display_name:
        if first_name and last_name:
            display_name = f"{first_name} {last_name}"
        elif first_name:
            display_name = first_name
        elif username:
            display_name = f"@{username}"
        else:
            display_name = f"User {telegram_id}"

    user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        display_name=display_name
    )

    db.session.add(user)
    db.session.commit()

    flash(f'Utente "{display_name}" creato con successo', 'success')
    return redirect(url_for('main.index'))

@telegram_bp.route('/users')
def list_users():
    """API per ottenere la lista degli utenti"""
    users = User.query.filter_by(is_active=True).all()
    return jsonify([user.to_dict() for user in users])

@telegram_bp.route('/test_connection')
def test_connection():
    """Testa la connessione con il bot Telegram"""
    try:
        from app.utils.telegram_helper import test_bot_connection

        if test_bot_connection():
            flash('Connessione al bot Telegram riuscita', 'success')
        else:
            flash('Errore nella connessione al bot Telegram. Verifica il token.', 'error')

    except Exception as e:
        flash(f'Errore nel test di connessione: {str(e)}', 'error')

    return redirect(url_for('main.index'))

@telegram_bp.route('/debug_updates')
def debug_updates():
    """Debug: mostra gli updates recenti del bot"""
    try:
        from app.utils.telegram_helper import get_specific_updates

        updates = get_specific_updates(limit=50)

        if updates:
            flash(f'Trovati {len(updates)} updates recenti. Controlla i log per dettagli.', 'info')
            # Log degli updates per debug
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Updates recenti: {updates}")
        else:
            flash('Nessun update trovato. Il bot potrebbe non aver ricevuto messaggi di recente.', 'warning')

    except Exception as e:
        flash(f'Errore nel debug updates: {str(e)}', 'error')

    return redirect(url_for('main.index'))