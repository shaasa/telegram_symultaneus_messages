import os
import requests
from flask import current_app
import logging

logger = logging.getLogger(__name__)

def get_bot_token():
    """
    Ottiene il token del bot dalle variabili ambiente (.env) o dalla configurazione Flask
    """
    # Prima prova dalle variabili ambiente (dal .env)
    token = os.environ.get('TELEGRAM_BOT_TOKEN')

    if token:
        logger.info(f"Token trovato in variabili ambiente (lunghezza: {len(token)})")
        return token

    # Se non trovato, prova dalla configurazione Flask (fallback)
    try:
        token = current_app.config.get('TELEGRAM_BOT_TOKEN')
        if token:
            logger.info(f"Token trovato in config Flask (lunghezza: {len(token)})")
            return token
    except RuntimeError:
        # Non siamo in un contesto Flask applicativo
        logger.warning("Nessun contesto Flask disponibile")

    # Se non trovato in nessun posto
    logger.error("TELEGRAM_BOT_TOKEN non trovato né in variabili ambiente né in config Flask")
    return None

def test_bot_connection():
    """
    Testa la connessione con il bot Telegram

    Returns:
        dict: {
            'success': bool,
            'bot_info': dict|None,
            'error': str|None
        }
    """
    token = get_bot_token()
    if not token:
        error_msg = "Token del bot Telegram non configurato"
        logger.error(error_msg)
        return {
            'success': False,
            'bot_info': None,
            'error': error_msg
        }

    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        logger.info("Test connessione bot...")
        response = requests.get(url, timeout=10)

        logger.info(f"Status code test bot: {response.status_code}")
        logger.info(f"Response test bot: {response.text}")

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                logger.info(f"✅ Bot connesso: @{bot_info.get('username', 'N/A')}")
                return {
                    'success': True,
                    'bot_info': bot_info,
                    'error': None
                }
            else:
                error_msg = f"Errore API: {data.get('description', 'Errore sconosciuto')}"
                logger.error(f"❌ {error_msg}")
                return {
                    'success': False,
                    'bot_info': None,
                    'error': error_msg
                }
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            logger.error(f"❌ Errore connessione: {error_msg}")
            return {
                'success': False,
                'bot_info': None,
                'error': error_msg
            }

    except Exception as e:
        error_msg = f"Errore nel test di connessione: {str(e)}"
        logger.error(f"❌ {error_msg}", exc_info=True)
        return {
            'success': False,
            'bot_info': None,
            'error': error_msg
        }

# Sostituisci la tua funzione send_telegram_message esistente con questa versione:

