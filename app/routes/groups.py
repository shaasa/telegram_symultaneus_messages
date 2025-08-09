from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Group, User, MessageLog
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

@groups_bp.route('/<int:group_id>/send_messages', methods=['POST'])
def send_messages(group_id):
    """Invia messaggi personalizzati agli utenti del gruppo"""
    group = Group.query.get_or_404(group_id)

    if not group.users:
        flash('Il gruppo non ha utenti', 'error')
        return redirect(url_for('groups.group_detail', group_id=group_id))

    messages_sent = 0
    messages_failed = 0

    # Importa qui per evitare import circolari
    from app.utils.telegram_helper import send_telegram_message

    for user in group.users:
        message_text = request.form.get(f'message_{user.id}', '').strip()

        if not message_text:
            continue

        # Crea log del messaggio
        message_log = MessageLog(
            group_id=group.id,
            user_id=user.id,
            message_text=message_text,
            status='pending'
        )
        db.session.add(message_log)

        # Invia messaggio via Telegram
        try:
            success = send_telegram_message(user.telegram_id, message_text)
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
        flash(f'{messages_sent} messaggi inviati con successo', 'success')
    if messages_failed > 0:
        flash(f'{messages_failed} messaggi non inviati', 'error')

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