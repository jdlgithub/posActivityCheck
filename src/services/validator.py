import os
from typing import Set

from models.fichier_analyse import SUPPORTED_FORMATS


def get_file_extension(filename: str) -> str:
    """Extrait l'extension en minuscules d'un nom de fichier."""
    return os.path.splitext(filename)[1].lstrip('.').lower()


def validate_file(extension: str, allowed_extensions: Set[str]) -> bool:
    """Vérifie qu'une extension fait partie des extensions autorisées."""
    return extension.lower() in allowed_extensions


def is_allowed_extension(extension: str) -> bool:
    """Vérifie l'extension contre les formats supportés par l'application."""
    return validate_file(extension, SUPPORTED_FORMATS)


def validate_file_size(file, max_size: int) -> bool:
    """Vérifie que la taille du fichier ouvert ne dépasse pas max_size."""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= max_size


def exceeds_max_size(size_bytes: int, max_size: int) -> bool:
    """Détermine si une taille donnée dépasse la limite autorisée."""
    return size_bytes > max_size
