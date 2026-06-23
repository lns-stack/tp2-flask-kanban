"""
Tests unitaires Python pour le Service 3 — Statistiques depuis MySQL
Usage : python test_service3.py
Pré-requis : service Flask sur http://localhost:5003 + BDD chargée
(lancer service4 et uploader donnees_exemple.csv d'abord)
"""

import requests

BASE_URL = "http://localhost:5003"

VERT  = "\033[92m"
ROUGE = "\033[91m"
RESET = "\033[0m"

passed = 0
failed = 0


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
            print(f"       Statut reçu : {r.status_code} | Réponse : {r.json()}")
            failed += 1
    except Exception as e:
        print(f"{ROUGE}❌ ERREUR{RESET} — {nom} : {e}")
        failed += 1


print("=" * 55)
print("  Tests Service 3 — Stats MySQL")
print("=" * 55)

# ── /db/stats/describe ────────────────────────────────────────────
test_get(
    "Describe serie_A (200)",
    f"{BASE_URL}/db/stats/describe?serie=serie_A",
    200,
    lambda d: d["resultat"]["n"] >= 5 and d["source"] == "mysql"
)
test_get(
    "Describe — paramètre manquant (400)",
    f"{BASE_URL}/db/stats/describe",
    400
)
test_get(
    "Describe — série inexistante (404)",
    f"{BASE_URL}/db/stats/describe?serie=serie_INEXISTANTE",
    404
)

# ── /db/stats/correlation ─────────────────────────────────────────
test_get(
    "Corrélation serie_A / serie_B (200)",
    f"{BASE_URL}/db/stats/correlation?serie_x=serie_A&serie_y=serie_B",
    200,
    lambda d: "r" in d["resultat"] and d["source"] == "mysql"
)
test_get(
    "Corrélation — serie_x manquant (400)",
    f"{BASE_URL}/db/stats/correlation?serie_y=serie_B",
    400
)
test_get(
    "Corrélation — serie_x inexistante (404)",
    f"{BASE_URL}/db/stats/correlation?serie_x=INCONNUE&serie_y=serie_B",
    404
)

print("=" * 55)
print(f"  Résultat : {passed} réussi(s), {failed} échoué(s)")
print("=" * 55)
