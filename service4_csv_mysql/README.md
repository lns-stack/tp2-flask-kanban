# Service 4 — Chargement CSV → MySQL

API REST Flask pour importer des fichiers CSV dans la base MySQL. Port : **5004**

## Installation

```bash
cd service4_csv_mysql
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # éditez avec vos credentials MySQL
python app.py
```

## Format CSV attendu

| Colonne | Type | Obligatoire |
|---------|------|-------------|
| nom_serie | Texte | ✅ |
| valeur | Nombre | ✅ |
| categorie | Texte | Non |
| date_mesure | Date (YYYY-MM-DD) | Non |

## Routes disponibles

### POST /upload/csv
Upload d'un fichier CSV pour insertion en base MySQL.

**Requête :** `multipart/form-data` avec le champ `file`  
**Réponse 201 :** `{"statut": "success", "lignes_inserees": 30, "lignes_invalides_ignorees": 0, ...}`  
**Erreur 400 :** fichier manquant, extension invalide, colonnes manquantes  
**Erreur 413 :** fichier > 5 Mo

---

### GET /upload/series
Liste les séries chargées en base avec leur nombre de points.

**Réponse 200 :** `{"series": [{"serie": "serie_A", "n_points": 10, ...}], "total": 3}`

## Tests

```bash
# Charger le fichier de démo
curl -X POST http://localhost:5004/upload/csv \
     -F 'file=@../data/donnees_exemple.csv'

# Lister les séries
curl http://localhost:5004/upload/series

# Tests Python
python test_service4.py
```

Ouvrir `test_service4.html` pour tester manuellement avec un vrai fichier.
