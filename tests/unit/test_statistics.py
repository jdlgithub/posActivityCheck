import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from services.statistics import calculate_statistics
from models.statistiques_globales import StatistiquesGlobales


def make_df(rows, columns):
    import pandas as pd
    return pd.DataFrame(rows, columns=columns)


class TestCalculateStatistics:
    def test_empty_dataframe_returns_zeros(self):
        stats = calculate_statistics(make_df([], ['status']))
        assert stats == {
            'taux_pos_attente': 0.0,
            'taux_pos_valides': 0.0,
            'taux_pos_conformes': 0.0,
            'taux_agents_performants': 0.0,
        }

    def test_taux_pos_valides(self):
        df = make_df(
            [['valide'], ['valide'], ['en attente'], ['inconforme'], ['valide']],
            ['status'],
        )
        assert calculate_statistics(df)['taux_pos_valides'] == 60.0

    def test_taux_pos_attente(self):
        df = make_df(
            [['en attente'], ['En Attente'], ['valide'], ['valide']],
            ['status'],
        )
        assert calculate_statistics(df)['taux_pos_attente'] == 50.0

    def test_colonne_statut_francais_detectee(self):
        df = make_df([['valide'], ['valide']], ['statut'])
        assert calculate_statistics(df)['taux_pos_valides'] == 100.0

    def test_taux_pos_conformes_colonne_conformite(self):
        df = make_df(
            [['oui'], ['non'], ['oui'], ['oui']],
            ['conformite'],
        )
        assert calculate_statistics(df)['taux_pos_conformes'] == 75.0

    def test_taux_arrondi_une_decimale(self):
        df = make_df([['valide']] * 3, ['status'])
        assert calculate_statistics(df)['taux_pos_valides'] == round(3 / 3 * 100, 1)

    def test_valeurs_manquantes_ignorees(self):
        df = make_df([['valide'], [None]], ['status'])
        # None ne compte ni comme valide ni comme attente
        stats = calculate_statistics(df)
        assert stats['taux_pos_valides'] == 50.0
        assert stats['taux_pos_attente'] == 0.0

    def test_resultat_instanciable_en_entite(self):
        df = make_df([['valide'], ['en attente']], ['status'])
        entite = StatistiquesGlobales.from_dict(calculate_statistics(df))
        assert entite.taux_pos_valides == 50.0
        assert entite.est_valide()
