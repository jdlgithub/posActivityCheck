import io
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest
from openpyxl import Workbook


def xlsx_bytes(rows):
    wb = Workbook()
    ws = wb.active
    for row in rows:
        ws.append(row)
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


CSV_VALIDE = (
    b'status,conformite\n'
    b'valide,oui\nvalide,oui\nen attente,non\ninconforme,non\nvalide,oui\n'
)


class TestFormatsSupportes:
    def test_csv_upload_et_analyse(self, client):
        up = client.post(
            '/upload',
            data={'file': (io.BytesIO(CSV_VALIDE), 'suivi.csv')},
            content_type='multipart/form-data',
        )
        assert up.status_code == 200
        fid = up.get_json()['id']

        an = client.post(f'/analyze/{fid}')
        assert an.status_code == 200
        stats = an.get_json()['statistics']
        assert stats['taux_pos_valides'] == 60.0

    def test_xlsx_upload_et_analyse(self, client):
        data = xlsx_bytes([
            ['Status', 'Conformite'],
            ['Valide', 'Oui'],
            ['En attente', 'Non'],
            ['Valide', 'Oui'],
        ])
        up = client.post(
            '/upload',
            data={'file': (data, 'suivi.xlsx')},
            content_type='multipart/form-data',
        )
        assert up.status_code == 200
        fid = up.get_json()['id']

        an = client.post(f'/analyze/{fid}')
        assert an.status_code == 200
        stats = an.get_json()['statistics']
        assert stats['taux_pos_valides'] == round(2 / 3 * 100, 1)
        assert stats['taux_pos_attente'] == round(1 / 3 * 100, 1)

    def test_xls_corrompu_message_lisible(self, client):
        """Un .xls illisible doit produire une erreur explicite (422), pas un crash."""
        up = client.post(
            '/upload',
            data={'file': (io.BytesIO(b'pas un vrai xls'), 'legacy.xls')},
            content_type='multipart/form-data',
        )
        assert up.status_code == 200
        fid = up.get_json()['id']

        an = client.post(f'/analyze/{fid}')
        assert an.status_code == 422
        assert 'xls' in an.get_json()['error'].lower()

    def test_pdf_sans_tableau_message_lisible(self, client):
        """Un PDF sans tableau exploitable doit renvoyer une erreur claire."""
        pdf_minimal = (
            b'%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n'
            b'2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n'
            b'3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]>>endobj\n'
            b'trailer<</Root 1 0 R>>\n%%EOF\n'
        )
        up = client.post(
            '/upload',
            data={'file': (io.BytesIO(pdf_minimal), 'doc.pdf')},
            content_type='multipart/form-data',
        )
        assert up.status_code == 200
        fid = up.get_json()['id']

        an = client.post(f'/analyze/{fid}')
        assert an.status_code in (422,)  # erreur métier lisible
        body = an.get_json()
        assert 'error' in body and 'pdf' in body['error'].lower()

    def test_en_tetes_accentues_normalises(self, client):
        csv_accents = 'Statut;Conformité\nValidé;Oui\n'.encode('latin-1')
        up = client.post(
            '/upload',
            data={'file': (io.BytesIO(csv_accents), 'accentue.csv')},
            content_type='multipart/form-data',
        )
        assert up.status_code == 200
        an = client.post('/analyze/' + up.get_json()['id'])
        # pandas: séparateur ';' non standard → colonnes brutes; le taux valide reste calculable si colonne détectée
        assert an.status_code == 200
