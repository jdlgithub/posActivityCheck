# Data Model - Static File Analyzer

## Entity: FichierAnalyse

| Champ | Type | Validation | Description |
|-------|------|------------|-------------|
| `id` | string | Auto-généré UUID | Identifiant unique |
| `nom_fichier` | string | Non vide, extension autorisée (.xlsx, .xls, .pdf, .csv) | Nom original du fichier |
| `format` | enum | Valeur stricte | Format détecté (.xlsx, .xls, .pdf, .csv) |
| `date_chargement` | datetime | Auto-généré (UTC) | Date/heure du chargement |
| `taille_bytes` | int | >= 1, <= 52428800 (50MB) | Taille du fichier |
| `contenu` | bytes | Non vide | Contenu binaire du fichier |
| `colonnes_detectees` | array[string] | Non vide | Noms des colonnes détectées |
| `donnees` | DataFrame | Structure dépend du format | Tableau de données |

**Contraintes**:
- `id`: UUID v4 obligatoire
- `format`: Valide seulement `.xlsx`, `.xls`, `.pdf`, `.csv`
- `taille_bytes`: <= 50MB, rejet supérieur
- `date_chargement`: Format ISO 8601 UTC

---

## Entity: StatistiquesGlobales

| Champ | Type | Unité | Plage | Description |
|-------|------|-------|-------|-------------|
| `taux_pos_attente` | float | Pourcentage | 0-100 | Taux POS en attente de complétion |
| `taux_pos_valides` | float | Pourcentage | 0-100 | Taux POS valides |
| `taux_pos_conformes` | float | Pourcentage | 0-100 | Taux POS conformes |
| `taux_agents_performants` | float | Pourcentage | 0-100 | Taux agents faisant le bon taf |

**Contraintes**:
- Toutes valeurs dans [0, 100]
- Somme possible > 100 selon données
- Préformaté avec 1 décimale (ex: 85.3)

---

## Entity: ZoneDepot (État UI)

| État | Transition trigger | État suivant |
|------|-------------------|--------------|
| `vide` | Déposer fichier | `fichier_charge` |
| `fichier_charge` | Cliquer "Démarrer analyse" | `analyse_en_cours` |
| `analyse_en_cours` | Finir calcul | `resultats` |
| `resultats` | Nouveau fichier ou quitter | `vide` |
| `erreur_format` | Répéter | `fichier_charge` |

**Note**: État `erreur_format` gère le cas format non supporté.