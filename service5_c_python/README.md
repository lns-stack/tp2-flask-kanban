# Service 5 — Fonctions C appelées depuis Python (ctypes)

API REST Flask exposant des calculs statistiques implémentés en C. Port : **5005**

## Pré-requis

- `gcc` installé (Linux/Mac) ou MinGW-w64 (Windows)
- Python 3.10+

## Installation

```bash
cd service5_c_python

# 1. Compiler la bibliothèque C
chmod +x compile.sh
./compile.sh
# → Crée lib/stats.so (Linux) ou lib/stats.dylib (macOS)

# 2. Installer Flask et lancer
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Routes disponibles

### POST /c/stats/describe
Statistiques complètes (moteur C).

**Corps JSON :** `{"data": [12.5, 15.3, 8.7, 21.0]}`  
**Réponse 200 :** `{"moteur": "C/ctypes", "operation": "description", "resultat": {...}}`

---

### POST /c/stats/mean — Moyenne  
### POST /c/stats/stddev — Écart-type  
### POST /c/stats/median — Médiane  
**Corps JSON :** `{"data": [...]}`

---

### POST /c/stats/dot
Produit scalaire de deux vecteurs.

**Corps JSON :** `{"v1": [1,2,3], "v2": [4,5,6]}`  
**Réponse 200 :** `{"resultat": 32.0}`

---

### GET /c/health
Vérification que le service est opérationnel.

## Benchmark Python vs C

```bash
python benchmark.py
```

## Tests

```bash
python test_service5.py

curl -X POST http://localhost:5005/c/stats/describe \
     -H 'Content-Type: application/json' \
     -d '{"data": [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]}'
```

## Note Git

`lib/stats.so` est dans `.gitignore` — chaque développeur doit compiler localement.
