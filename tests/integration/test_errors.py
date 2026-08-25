import io
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestRejetsFormat:
    def test_docx_rejete_400(self, client):
        resp = client.post(
            '/upload',
            data={'file': (io.BytesIO(b'doc'), 'rapport.docx')},
            content_type='multipart/form-data',
        )
        assert resp.status_code == 400
        body = resp.get_json()
        assert 'Format non support' in body['error']
        assert '.xlsx' in body['error'] and '.csv' in body['error']

    def test_sans_extension_rejete_400(self, client):
        resp = client.post(
            '/upload',
            data={'file': (io.BytesIO(b'x'), 'fichiersansextension')},
            content_type='multipart/form-data',
        )
        assert resp.status_code == 400

    def test_exe_rejete_400(self, client):
        resp = client.post(
            '/upload',
            data={'file': (io.BytesIO(b'MZ\x90\x00'), 'virus.exe')},
            content_type='multipart/form-data',
        )
        assert resp.status_code == 400


class TestRejetsTaille:
    def test_fichier_trop_volumineux_413(self, client, app):
        app.config['MAX_CONTENT_LENGTH'] = 1024
        gros = io.BytesIO(b'x' * 2048)
        resp = client.post(
            '/upload',
            data={'file': (gros, 'gros.csv')},
            content_type='multipart/form-data',
        )
        assert resp.status_code == 413
        assert 'trop volumineux' in resp.get_json()['error'].lower()


class TestErreursAnalyse:
    def test_analyze_id_inconnu_404(self, client):
        resp = client.post('/analyze/id-qui-nexiste-pas')
        assert resp.status_code == 404
        assert 'Rechargez' in resp.get_json()['error']

    def test_xlsx_corrompu_422_lisible(self, client):
        up = client.post(
            '/upload',
            data={'file': (io.BytesIO(b'contenu bidon'), 'fake.xlsx')},
            content_type='multipart/form-data',
        )
        fid = up.get_json()['id']
        an = client.post(f'/analyze/{fid}')
        assert an.status_code == 422
        assert 'xlsx' in an.get_json()['error'].lower()

    def test_aucun_fichier_fourini_400(self, client):
        resp = client.post('/upload', data={}, content_type='multipart/form-data')
        assert resp.status_code == 400
