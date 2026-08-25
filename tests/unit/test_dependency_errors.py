import io
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest

from services import file_parser


class TestDependanceManquante:
    """Quand une lib de parsing manque sur le serveur, le message doit
    désigner la dépendance — pas accuser le fichier utilisateur."""

    def _sans_module(self, monkeypatch, nom_module):
        monkeypatch.setitem(sys.modules, nom_module, None)

    def test_xlsx_sans_openpyxl_message_dependance(self, monkeypatch):
        self._sans_module(monkeypatch, 'openpyxl')
        with pytest.raises(file_parser.DependanceManquante) as excinfo:
            file_parser.parse_xlsx(io.BytesIO(b'x'))
        assert 'openpyxl' in str(excinfo.value)
        assert 'pip install' in str(excinfo.value)

    def test_xls_sans_xlrd_message_dependance(self, monkeypatch):
        self._sans_module(monkeypatch, 'xlrd')
        with pytest.raises(file_parser.DependanceManquante) as excinfo:
            file_parser.parse_xls(io.BytesIO(b'x'))
        assert 'xlrd' in str(excinfo.value)

    def test_corrompu_reste_une_valueerror_lisible(self):
        with pytest.raises(ValueError, match='illisible ou corrompu'):
            file_parser.parse_xlsx(io.BytesIO(b'Ceci nest pas un excel'))

    def test_verifier_dependances_ok(self, monkeypatch):
        # Tous les modules présents -> aucune exception
        file_parser.verifier_dependances()

    def test_verifier_dependances_manquant_liste_le_nom(self, monkeypatch):
        self._sans_module(monkeypatch, 'xlrd')
        with pytest.raises(file_parser.DependanceManquante) as excinfo:
            file_parser.verifier_dependances()
        assert 'xlrd' in str(excinfo.value)


class TestRouteDependanceManquante:
    def test_analyze_renvoie_guidage_installation(self, client, app, monkeypatch):
        up = client.post(
            '/upload',
            data={'file': (io.BytesIO(b'fake'), 'f.xlsx')},
            content_type='multipart/form-data',
        )
        fid = up.get_json()['id']

        original = file_parser.parse_file
        monkeypatch.setattr(
            'routes.parse_file',
            lambda *a, **k: (_ for _ in ()).throw(
                file_parser.DependanceManquante('openpyxl')
            ),
        )
        an = client.post(f'/analyze/{fid}')
        body = an.get_json()
        assert an.status_code == 503
        assert 'openpyxl' in body['error']
        assert 'pip install' in body['error']
