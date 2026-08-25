# Implementation Plan: Static File Analyzer

**Branch**: `[001-static-file-analyzer]` | **Date**: 2025-08-25 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/static-file-analyzer/spec.md`

## Summary

L'application **Static File Analyzer** est un utilitaire d'analyse de fichiers Excel/PDF/CSV pour visualiser les statistiques d'activité POS avec un rendu statique professionnel. L'utilisateur dépose un fichier, lance l'analyse et consulte les statistiques globales colorées selon les critères.

**Approche technique**: Application web Flask avec templates Jinja2 côté serveur, support multi-formats (.xlsx, .xls, .pdf, .csv), rendu HTML/CSS professionnel.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Flask, openpyxl (xlsx), xlrd (xls), tabula-py (pdf), pandas (csv), Jinja2 (templates), Bootstrap 5 (CSS)

**Storage**: Fichiers temporaires en mémoire (pas de persistance), session Flask pour l'état

**Testing**: pytest (unit tests), pytest-flask (integration tests)

**Target Platform**: Linux/Windows server, navigateur web moderne

**Project Type**: Application web avec rendu serveur (Flask + templates statiques)

**Performance Goals**: Analyse de fichiers jusqu'à 10 000 lignes en moins de 10 secondes

**Constraints**: 
- Interface responsive et accessible
- Couleurs professionnelles selon les critères
- Message popup après analyse
- Support des formats: .xlsx, .xls, .pdf, .csv uniquement

**Scale/Scope**: 
- Mono-utilisateur (pas d'authentification)
- Fichiers jusqu'à 10 000 lignes
- Pas de stockage persistant

## Constitution Check

| Principe Constitution | Applicable | Vérification |
|----------------------|------------|-------------|
| KISS | Oui | Architecture simple Flask monocouche avec templates |
| YAGNI | Oui | Fonctionnalités limitées au scope (analyse, stats, affichage) |
| SOLID/DRY | Oui | Services séparés pour analyse, conversion, statistiques |
| Tests Edge Cases | Oui | Tests pour fichiers invalides, formats non supportés |
| Logs JSON stdout | Oui | Configuration Flask logging en JSON |

**GATE**: ✅ Toutes les vérifications passent

## Project Structure

### Documentation (this feature)

```text
.specify/specs/static-file-analyzer/
├── spec.md              # Feature specification
├── plan.md              # This implementation plan
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output (HTML contract)
    └── ui-contract.md
```

### Source Code (repository root)

```text
src/
├── app.py                    # Application Flask principale
├── config.py                 # Configuration Flask
├── services/
│   ├── __init__.py
│   ├── file_parser.py        # Parser multi-format (xlsx, xls, pdf, csv)
│   ├── statistics.py         # Calcul des statistiques POS
│   └── validator.py          # Validation des formats
├── templates/
│   ├── base.html             # Template de base
│   ├── index.html            # Page principale avec zone drag-drop
│   └── results.html          # Page de résultats statistiques
├── static/
│   ├── css/
│   │   └── styles.css        # Styles professionnels
│   └── js/
│       └── app.js            # JavaScript pour drag-drop et UI
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_file_parser.py
│   │   ├── test_statistics.py
│   │   └── test_validator.py
│   └── integration/
│       └── test_app.py       # Tests d'intégration Flask
├── templates/
│   └── ControlDoc.xlsx       # Template de référence (copie)
└── requirements.txt          # Dépendances Python
```

**Structure Decision**: Structure Flask classique avec services, templates Jinja2, et tests unitaires/integration séparés. Le frontend utilise des templates serveur (rendu statique) avec Bootstrap 5 pour un look professionnel.

## Complexity Tracking

> Aucune violation de constitution détectée. Complexité minimale adaptée au scope.

## Phase 0: Research

### Décisions Techniques Identifiées

| Décision | Choix | Rationale |
|----------|-------|-----------|
| Format PDF parsing | tabula-py + pandas | Extraction fiable de tableaux depuis PDF |
| Format Excel parsing | openpyxl + xlrd | Support .xlsx et .xls legacy |
| Format CSV parsing | pandas | Parsing robuste avec détection d'encodage |
| UI Framework | Bootstrap 5 + Custom CSS | Rendu professionnel et responsive |
| Rendu statistiques | Template Jinja2 + CSS | Rendu serveur (static rendering) |

### Research.md Consolidé

Les technologies sélectionnées sont standard et bien documentées:
- **Flask**: Framework Python léger pour applications web
- **openpyxl/xlrd**: Parsing Excel natif sans dépendances externes lourdes
- **pandas**: Analyse de données CSV robuste
- **tabula-py**: Extraction de tableaux depuis PDF
- **Bootstrap 5**: CSS professionnel et responsive

**Risques identifiés**:
- Extraction PDF peut varier selon la structure du document
- Fichiers Excel avec format non standard peuvent échouer

**Mitigations**:
- Messages d'erreur clairs pour l'utilisateur
- Validation du format avant analyse
- Tests avec différents types de fichiers

## Phase 1: Design & Contracts

### Data Model (data-model.md)

```markdown
## Entities