def send_telegram_message(chat_id, message_text):
    """
    Invia un messaggio Telegram a un utente specifico

    Returns:
        dict: {
            'success': bool,
            'message_id': str|None,
            'error': str|None,
            'error_code': int|None
        }
    """
    token = get_bot_token()
    if not token:
        error_msg = "Token del bot Telegram non configurato"
        logger.error(error_msg)
        return {
            'success': False,
            'message_id': None,
            'error': error_msg,
            'error_code': None
        }

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"

        payload = {
            'chat_id': chat_id,
            'text': message_text,
            'parse_mode': 'HTML'  # Supporta formattazione HTML di base
        }

        logger.info(f"Tentativo invio messaggio a chat_id: {chat_id}")
        response = requests.post(url, json=payload, timeout=30)

        # Log della risposta per debug
        logger.info(f"Status code: {response.status_code}")
        logger.info(f"Response body: {response.text}")

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                message_id = data.get('result', {}).get('message_id')
                logger.info(f"✅ Messaggio inviato con successo a {chat_id}, message_id: {message_id}")
                return {
                    'success': True,
                    'message_id': str(message_id) if message_id else None,
                    'error': None,
                    'error_code': None
                }
            else:
                # Errore API Telegram
                error_code = data.get('error_code')
                error_description = data.get('description', 'Errore API Telegram sconosciuto')
                full_error = f"API Error {error_code}: {error_description}"

                logger.error(f"❌ Errore API Telegram per {chat_id}: {full_error}")
                return {
                    'success': False,
                    'message_id': None,
                    'error': full_error,
                    'error_code': error_code
                }
        else:
            # Errore HTTP
            try:
                error_data = response.json()
                error_description = error_data.get('description', response.text)
                error_code = error_data.get('error_code')
            except:
                error_description = response.text
                error_code = response.status_code

            full_error = f"HTTP {response.status_code}: {error_description}"
            logger.error(f"❌ Errore HTTP per {chat_id}: {full_error}")

            return {
                'success': False,
                'message_id': None,
                'error': full_error,
                'error_code': error_code
            }

    except requests.exceptions.Timeout:
        error_msg = "Timeout nella richiesta (30s) - Telegram non risponde"
        logger.error(f"❌ Timeout per {chat_id}: {error_msg}")
        return {
            'success': False,
            'message_id': None,
            'error': error_msg,
            'error_code': None
        }
    except requests.exceptions.ConnectionError:
        error_msg = "Errore di connessione - Impossibile raggiungere Telegram"
        logger.error(f"❌ Connection error per {chat_id}: {error_msg}")
        return {
            'success': False,
            'message_id': None,
            'error': error_msg,
            'error_code': None
        }
    except Exception as e:
        error_msg = f"Errore imprevisto: {str(e)}"
        logger.error(f"❌ Errore generico per {chat_id}: {error_msg}", exc_info=True)
        return {
            'success': False,
            'message_id': None,
            'error': error_msg,
            'error_code': None
        }

