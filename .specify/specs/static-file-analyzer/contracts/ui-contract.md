# UI Contract - Static File Analyzer

## Page Principale (index.html)

### 1. Zone de Dépôt
```
Position: Center, top 1/3 of page
Size: 600px width, 300px height
Border: 2px dashed #4A90E2
Background: #F5F7FA
Icon: Upload icon, 64px
Text: "Glissez votre fichier ici"
Subtext: ".xlsx, .xls, .pdf, .csv"
Hover state: border-color #2C5C8A
```

### 2. Bouton Démarrer
```
Hidden by default
After file drop: visible, large button, primary color
Text: "Démarrer l'analyse"
Position: Below dropzone
```

### 3. Popup "Analyse terminée"
```
Toast notification, top-right
Duration: 3 seconds, auto-dismiss
Background: #28A745 (green)
Icon: ✓ check
Animation: slide-in from right
```

### 4. Zone Statistiques (cards)
```
Layout: 4 columns, responsive grid
Card size: min 200px width

Each card:
- Icon: bar chart icon
- Title: Nom du taux
- Value: pourcentage avec couleur conditionnelle
- Color rules:
  * Vert (#28A745) si >= 80%
  * Jaune (#FFC107) si 50-79%
  * Rouge (#DC3545) si < 50%
```

## Données Attendues (POST /analyze)
```
Content-Type: multipart/form-data
Field: file (binary)
```

## Réponse (HTML rendering)
```
200 OK: rendered HTML with statistics
400 Bad Request: invalid format
413 Payload Too Large: file > 50MB
500 Internal Server Error: parsing error
```

## JavaScript Events
```
- dragenter, dragover: prevent default, show hover
- drop: send POST to /analyze
- success: render results
- error: show error message
```