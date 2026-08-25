from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


SUPPORTED_FORMATS = {'xlsx', 'xls', 'pdf', 'csv'}

# ZoneDepot states
STATE_EMPTY = 'vide'
STATE_FILE_LOADED = 'fichier_charge'
STATE_ANALYZING = 'analyse_en_cours'
STATE_RESULTS = 'resultats'
STATE_FORMAT_ERROR = 'erreur_format'


@dataclass(frozen=True)
class FichierAnalyse:
    """Représente un fichier déposé pour analyse (immuable par conception).

    La validation du format est effectuée à la création pour garantir
    qu'aucune instance invalide ne circule dans le reste de l'application.
    """
    nom_fichier: str
    format: str
    taille_bytes: int
    id: str = field(default_factory=lambda: __import__('uuid').uuid4().hex)
    date_chargement: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    erreur: Optional[str] = None

    def __post_init__(self):
        if not self.nom_fichier:
            raise ValueError('Le nom du fichier ne peut pas être vide')
        if self.format.lower() not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Format non supporté: '{self.format}'. "
                f"Formats acceptés: {', '.join(sorted(SUPPORTED_FORMATS))}"
            )

    @classmethod
    def from_upload(cls, filename: str, size_bytes: int) -> 'FichierAnalyse':
        """Construit une instance depuis un upload, extension déduite du nom."""
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        return cls(nom_fichier=filename, format=ext, taille_bytes=size_bytes)

    def en_erreur(self, message: str) -> 'FichierAnalyse':
        """Retourne une copie marquée en erreur (transition vers `erreur_format`)."""
        return FichierAnalyse(
            nom_fichier=self.nom_fichier,
            format=self.format,
            taille_bytes=self.taille_bytes,
            id=self.id,
            date_chargement=self.date_chargement,
            erreur=message,
        )

    @property
    def est_en_erreur(self) -> bool:
        return self.erreur is not None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nom_fichier': self.nom_fichier,
            'format': self.format,
            'taille_bytes': self.taille_bytes,
            'date_chargement': self.date_chargement,
            'erreur': self.erreur,
        }
