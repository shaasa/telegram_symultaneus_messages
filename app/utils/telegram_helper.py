import requests
from flask import current_app
import logging

logger = logging.getLogger(__name__)

def get_bot_token():
    """Ottiene il token del bot dalla configurazione"""
    return current_app.config.get('TELEGRAM_BOT_TOKEN')

def test_bot_connection():
    """Testa la connessione con il bot Telegram"""
    token = get_bot_token()
    if not token:
        logger.error("Token del bot Telegram non configurato")
        return False

    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                logger.info(f"Bot connesso: {data['result']['username']}")
                return True

        logger.error(f"Errore nella connessione: {response.text}")
        return False

    except Exception as e:
        logger.error(f"Errore nel test di connessione: {str(e)}")
        return False

def send_telegram_message(chat_id, message_text):
    """Invia un messaggio Telegram a un utente specifico"""
    token = get_bot_token()
    if not token:
        logger.error("Token del bot Telegram non configurato")
        return False

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"

        payload = {
            'chat_id': chat_id,
            'text': message_text,
            'parse_mode': 'HTML'  # Supporta formattazione HTML di base
        }

        response = requests.post(url, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                logger.info(f"Messaggio inviato a {chat_id}")
                return True
            else:
                logger.error(f"Errore API Telegram: {data.get('description', 'Errore sconosciuto')}")
                return False
        else:
            logger.error(f"Errore HTTP {response.status_code}: {response.text}")
            return False

    except Exception as e:
        logger.error(f"Errore nell'invio del messaggio: {str(e)}")
        return False

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