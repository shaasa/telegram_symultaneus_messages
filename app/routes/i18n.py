from flask import Blueprint, request, redirect, session, url_for, current_app, flash

i18n_bp = Blueprint('i18n', __name__)

@i18n_bp.route('/set/<language>')
def set_language(language=None):
    """Cambia la lingua dell'interfaccia"""

    # Verifica che la lingua sia supportata
    supported_languages = ['it', 'en', 'es', 'fr', 'de']
    if language not in supported_languages:
        language = current_app.config.get('BABEL_DEFAULT_LOCALE', 'it')
        flash(f'Lingua non supportata, impostata su {language}', 'warning')

    # Salva la lingua scelta nella sessione
    session['language'] = language
    session.permanent = True  # Rendi la sessione permanente

    print(f"DEBUG: Lingua impostata su: {language}")  # Debug
    print(f"DEBUG: Sessione dopo cambio: {session.get('language')}")  # Debug

    flash(f'Lingua cambiata in: {language.upper()}', 'success')

    # Redirect alla pagina precedente o homepage
    return redirect(request.referrer or url_for('main.index'))