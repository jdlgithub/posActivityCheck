import os

import pandas as pd

from services.statistics import _normaliser


def parse_file(file, filename: str) -> pd.DataFrame:
    """Dispatche vers le bon parser selon l'extension du fichier."""
    extension = get_file_extension(filename)

    parsers = {
        'xlsx': parse_xlsx,
        'xls': parse_xls,
        'csv': parse_csv,
        'pdf': parse_pdf,
    }
    parser = parsers.get(extension)
    if parser is None:
        raise ValueError(f"Format non supporté: '{extension}'")
    return parser(file)


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lstrip('.').lower()


def _normaliser_entetes(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise les en-têtes de colonnes (accents/casse) pour le calcul des taux."""
    df = df.copy()
    df.columns = [_normaliser(c) for c in df.columns]
    return df


def parse_xlsx(file) -> pd.DataFrame:
    try:
        df = pd.read_excel(file, engine='openpyxl')
    except ValueError:
        raise
    except Exception as exc:  # noqa: BLE001 — fichier illisible/corrompu
        raise ValueError(f"Fichier .xlsx illisible ou corrompu: {exc}") from exc
    return _normaliser_entetes(df)


def parse_xls(file) -> pd.DataFrame:
    try:
        df = pd.read_excel(file, engine='xlrd')
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"Fichier .xls illisible ou corrompu: {exc}") from exc
    return _normaliser_entetes(df)


def parse_csv(file, encoding_candidates=('utf-8', 'utf-8-sig', 'latin-1')) -> pd.DataFrame:
    """Parse un CSV avec repli d'encodage automatique."""
    raw = file.read()
    derniere_erreur = None
    for encodage in encoding_candidates:
        try:
            df = pd.read_csv(io_bytes(raw), encoding=encodage)
            return _normaliser_entetes(df)
        except UnicodeDecodeError as exc:
            derniere_erreur = exc
    raise ValueError(f"Encodage du fichier CSV non reconnu: {derniere_erreur}")


def io_bytes(data: bytes):
    from io import BytesIO
    return BytesIO(data)


def parse_pdf(file):
    """Extraction tabulaire d'un PDF via tabula-py (requiert Java)."""
    try:
        import tabula
    except ImportError as exc:
        raise ValueError("L'extraction PDF nécessite tabula-py (et Java)") from exc
    tables = tabula.read_pdf(file, pages='all', multiple_tables=True, silent=True)
    if not tables:
        raise ValueError("Aucun tableau détecté dans le fichier PDF")
    df = pd.concat(tables, ignore_index=True)
    return _normaliser_entetes(df)
