import io
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestIndexPage:
    def test_index_returns_200(self, client):
        resp = client.get('/')
        assert resp.status_code == 200

    def test_index_contains_dropzone(self, client):
        resp = client.get('/')
        assert b'id="dropzone"' in resp.data
        assert b'D\xc3\xa9marrer l\'analyse' in resp.data or 'Démarrer'.encode('utf-8') in resp.data


class TestUploadEndpoint:
    def test_upload_valid_csv(self, client):
        data = {
            'file': (io.BytesIO(b'a,b\n1,2\n'), 'activity.csv')
        }
        resp = client.post('/upload', data=data, content_type='multipart/form-data')
        assert resp.status_code == 200
        body = resp.get_json()
        assert body['success'] is True
        assert body['nom_fichier'] == 'activity.csv'
        assert body['format'] == 'csv'
        assert 'id' in body

    def test_upload_invalid_format_rejected(self, client):
        data = {
            'file': (io.BytesIO(b'fake doc'), 'document.docx')
        }
        resp = client.post('/upload', data=data, content_type='multipart/form-data')
        assert resp.status_code == 400
        body = resp.get_json()
        assert 'error' in body
        assert 'Format non support' in body['error']

    def test_upload_no_file_rejected(self, client):
        resp = client.post('/upload', data={}, content_type='multipart/form-data')
        assert resp.status_code == 400

    def test_upload_empty_filename_rejected(self, client):
        data = {
            'file': (io.BytesIO(b''), '')
        }
        resp = client.post('/upload', data=data, content_type='multipart/form-data')
        assert resp.status_code == 400


class TestHealthEndpoint:
    def test_health_returns_healthy(self, client):
        resp = client.get('/health')
        assert resp.status_code == 200
        assert resp.get_json()['status'] == 'healthy'
