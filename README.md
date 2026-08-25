# POS Activity Check

Utilitaire d'analyse de fichiers de suivi d'activité POS : déposez un fichier,
lancez l'analyse et consultez les statistiques globales avec un rendu statique
professionnel (couleurs selon les niveaux).

## Stack

- **Backend** : Python 3.11+ / Flask
- **Parsing** : openpyxl (.xlsx), xlrd (.xls), pandas (.csv), tabula-py (.pdf)
- **Frontend** : Jinja2 + Bootstrap 5 + JavaScript vanilla (rendu serveur)
- **Tests** : pytest

## Formats supportés

`.xlsx` `.xls` `.pdf` `.csv` — taille max **50 Mo**.

## Démarrage

```bash
# 1. Environnement virtuel
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Windows
source .venv/bin/activate           # Linux/Mac

# 2. Dépendances
pip install -r requirements.txt

# 3. Lancement
cd src
flask --app app run --debug
```

Application disponible sur <http://localhost:5000>.

> Le support PDF nécessite Java sur la machine (requis par tabula-py).

## Utilisation

1. Glissez-déposez un fichier de suivi d'activité sur la zone centrale
   (ou cliquez pour parcourir).
2. Cliquez sur **« Démarrer l'analyse »**.
3. Une notification « Analyse terminée » s'affiche puis les statistiques :
   - Taux de POS en attente de complétion
   - Taux de POS valides
   - Taux de POS conformes
   - Taux d'agents faisant le bon travail

Chaque taux est coloré selon son niveau : vert (≥ 80 %), jaune (≥ 50 %),
rouge (< 50 %).

## Colonnes attendues

Le fichier doit contenir des colonnes de type :

| Colonne | Alias reconnus | Exemples de valeurs |
|---------|----------------|---------------------|
| Statut | `status`, `statut`, `etat` | `valide`, `en attente`, `inconforme` |
| Conformité | `conformite`, `conforme` | `oui`, `non`, `true`, `1` |

La détection est tolérante à la casse et aux accents.

## Tests

```bash
python -m pytest tests/ -v
```

Couverture : validateur, parsers multi-formats, calcul des statistiques,
routes HTTP, cas limites, scénarios d'intégration.

## Architecture

```text
src/
├── app.py                  # Factory Flask + logging JSON (stdout)
├── config.py               # Configuration par environnement
├── routes.py               # Routes / , /upload , /analyze/<id> , /health
├── models/
│   ├── fichier_analyse.py  # Entité immuable + états ZoneDepot
│   └── statistiques_globales.py
├── services/
│   ├── validator.py        # Extension + taille
│   ├── file_parser.py      # Dispatch multi-formats
│   └── statistics.py       # Calcul des taux
├── templates/              # base, index, results (Jinja2)
└── static/                 # CSS professionnel + JS drag-and-drop

tests/
├── conftest.py             # Fixtures partagées
├── unit/                   # Validator, parser, statistics, edge cases
└── integration/            # Upload, formats, erreurs
```

Principes appliqués : KISS, YAGNI, entités immuables, logs JSON structurés,
aucun stockage disque des fichiers déposés.
