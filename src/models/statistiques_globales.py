from dataclasses import dataclass


@dataclass(frozen=True)
class StatistiquesGlobales:
    """Résultat agrégé d'une analyse : 4 taux en pourcentage [0, 100].

    Immuable par conception ; les valeurs sont arrondies à une décimale
    au moment du calcul pour garantir un affichage homogène.
    """
    taux_pos_attente: float = 0.0
    taux_pos_valides: float = 0.0
    taux_pos_conformes: float = 0.0
    taux_agents_performants: float = 0.0

    CHAMPS = (
        'taux_pos_attente',
        'taux_pos_valides',
        'taux_pos_conformes',
        'taux_agents_performants',
    )

    def __post_init__(self):
        for champ in self.CHAMPS:
            valeur = getattr(self, champ)
            if not 0.0 <= valeur <= 100.0:
                raise ValueError(f"{champ} hors plage [0, 100]: {valeur}")

    @classmethod
    def from_dict(cls, data: dict) -> 'StatistiquesGlobales':
        return cls(**{champ: float(data[champ]) for champ in cls.CHAMPS})

    def to_dict(self) -> dict:
        return {champ: getattr(self, champ) for champ in self.CHAMPS}

    def est_valide(self) -> bool:
        """Cohérence : les taux doivent être calculables et bornés."""
        return all(0.0 <= getattr(self, c) <= 100.0 for c in self.CHAMPS)
