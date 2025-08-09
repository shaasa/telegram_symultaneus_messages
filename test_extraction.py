#!/usr/bin/env python3
"""
Test per verificare l'estrazione delle traduzioni
"""

import os
import subprocess

def test_babel_extraction():
    """Test diretto di estrazione babel"""
    print("🧪 TEST ESTRAZIONE BABEL")
    print("=" * 50)

    # Test comando babel
    commands_to_test = [
        'pybabel extract -F babel.cfg -k _ -o test_messages.pot .',
        'pybabel extract -F babel.cfg -k _ -k gettext -o test_messages2.pot .',
        'pybabel extract -F babel.cfg -k _ -k lazy_gettext -o test_messages3.pot app/',
    ]

    for i, cmd in enumerate(commands_to_test, 1):
        print(f"\n🔧 Test {i}: {cmd}")

        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✅ Comando riuscito")

                # Controlla output file
                output_file = cmd.split(' -o ')[1].split(' ')[0]
                if os.path.exists(output_file):
                    with open(output_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        msgid_count = content.count('msgid "') - 1
                        print(f"📊 Messaggi trovati: {msgid_count}")

                        if msgid_count > 0:
                            print("📝 Primi messaggi:")
                            lines = content.split('\n')
                            for line in lines:
                                if line.startswith('msgid "') and len(line) > 8:
                                    msg = line[7:-1]
                                    if msg:
                                        print(f"   - {msg}")
                                        break

                    # Pulisci file test
                    os.remove(output_file)
                else:
                    print("❌ File output non creato")
            else:
                print(f"❌ Comando fallito: {result.stderr}")

        except Exception as e:
            print(f"❌ Errore: {e}")

def check_template_files():
    """Verifica che i file template esistano e contengano {{ _() }}"""
    print("\n📁 VERIFICA FILE TEMPLATE")
    print("=" * 50)

    template_dir = 'app/templates'
    if not os.path.exists(template_dir):
        print(f"❌ Directory {template_dir} non esistente")
        return

    template_files = []
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                template_files.append(os.path.join(root, file))

    print(f"📋 Trovati {len(template_files)} file template:")

    total_translations = 0
    for template_file in template_files:
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()

                # Conta {{ _('...') }}
                count1 = content.count("{{ _('")
                count2 = content.count('{{ _("')
                total_count = count1 + count2
                total_translations += total_count

                print(f"   {template_file}: {total_count} traduzioni")

                if total_count > 0:
                    # Mostra primi esempi
                    import re
                    patterns = [
                        r"\{\{\s*_\(['\"]([^'\"]+)['\"]",
                        r"\{\{\s*_\(\'([^\']+)\'",
                        r'\{\{\s*_\("([^"]+)"'
                    ]

                    examples = []
                    for pattern in patterns:
                        matches = re.findall(pattern, content)
                        examples.extend(matches[:3])

                    if examples:
                        print(f"      Esempi: {examples[:3]}")

        except Exception as e:
            print(f"   ❌ Errore leggendo {template_file}: {e}")

    print(f"\n📊 TOTALE: {total_translations} stringhe da tradurre trovate")

def main():
    check_template_files()
    test_babel_extraction()

if __name__ == '__main__':
    main()