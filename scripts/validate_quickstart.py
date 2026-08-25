"""Validation quickstart.md (SV-001 a SV-006) + performance T045 (10k lignes).

Exécuter depuis la racine : python scripts/validate_quickstart.py
"""
import io
import sys
import time

sys.path.insert(0, 'src')

from openpyxl import Workbook

from app import app

client = app.test_client()
resultats = []


def check(nom, condition):
    resultats.append((nom, bool(condition)))
    print(('OK  ' if condition else 'FAIL'), nom)


# SV-001 / SV-004 : chargement fichier valide (csv)
csv_content = b'status,conformite\nvalide,oui\nen attente,non\n'
up = client.post('/upload', data={'file': (io.BytesIO(csv_content), 'suivi.csv')},
                 content_type='multipart/form-data')
body = up.get_json()
check('SV-001 upload csv -> nom + id', up.status_code == 200 and body['nom_fichier'] == 'suivi.csv' and body['id'])
check('SV-004 format csv reconnu', body['format'] == 'csv')

# Analyse -> stats
an = client.post('/analyze/' + body['id'])
stats = an.get_json()['statistics']
check('SV-002 analyse -> 4 taux', an.status_code == 200 and len(stats) == 4)

# SV-003 : format non supporte
up_docx = client.post('/upload', data={'file': (io.BytesIO(b'x'), 'doc.docx')},
                      content_type='multipart/form-data')
check('SV-003 docx rejete avec message', up_docx.status_code == 400 and 'Format non support' in up_docx.get_json()['error'])

# SV-005 : xlsx
wb = Workbook(); ws = wb.active
ws.append(['Status', 'Conformite']); ws.append(['Valide', 'Oui'])
buf = io.BytesIO(); wb.save(buf); buf.seek(0)
up_x = client.post('/upload', data={'file': (buf, 's.xlsx')}, content_type='multipart/form-data')
an_x = client.post('/analyze/' + up_x.get_json()['id'])
check('SV-005 xlsx analyse OK', up_x.status_code == 200 and an_x.status_code == 200)

# Rendu page
page = client.get('/')
html = page.data.decode('utf-8')
check('Page contient dropzone + bouton + cartes', all(
    k in html for k in ('dropzone', 'Démarrer l\'analyse'.replace("'", "'"), 'stat-valides')))

# T045 : performance 10k lignes
lignes = ['status,conformite'] + [
    f"{['valide','en attente','inconforme'][i % 3]},{'oui' if i % 2 else 'non'}"
    for i in range(10_000)
]
gros_csv = ('\n'.join(lignes)).encode('utf-8')
t0 = time.perf_counter()
up_gros = client.post('/upload', data={'file': (io.BytesIO(gros_csv), 'gros.csv')},
                      content_type='multipart/form-data')
fid = up_gros.get_json()['id']
an_gros = client.post(f'/analyze/{fid}')
duree = time.perf_counter() - t0
check(f'T045 10k lignes analysees en {duree:.2f}s (< 10s)', duree < 10 and an_gros.status_code == 200)
print('    Stats:', {k: v for k, v in an_gros.get_json()['statistics'].items()})

echecs = [n for n, ok in resultats if not ok]
print()
print(f'{len(resultats) - len(echecs)}/{len(resultats)} validations passées')
sys.exit(1 if echecs else 0)
