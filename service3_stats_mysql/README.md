# Service 3 — Statistiques depuis MySQL

API REST Flask qui lit les données depuis MySQL pour les calculs statistiques. Port : **5003**

## Pré-requis

- MySQL opérationnel avec la base `flask_stats` (voir `sql/init_db.sql`)
- Service 4 utilisé pour charger les données via CSV

## Installation

```bash
cd service3_stats_mysql
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # puis éditez .env avec vos credentials
python app.py
```

## Configuration .env

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=flask_user
DB_PASSWORD=votre_mot_de_passe
DB_NAME=flask_stats
```

## Routes disponibles

### GET /db/stats/describe?serie=serie_A
Statistiques descriptives d'une série depuis MySQL.

**Réponse 200 :** `{"source": "mysql", "resultat": {"serie": "serie_A", "n": 10, "moyenne": 14.32, ...}}`  
**Erreur 400 :** paramètre `serie` manquant  
**Erreur 404 :** série inexistante en base

---

### GET /db/stats/correlation?serie_x=serie_A&serie_y=serie_B
Corrélation de Pearson entre deux séries depuis MySQL.

**Réponse 200 :** `{"source": "mysql", "series": {...}, "resultat": {"r": ..., "p_value": ..., "significatif": ...}}`

## Tests

```bash
python test_service3.py

curl "http://localhost:5003/db/stats/describe?serie=serie_A"
curl "http://localhost:5003/db/stats/correlation?serie_x=serie_A&serie_y=serie_B"
```

Ouvrir `test_service3.html` dans un navigateur pour les tests visuels.
