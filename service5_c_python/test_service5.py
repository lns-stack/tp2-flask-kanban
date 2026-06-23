"""
Tests unitaires Python pour le Service 5 — C/ctypes
Usage : python test_service5.py
Pré-requis : ./compile.sh exécuté + service Flask sur http://localhost:5005
"""

import requests

BASE_URL = "http://localhost:5005"

VERT  = "\033[92m"
ROUGE = "\033[91m"
RESET = "\033[0m"

passed = 0
failed = 0

DATA = [12.5, 15.3, 8.7, 21.0, 13.2, 9.8, 17.6, 11.4]


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


def test_get(nom, url, status_attendu, check_fn=None):
    global passed, failed
    try:
        r = requests.get(url, timeout=5)
        ok = (r.status_code == status_attendu)
        if ok and check_fn:
            ok = check_fn(r.json())
        if ok:
            print(f"{VERT}✅ PASS{RESET} — {nom}")
            passed += 1
        else:
            print(f"{ROUGE}❌ FAIL{RESET} — {nom}")
            failed += 1
    except Exception as e:
        print(f"{ROUGE}❌ ERREUR{RESET} — {nom} : {e}")
        failed += 1


print("=" * 55)
print("  Tests Service 5 — C/ctypes")
print("=" * 55)

# ── Health check ─────────────────────────────────────────────────
test_get(
    "Health check (200)",
    f"{BASE_URL}/c/health", 200,
    lambda d: d["statut"] == "ok"
)

# ── /c/stats/describe ─────────────────────────────────────────────
test(
    "Describe complet (200)",
    f"{BASE_URL}/c/stats/describe",
    {"data": DATA}, 200,
    lambda d: d["moteur"] == "C/ctypes" and d["resultat"]["n"] == 8
)
test(
    "Describe — clé 'data' manquante (400)",
    f"{BASE_URL}/c/stats/describe",
    {"valeurs": DATA}, 400
)

# ── /c/stats/mean ─────────────────────────────────────────────────
test(
    "Moyenne — valide (200)",
    f"{BASE_URL}/c/stats/mean",
    {"data": DATA}, 200,
    lambda d: abs(d["resultat"] - 13.6875) < 0.001
)

# ── /c/stats/stddev ───────────────────────────────────────────────
test(
    "Écart-type — valide (200)",
    f"{BASE_URL}/c/stats/stddev",
    {"data": DATA}, 200,
    lambda d: d["resultat"] > 0
)
test(
    "Écart-type — trop court (400)",
    f"{BASE_URL}/c/stats/stddev",
    {"data": [42.0]}, 400
)

# ── /c/stats/median ───────────────────────────────────────────────
test(
    "Médiane — valide (200)",
    f"{BASE_URL}/c/stats/median",
    {"data": DATA}, 200,
    lambda d: d["resultat"] > 0
)

# ── /c/stats/dot ──────────────────────────────────────────────────
test(
    "Produit scalaire [1,2,3]·[4,5,6] = 32 (200)",
    f"{BASE_URL}/c/stats/dot",
    {"v1": [1, 2, 3], "v2": [4, 5, 6]}, 200,
    lambda d: abs(d["resultat"] - 32.0) < 0.001
)
test(
    "Produit scalaire — longueurs différentes (400)",
    f"{BASE_URL}/c/stats/dot",
    {"v1": [1, 2, 3], "v2": [4, 5]}, 400
)

print("=" * 55)
print(f"  Résultat : {passed} réussi(s), {failed} échoué(s)")
print("=" * 55)
