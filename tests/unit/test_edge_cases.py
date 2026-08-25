import io
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest
import pandas as pd

from services.statistics import calculate_statistics
from services.file_parser import parse_csv, parse_file
from models.fichier_analyse import FichierAnalyse, STATE_EMPTY, STATE_FORMAT_ERROR
from models.statistiques_globales import StatistiquesGlobales


class TestCasLimitesStatistiques:
    def test_csv_en_tetes_seulement(self):
        df = parse_csv(io.BytesIO(b'status,conformite\n'))
        assert df.empty
        assert calculate_statistics(df) == {
            'taux_pos_attente': 0.0,
            'taux_pos_valides': 0.0,
            'taux_pos_conformes': 0.0,
            'taux_agents_performants': 0.0,
        }

    def test_colonnes_non_reconnues_tous_les_taux_zero(self):
        df = pd.DataFrame({'nom': ['A'], 'ville': ['Dakar']})
        stats = calculate_statistics(df)
        assert all(v == 0.0 for v in stats.values())

    def test_valeurs_status_inconnues_ne_comptent_pas(self):
        df = pd.DataFrame({'status': ['bizarre', 'inconnu', 'xyz']})
        stats = calculate_statistics(df)
        assert stats['taux_pos_valides'] == 0.0
        assert stats['taux_pos_attente'] == 0.0

    def test_dataframe_none_renvoie_zeros(self):
        assert calculate_statistics(None)['taux_pos_valides'] == 0.0

    def test_statut_majuscule_accents_detecte(self):
        df = pd.DataFrame({'statut': ['VALIDÉ', 'En Attente']})
        stats = calculate_statistics(df)
        assert stats['taux_pos_valides'] == 50.0
        assert stats['taux_pos_attente'] == 50.0


class TestCasLimitesEntites:
    def test_fichier_analyse_format_interdit_leve_valueerror(self):
        with pytest.raises(ValueError, match='Format non supporté'):
            FichierAnalyse(nom_fichier='doc.docx', format='docx', taille_bytes=10)

    def test_fichier_analyse_nom_vide_leve_valueerror(self):
        with pytest.raises(ValueError, match='nom du fichier'):
            FichierAnalyse(nom_fichier='', format='csv', taille_bytes=10)

    def test_en_erreur_est_immuable_nouvelle_instance(self):
        f = FichierAnalyse.from_upload('a.csv', 100)
        f2 = f.en_erreur('test')
        assert f.erreur is None
        assert f2.est_en_erreur is True
        assert f2.id == f.id

    def test_statistiques_hors_plage_leve_valueerror(self):
        with pytest.raises(ValueError, match='hors plage'):
            StatistiquesGlobales(taux_pos_valides=150.0)


class TestCasLimitesParsing:
    def test_csv_vide_leve_erreur_pandassexperty(self):
        with pytest.raises(Exception):
            parse_csv(io.BytesIO(b''))

    def test_dispatch_sensible_a_la_casse_extension(self):
        content = b'status\nvalide\n'
        df = parse_file(io.BytesIO(content), 'FICHIER.CSV')
        assert len(df) == 1

    def test_etats_zone_depot_exposes(self):
        assert STATE_EMPTY == 'vide'
        assert STATE_FORMAT_ERROR == 'erreur_format'
