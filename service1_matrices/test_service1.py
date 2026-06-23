"""
Tests unitaires Python pour le Service 1 — Calculs Matriciels
Usage : python test_service1.py
Le service doit tourner sur http://localhost:5001
"""

import requests
import json

BASE_URL = "http://localhost:5001"

VERT  = "\033[92m"
ROUGE = "\033[91m"
RESET = "\033[0m"

passed = 0
failed = 0


def test(nom, url, payload, status_attendu, cle_resultat=None, valeur_attendue=None):
    global passed, failed
    try:
        r = requests.post(url, json=payload, timeout=5)
        ok_status = (r.status_code == status_attendu)
        ok_valeur = True

        if cle_resultat and valeur_attendue is not None:
            data = r.json()
            ok_valeur = (data.get(cle_resultat) == valeur_attendue)

        if ok_status and ok_valeur:
            print(f"{VERT}✅ PASS{RESET} — {nom}")
            passed += 1
        else:
            print(f"{ROUGE}❌ FAIL{RESET} — {nom}")
            print(f"       Statut : attendu {status_attendu}, reçu {r.status_code}")
            if not ok_valeur:
                print(f"       Valeur '{cle_resultat}' : attendu {valeur_attendue}, reçu {r.json().get(cle_resultat)}")
            failed += 1
    except Exception as e:
        print(f"{ROUGE}❌ ERREUR{RESET} — {nom} : {e}")
        failed += 1


print("=" * 55)
print("  Tests Service 1 — Matrices")
print("=" * 55)

# ── Addition ──────────────────────────────────────────────────────
test(
    "Addition 2x2 basique",
    f"{BASE_URL}/matrices/add",
    {"A": [[1, 2], [3, 4]], "B": [[5, 6], [7, 8]]},
    200,
    "operation", "addition"
)
test(
    "Addition — dimensions incompatibles → 400",
    f"{BASE_URL}/matrices/add",
    {"A": [[1, 2]], "B": [[1, 2], [3, 4]]},
    400
)
test(
    "Addition — matrice manquante → 400",
    f"{BASE_URL}/matrices/add",
    {"A": [[1, 2]]},
    400
)

# ── Multiplication ────────────────────────────────────────────────
test(
    "Multiplication 2x2",
    f"{BASE_URL}/matrices/multiply",
    {"A": [[1, 2], [3, 4]], "B": [[5, 6], [7, 8]]},
    200,
    "operation", "multiplication"
)
test(
    "Multiplication — colonnes/lignes incompatibles → 400",
    f"{BASE_URL}/matrices/multiply",
    {"A": [[1, 2, 3]], "B": [[1, 2], [3, 4]]},
    400
)

# ── Transposition ─────────────────────────────────────────────────
test(
    "Transposition 2x3",
    f"{BASE_URL}/matrices/transpose",
    {"A": [[1, 2, 3], [4, 5, 6]]},
    200,
    "operation", "transposee"
)

# ── Déterminant ───────────────────────────────────────────────────
test(
    "Déterminant matrice 2x2",
    f"{BASE_URL}/matrices/determinant",
    {"A": [[1, 2], [3, 4]]},
    200,
    "operation", "determinant"
)
test(
    "Déterminant — matrice non carrée → 400",
    f"{BASE_URL}/matrices/determinant",
    {"A": [[1, 2, 3], [4, 5, 6]]},
    400
)

# ── Inverse ───────────────────────────────────────────────────────
test(
    "Inverse matrice 2x2",
    f"{BASE_URL}/matrices/inverse",
    {"A": [[1, 2], [3, 4]]},
    200,
    "operation", "inverse"
)
test(
    "Inverse — matrice singulière → 400",
    f"{BASE_URL}/matrices/inverse",
    {"A": [[1, 2], [2, 4]]},
    400
)
test(
    "Inverse — matrice non carrée → 400",
    f"{BASE_URL}/matrices/inverse",
    {"A": [[1, 2, 3], [4, 5, 6]]},
    400
)

print("=" * 55)
print(f"  Résultat : {passed} réussi(s), {failed} échoué(s)")
print("=" * 55)
