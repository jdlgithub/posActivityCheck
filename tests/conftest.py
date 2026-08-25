import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import create_app


@pytest.fixture
def app():
    app = create_app('testing')
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_csv_content():
    """Contenu CSV d'exemple avec colonnes standard POS."""
    return (
        "id_pos,nom_pos,status,conformite,agent,agent_performance\n"
        "1,POS-001,valide,oui,Diallo,bon\n"
        "2,POS-002,en attente,non,Ba,mauvais\n"
        "3,POS-003,validé,oui,Sow,bon\n"
        "4,POS-004,inconforme,non,Ndiaye,mauvais\n"
        "5,POS-005,valide,oui,Fall,bon\n"
    )


@pytest.fixture
def csv_file(tmp_path, sample_csv_content):
    """Fichier CSV temporaire pour les tests."""
    file_path = tmp_path / "test_activity.csv"
    file_path.write_text(sample_csv_content, encoding="utf-8")
    return str(file_path)
