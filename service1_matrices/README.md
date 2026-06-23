# Service 1 — Calculs Matriciels

API REST Flask pour effectuer des calculs sur des matrices. Port : **5001**

## Installation

```bash
cd service1_matrices
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Routes disponibles

### POST /matrices/add
Additionne deux matrices de mêmes dimensions.

**Corps JSON :** `{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]}`  
**Réponse 200 :** `{"operation": "addition", "resultat": [[6.0,8.0],[10.0,12.0]]}`  
**Erreur 400 :** dimensions incompatibles

---

### POST /matrices/multiply
Multiplie deux matrices (colonnes A = lignes B).

**Corps JSON :** `{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]}`  
**Réponse 200 :** `{"operation": "multiplication", "resultat": [[19.0,22.0],[43.0,50.0]]}`

---

### POST /matrices/transpose
Retourne la transposée d'une matrice.

**Corps JSON :** `{"A": [[1,2,3],[4,5,6]]}`  
**Réponse 200 :** `{"operation": "transposee", "resultat": [[1.0,4.0],[2.0,5.0],[3.0,6.0]]}`

---

### POST /matrices/determinant
Calcule le déterminant d'une matrice carrée.

**Corps JSON :** `{"A": [[1,2],[3,4]]}`  
**Réponse 200 :** `{"operation": "determinant", "resultat": -2.0}`  
**Erreur 400 :** matrice non carrée

---

### POST /matrices/inverse
Calcule l'inverse d'une matrice carrée non singulière.

**Corps JSON :** `{"A": [[1,2],[3,4]]}`  
**Réponse 200 :** `{"operation": "inverse", "resultat": [[-2.0,1.0],[1.5,-0.5]]}`  
**Erreur 400 :** matrice singulière ou non carrée

## Tests

```bash
# Tests Python
python test_service1.py

# Test curl rapide
curl -X POST http://localhost:5001/matrices/add \
     -H 'Content-Type: application/json' \
     -d '{"A": [[1,2],[3,4]], "B": [[5,6],[7,8]]}'
```

Ouvrir `test_service1.html` dans un navigateur pour les tests visuels.