### FichierAnalyse
| Champ | Type | Validation |
|-------|------|------------|
| nom_fichier | string | Non vide, extension valide |
| format | enum | xlsx, xls, pdf, csv |
| date_chargement | datetime | Auto-généré |
| contenu | bytes | Non vide, taille max 50MB |
| donnees | DataFrame | Colonnes attendues du template |

### StatistiquesGlobales
| Champ | Type | Description |
|-------|------|-------------|
| taux_pos_attente | float | Pourcentage 0-100 |
| taux_pos_valides | float | Pourcentage 0-100 |
| taux_pos_conformes | float | Pourcentage 0-100 |
| taux_agents_performants | float | Pourcentage 0-100 |

### ZoneDepot (état UI)
| État | Description |
|------|-------------|
| vide | Zone de dépôt prête |
| fichier_charge | Fichier déposé, nom affiché |
| analyse_en_cours | Analyse en traitement |
| resultats | Statistiques affichées |
| erreur_format | Format non supporté |
```

### UI Contract (contracts/ui-contract.md)

```markdown
## Page Principale (index.html)

### Zone de Dépôt
- Surface drag-drop visible au centre de la page
- Icône et texte d'instruction
- Indicateur visuel au survol (border highlight)
- Affichage du nom du fichier après dépôt

### Bouton Démarrer
- État initial: caché
- Après dépôt: visible avec texte "Démarrer l'analyse"
- État actif: "Analyse en cours..." pendant le traitement

### Message Popup
- Apparaît après analyse avec texte "Analyse terminée ✓"
- Auto-dismiss après 3 secondes
- Style: toast notification Bootstrap

### Zone Statistiques
- 4 cards Bootstrap avec icônes
- Couleurs conditionnelles selon seuils:
  - Vert (≥80%): très bon
  - Jaune (50-79%): acceptable
  - Rouge (<50%): à améliorer
- Labels clairs et pourcentage mis en évidence
```

### Quickstart Guide (quickstart.md)

```markdown
# Static File Analyzer - Guide de Validation

## Prérequis
- Python 3.11+
- pip install -r requirements.txt

## Lancement
```bash
cd src
flask run --debug
```

## Scénarios de Validation

### SV-001: Chargement fichier valide
1. Ouvrir http://localhost:5000
2. Déposer un fichier .xlsx sur la zone
3. Vérifier: nom du fichier affiché, bouton "Démarrer l'analyse" visible

### SV-002: Analyse et affichage
1. Cliquer sur "Démarrer l'analyse"
2. Attendre le popup "Analyse terminée"
3. Vérifier: 4 statistiques affichées avec couleurs

### SV-003: Format non supporté
1. Déposer un fichier .docx
2. Vérifier: message d'erreur "Format non supporté"

### SV-004: Fichier CSV
1. Déposer un fichier .csv
2. Lancer l'analyse
3. Vérifier: statistiques extraites correctement
```

## Complexity Tracking

> Ce projet est de complexité faible. Structure simple, pas d'authentification, pas de base de données.

| Aspect | Valeur | Justification |
|--------|--------|---------------|
| Services | 3 | file_parser, statistics, validator |
| Routes | 2 | GET /, POST /analyze |
| Tests | 6+ | Unitaires par service + integration |
