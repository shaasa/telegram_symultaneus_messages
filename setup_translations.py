#!/usr/bin/env python3
"""
Script per gestire le traduzioni con Flask-Babel

FLUSSO TRADUZIONI:
1. Scrivi {{ _('Testo italiano') }} nei template
2. python setup_translations.py --extract
3. python setup_translations.py --init-all
4. Traduci manualmente i file .po
5. python setup_translations.py --compile
6. Riavvia l'app
"""

import os
import sys
import subprocess

def run_command(command):
    """Esegue un comando e mostra l'output"""
    print(f"🔧 Eseguendo: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print("❌ ERRORE:", result.stderr)

    return result.returncode == 0

def extract_messages():
    """Estrae tutti i messaggi da tradurre"""
    print("📤 1. Estrazione messaggi da tradurre...")

    # Crea directory translations se non esiste
    if not os.path.exists('app/translations'):
        os.makedirs('app/translations')
        print("✅ Creata cartella app/translations/")

    # Estrai messaggi con opzioni dettagliate
    cmd = 'pybabel extract -F babel.cfg -k _ -k lazy_gettext -k ngettext -o app/translations/messages.pot --input-dirs=. --add-comments=TRANSLATORS'
    success = run_command(cmd)

    if success and os.path.exists('app/translations/messages.pot'):
        print("✅ File messages.pot creato con successo")

        # Mostra quanti messaggi sono stati trovati
        with open('app/translations/messages.pot', 'r', encoding='utf-8') as f:
            content = f.read()
            msgid_count = content.count('msgid "') - 1  # -1 per il header vuoto
            print(f"📊 Trovati {msgid_count} messaggi da tradurre")

            # Mostra alcuni esempi
            if msgid_count > 0:
                print("📝 Esempi di messaggi trovati:")
                lines = content.split('\n')
                examples = []
                for i, line in enumerate(lines):
                    if line.startswith('msgid "') and len(line) > 8:
                        msg = line[7:-1]  # Rimuovi 'msgid "' e '"'
                        if msg and msg != '':
                            examples.append(msg)
                        if len(examples) >= 5:
                            break

                for example in examples:
                    print(f"   - {example}")
    else:
        print("❌ Errore nella creazione di messages.pot")

    return success

def init_language(lang):
    """Inizializza una nuova lingua"""
    print(f"🌍 Inizializzazione lingua: {lang}")

    cmd = f'pybabel init -i app/translations/messages.pot -d app/translations -l {lang}'
    success = run_command(cmd)

    if success:
        print(f"✅ Lingua {lang} inizializzata")
        po_file = f'app/translations/{lang}/LC_MESSAGES/messages.po'
        if os.path.exists(po_file):
            print(f"📝 File da tradurre: {po_file}")

    return success

def update_translations():
    """Aggiorna tutte le traduzioni esistenti"""
    print("🔄 Aggiornamento traduzioni esistenti...")

    cmd = 'pybabel update -i app/translations/messages.pot -d app/translations'
    success = run_command(cmd)

    if success:
        print("✅ Traduzioni aggiornate")

    return success

def compile_translations():
    """Compila tutte le traduzioni"""
    print("⚙️  Compilazione traduzioni...")

    cmd = 'pybabel compile -d app/translations'
    success = run_command(cmd)

    if success:
        print("✅ Traduzioni compilate")

        # Mostra le lingue compilate
        translations_dir = 'app/translations'
        if os.path.exists(translations_dir):
            languages = [d for d in os.listdir(translations_dir)
                         if os.path.isdir(os.path.join(translations_dir, d))]
            print(f"🌍 Lingue disponibili: {', '.join(languages)}")

    return success

def show_translation_status():
    """Mostra lo stato delle traduzioni"""
    print("\n📊 STATO TRADUZIONI:")
    print("=" * 50)

    translations_dir = 'app/translations'

    # Controlla se esiste messages.pot
    pot_file = os.path.join(translations_dir, 'messages.pot')
    if os.path.exists(pot_file):
        print("✅ Template traduzioni (messages.pot): PRESENTE")

        with open(pot_file, 'r', encoding='utf-8') as f:
            content = f.read()
            msgid_count = content.count('msgid ""') - 1
            print(f"   📝 Messaggi da tradurre: {msgid_count}")
    else:
        print("❌ Template traduzioni (messages.pot): MANCANTE")
        print("   🔧 Esegui: python setup_translations.py --extract")
        return

    # Controlla le lingue
    if os.path.exists(translations_dir):
        languages = [d for d in os.listdir(translations_dir)
                     if os.path.isdir(os.path.join(translations_dir, d))]

        if languages:
            print(f"\n🌍 Lingue configurate: {len(languages)}")
            for lang in sorted(languages):
                lang_dir = os.path.join(translations_dir, lang, 'LC_MESSAGES')
                po_file = os.path.join(lang_dir, 'messages.po')
                mo_file = os.path.join(lang_dir, 'messages.mo')

                print(f"\n   📂 {lang.upper()}:")

                if os.path.exists(po_file):
                    print(f"      ✅ File da tradurre: messages.po")

                    # Conta traduzioni fatte
                    with open(po_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        total_msgs = content.count('msgid ')
                        translated_msgs = len([line for line in content.split('\n')
                                               if line.startswith('msgstr ') and '""' not in line])

                        if total_msgs > 0:
                            percentage = (translated_msgs / total_msgs) * 100
                            print(f"      📊 Progresso: {translated_msgs}/{total_msgs} ({percentage:.1f}%)")
                else:
                    print(f"      ❌ File da tradurre: MANCANTE")

                if os.path.exists(mo_file):
                    print(f"      ✅ File compilato: messages.mo")
                else:
                    print(f"      ❌ File compilato: MANCANTE")
        else:
            print("\n❌ Nessuna lingua configurata")
            print("   🔧 Esegui: python setup_translations.py --init-all")

def init_all_languages():
    """Inizializza tutte le lingue supportate"""
    languages = ['en', 'es', 'fr', 'de']

    print("🌍 Inizializzazione tutte le lingue...")

    # Controlla se esiste messages.pot
    if not os.path.exists('app/translations/messages.pot'):
        print("❌ Template traduzioni mancante, estraggo prima i messaggi...")
        if not extract_messages():
            return False

    success_count = 0
    for lang in languages:
        lang_dir = f'app/translations/{lang}'
        if not os.path.exists(lang_dir):
            if init_language(lang):
                success_count += 1
        else:
            print(f"ℹ️  Lingua {lang} già esistente, salto")
            success_count += 1

    print(f"\n✅ Inizializzate {success_count}/{len(languages)} lingue")
    return success_count == len(languages)

def main():
    print("🌍 GESTORE TRADUZIONI - Telegram Group Manager")
    print("=" * 60)

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == '--extract':
            extract_messages()

        elif command == '--update':
            if not os.path.exists('app/translations/messages.pot'):
                print("❌ Estrai prima i messaggi con --extract")
                return
            update_translations()

        elif command == '--compile':
            compile_translations()

        elif command == '--init-all':
            init_all_languages()

        elif command == '--status':
            show_translation_status()

        elif command == '--init' and len(sys.argv) > 2:
            lang = sys.argv[2]
            if not os.path.exists('app/translations/messages.pot'):
                print("❌ Estrai prima i messaggi con --extract")
                return
            init_language(lang)

        elif command == '--full-setup':
            print("🚀 SETUP COMPLETO...")
            if extract_messages() and init_all_languages():
                print("\n✅ SETUP COMPLETATO!")
                print("\n📋 PROSSIMI PASSI:")
                print("1. Traduci i file .po in app/translations/*/LC_MESSAGES/")
                print("2. Esegui: python setup_translations.py --compile")
                print("3. Riavvia l'applicazione")
                show_translation_status()

        else:
            print("❌ Comando non riconosciuto\n")
            show_help()

    else:
        show_help()

def show_help():
    print("📖 COMANDI DISPONIBILI:")
    print("")
    print("  --extract      : Estrai messaggi da tradurre dai template")
    print("  --init-all     : Inizializza tutte le lingue (en, es, fr, de)")
    print("  --init <lang>  : Inizializza una lingua specifica")
    print("  --update       : Aggiorna traduzioni esistenti")
    print("  --compile      : Compila traduzioni per l'uso")
    print("  --status       : Mostra stato traduzioni")
    print("  --full-setup   : Setup completo automatico")
    print("")
    print("📋 WORKFLOW TIPICO:")
    print("  1. python setup_translations.py --full-setup")
    print("  2. Modifica i file .po per tradurre")
    print("  3. python setup_translations.py --compile")
    print("  4. Riavvia l'app")

if __name__ == '__main__':
    main()