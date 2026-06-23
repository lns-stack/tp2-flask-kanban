"""
Tests unitaires Python pour le Service 2 — Statistiques JSON
Usage : python test_service2.py
Le service doit tourner sur http://localhost:5002
"""

import requests

BASE_URL = "http://localhost:5002"

VERT  = "\033[92m"
ROUGE = "\033[91m"
RESET = "\033[0m"

passed = 0
failed = 0

DATA_EXEMPLE = [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]


def test(nom, url, payload, status_attendu, check_fn=None):
    global passed, failed
    try:
        r = requests.post(url, json=payload, timeout=5)
        ok = (r.status_code == status_attendu)
        if ok and check_fn:
            ok = check_fn(r.json())
        if ok:
            print(f"{VERT}✅ PASS{RESET} — {nom}")
            passed += 1
        else:
            print(f"{ROUGE}❌ FAIL{RESET} — {nom}")
            print(f"       Statut reçu : {r.status_code} | Réponse : {r.json()}")
            failed += 1
    except Exception as e:
        print(f"{ROUGE}❌ ERREUR{RESET} — {nom} : {e}")
        failed += 1


print("=" * 55)
print("  Tests Service 2 — Statistiques JSON")
print("=" * 55)

# ── /stats/describe ───────────────────────────────────────────────
test(
    "Describe — données valides (200)",
    f"{BASE_URL}/stats/describe",
    {"data": DATA_EXEMPLE},
    200,
    lambda d: d["resultat"]["n"] == 8
)
test(
    "Describe — clé 'data' manquante (400)",
    f"{BASE_URL}/stats/describe",
    {"valeurs": DATA_EXEMPLE},
    400
)
test(
    "Describe — liste trop courte (400)",
    f"{BASE_URL}/stats/describe",
    {"data": [42.0]},
    400
)

# ── /stats/correlation ────────────────────────────────────────────
test(
    "Corrélation — deux séries valides (200)",
    f"{BASE_URL}/stats/correlation",
    {"x": [1, 2, 3, 4, 5], "y": [2, 4, 5, 4, 5]},
    200,
    lambda d: "r" in d["resultat"]
)
test(
    "Corrélation — longueurs différentes (400)",
    f"{BASE_URL}/stats/correlation",
    {"x": [1, 2, 3], "y": [4, 5]},
    400
)
test(
    "Corrélation — clé 'y' manquante (400)",
    f"{BASE_URL}/stats/correlation",
    {"x": [1, 2, 3]},
    400
)

# ── /stats/test_normalite ─────────────────────────────────────────
test(
    "Test normalité — données valides (200)",
    f"{BASE_URL}/stats/test_normalite",
    {"data": DATA_EXEMPLE},
    200,
    lambda d: "est_normale" in d["resultat"]
)
test(
    "Test normalité — données trop courtes (400)",
    f"{BASE_URL}/stats/test_normalite",
    {"data": [1.0]},
    400
)

# ── /stats/test_student ───────────────────────────────────────────
test(
    "Test Student — deux groupes valides (200)",
    f"{BASE_URL}/stats/test_student",
    {"groupe1": [10, 11, 12, 13], "groupe2": [20, 21, 22, 23]},
    200,
    lambda d: "difference_significative" in d["resultat"]
)
test(
    "Test Student — groupe2 manquant (400)",
    f"{BASE_URL}/stats/test_student",
    {"groupe1": [10, 11, 12]},
    400
)

print("=" * 55)
print(f"  Résultat : {passed} réussi(s), {failed} échoué(s)")
print("=" * 55)
