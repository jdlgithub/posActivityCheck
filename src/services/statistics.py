import unicodedata

import pandas as pd

from models.statistiques_globales import StatistiquesGlobales


def _normaliser(texte: str) -> str:
    """Minuscules sans accents pour une détection de colonnes tolérante."""
    texte = str(texte).strip().lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texte)
        if unicodedata.category(c) != 'Mn'
    )


# Noms de colonnes candidats (normalisés) pour chaque indicateur
COLONNES_STATUT = ('status', 'statut', 'etat')
COLONNES_CONFORMITE = ('conformite', 'conforme', 'conformity')

MOTS_ATTENTE = ('attente', 'pending', 'en cours')
MOTS_VALIDE = ('valide', 'valid')


def _trouver_colonne(df: pd.DataFrame, candidats) -> str | None:
    for colonne in df.columns:
        if _normaliser(colonne) in candidats:
            return colonne
    return None


def _taux_contenant(df: pd.DataFrame, colonne: str, mots_cles) -> float:
    serie = df[colonne].dropna().astype(str).map(_normaliser)
    if serie.empty:
        return 0.0
    total = len(df)
    correspondances = serie.str.contains('|'.join(mots_cles), regex=True).sum()
    return round((correspondances / total) * 100, 1)


def _taux_conformite(df: pd.DataFrame) -> float:
    colonne = _trouver_colonne(df, COLONNES_CONFORMITE)
    if colonne is None:
        return 0.0
    serie = df[colonne].dropna().astype(str).map(_normaliser)
    if serie.empty:
        return 0.0
    positifs = serie.isin(('oui', 'oui ', 'true', '1', 'yes', 'conforme')).sum()
    return round((positifs / len(df)) * 100, 1)


def calculate_statistics(data: pd.DataFrame) -> dict:
    """Calcule les 4 taux globaux à partir des données extraites du fichier.

    Retourne un dict compatible avec StatistiquesGlobales.from_dict().
    """
    if data is None or data.empty:
        return StatistiquesGlobales().to_dict()

    colonne_statut = _trouver_colonne(data, COLONNES_STATUT)

    stats = StatistiquesGlobales(
        taux_pos_attente=(
            _taux_contenant(data, colonne_statut, MOTS_ATTENTE)
            if colonne_statut else 0.0
        ),
        taux_pos_valides=(
            _taux_contenant(data, colonne_statut, MOTS_VALIDE)
            if colonne_statut else 0.0
        ),
        taux_pos_conformes=_taux_conformite(data),
    )
    return stats.to_dict()
