# Service 2 — Statistiques JSON

API REST Flask pour des calculs statistiques sur données JSON. Port : **5002**

## Installation

```bash
cd service2_statistiques
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Routes disponibles

### POST /stats/describe
Statistiques descriptives d'une série de valeurs.

**Corps JSON :** `{"data": [12.5, 15.3, 8.7, 21.0, 13.2]}`  
**Réponse 200 :** `{"operation": "description", "resultat": {"n": 5, "moyenne": ..., "mediane": ..., ...}}`

---

### POST /stats/correlation
Coefficient de corrélation de Pearson entre deux séries.

**Corps JSON :** `{"x": [1,2,3,4,5], "y": [2,4,5,4,5]}`  
**Réponse 200 :** `{"operation": "correlation_pearson", "resultat": {"r": 0.87, "p_value": ..., "significatif": true}}`

---

### POST /stats/test_normalite
Test de Shapiro-Wilk (normalité d'une distribution).

**Corps JSON :** `{"data": [12.5, 15.3, 8.7, 21.0, 13.2, 9.8]}`  
**Réponse 200 :** `{"operation": "test_normalite_shapiro_wilk", "resultat": {"est_normale": true, ...}}`

---

### POST /stats/test_student *(bonus)*
Test t de Student entre deux groupes indépendants.

**Corps JSON :** `{"groupe1": [10,11,12], "groupe2": [20,21,22]}`

## Tests

```bash
python test_service2.py

curl -X POST http://localhost:5002/stats/describe \
     -H 'Content-Type: application/json' \
     -d '{"data": [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]}'
```

Ouvrir `test_service2.html` dans un navigateur pour les tests visuels.