def get_bot_users():
    """
    Ottiene la lista degli utenti che hanno interagito con il bot.

    IMPORTANTE: Telegram non fornisce direttamente una lista completa di utenti.
    Questa funzione cerca negli updates recenti e potrebbe non trovare tutti gli utenti.

    Per una soluzione completa, implementa un webhook o salva gli utenti
    quando interagiscono con il bot.
    """
    token = get_bot_token()
    if not token:
        logger.error("Token del bot Telegram non configurato")
        return []

    users = {}

    try:
        # Metodo 1: Ottieni updates recenti con offset per recuperare più messaggi
        url = f"https://api.telegram.org/bot{token}/getUpdates"

        # Prova a recuperare fino a 1000 updates recenti
        for offset in [None, -100, -200, -300, -400, -500]:
            params = {
                'limit': 100,
                'timeout': 0  # Non aspettare nuovi messaggi
            }

            if offset:
                params['offset'] = offset

            try:
                response = requests.get(url, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok'):
                        updates = data.get('result', [])

                        if not updates:
                            continue

                        logger.info(f"Trovati {len(updates)} updates con offset {offset}")

                        # Estrai utenti dai messaggi
                        for update in updates:
                            user_data = None

                            # Controlla diversi tipi di update
                            if 'message' in update:
                                user_data = update['message']['from']
                            elif 'callback_query' in update:
                                user_data = update['callback_query']['from']
                            elif 'inline_query' in update:
                                user_data = update['inline_query']['from']
                            elif 'edited_message' in update:
                                user_data = update['edited_message']['from']

                            if user_data and not user_data.get('is_bot', False):
                                user_id = user_data['id']
                                users[user_id] = {
                                    'id': user_id,
                                    'username': user_data.get('username'),
                                    'first_name': user_data.get('first_name', ''),
                                    'last_name': user_data.get('last_name', ''),
                                    'is_bot': user_data.get('is_bot', False)
                                }
                    else:
                        logger.error(f"Errore API con offset {offset}: {data.get('description')}")
                else:
                    logger.error(f"Errore HTTP {response.status_code} con offset {offset}")

            except requests.RequestException as e:
                logger.error(f"Errore richiesta con offset {offset}: {str(e)}")
                continue

        # Converti in lista
        real_users = list(users.values())

        logger.info(f"Trovati {len(real_users)} utenti unici totali")

        # Ordina per ID (utenti più recenti hanno ID più alti)
        real_users.sort(key=lambda x: x['id'], reverse=True)

        return real_users

    except Exception as e:
        logger.error(f"Errore generale nel recupero utenti: {str(e)}")
        return []

def get_specific_updates(limit=100, offset=None):
    """
    Recupera updates specifici per debug
    """
    token = get_bot_token()
    if not token:
        return []

    try:
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        params = {
            'limit': limit,
            'timeout': 0
        }

        if offset:
            params['offset'] = offset

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return data.get('result', [])

        return []

    except Exception as e:
        logger.error(f"Errore nel recupero updates: {str(e)}")
        return []

def manual_add_user_from_chat_id(chat_id):
    """
    Recupera informazioni utente da un chat_id specifico
    Utile per aggiungere manualmente utenti conosciuti
    """
    token = get_bot_token()
    if not token:
        logger.error("Token del bot Telegram non configurato")
        return None

    try:
        # Prova a inviare un messaggio di test per ottenere info
        url = f"https://api.telegram.org/bot{token}/getChat"
        params = {'chat_id': chat_id}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                chat_info = data['result']

                # Converti in formato utente
                if chat_info.get('type') == 'private':
                    return {
                        'id': chat_info['id'],
                        'username': chat_info.get('username'),
                        'first_name': chat_info.get('first_name', ''),
                        'last_name': chat_info.get('last_name', ''),
                        'is_bot': False
                    }

        logger.error(f"Impossibile ottenere info per chat_id {chat_id}")
        return None

    except Exception as e:
        logger.error(f"Errore nel recupero info utente {chat_id}: {str(e)}")
        return None

def get_chat_info(chat_id):
    """Ottiene informazioni su una chat specifica"""
    token = get_bot_token()
    if not token:
        return None

    try:
        url = f"https://api.telegram.org/bot{token}/getChat"
        params = {'chat_id': chat_id}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return data['result']

        return None

    except Exception as e:
        logger.error(f"Errore nel recupero info chat {chat_id}: {str(e)}")
        return None

def send_message_with_retry(chat_id, message_text, max_retries=3, delay=1):
    """Invia messaggio con retry automatico in caso di errore"""
    import time

    for attempt in range(max_retries):
        try:
            success = send_telegram_message(chat_id, message_text)
            if success:
                return True

            # Se fallisce, aspetta prima del retry
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))  # Backoff progressivo

        except Exception as e:
            logger.error(f"Tentativo {attempt + 1} fallito per {chat_id}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))

    return False

def batch_send_messages(messages_data, batch_size=5, delay_between_batches=1):
    """
    Invia messaggi in batch per rispettare rate limits

    Args:
        messages_data: Lista di dict con 'chat_id' e 'message_text'
        batch_size: Numero messaggi per batch
        delay_between_batches: Secondi di pausa tra batch

    Returns:
        Dict con statistiche invio
    """
    import time

    results = {
        'sent': 0,
        'failed': 0,
        'total': len(messages_data),
        'errors': []
    }

    for i in range(0, len(messages_data), batch_size):
        batch = messages_data[i:i + batch_size]

        for msg_data in batch:
            try:
                success = send_message_with_retry(
                    msg_data['chat_id'],
                    msg_data['message_text']
                )

                if success:
                    results['sent'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append({
                        'chat_id': msg_data['chat_id'],
                        'error': 'Invio fallito dopo retry'
                    })

            except Exception as e:
                results['failed'] += 1
                results['errors'].append({
                    'chat_id': msg_data['chat_id'],
                    'error': str(e)
                })

        # Pausa tra batch per rispettare rate limits
        if i + batch_size < len(messages_data):
            time.sleep(delay_between_batches)

    return results