"""
Tests unitaires Python pour le Service 4 — Upload CSV → MySQL
Usage : python test_service4.py
Le service doit tourner sur http://localhost:5004
"""

import requests
import os

BASE_URL = "http://localhost:5004"

VERT  = "\033[92m"
ROUGE = "\033[91m"
RESET = "\033[0m"

passed = 0
failed = 0

CSV_VALIDE = b"""nom_serie,valeur,categorie,date_mesure
test_serie,10.5,test,2024-06-01
test_serie,20.0,test,2024-06-02
test_serie,15.3,test,2024-06-03
"""

CSV_SANS_VALEUR = b"""nom_serie,categorie
test_serie,test
"""

CSV_VALEUR_NON_NUM = b"""nom_serie,valeur
test_serie,abc
test_serie,def
"""

CSV_MIXTE = b"""nom_serie,valeur,categorie
bon_serie,12.0,ok
mauvaise_serie,xyz,ko
bon_serie,14.5,ok
"""


def test_upload(nom, content, filename, status_attendu, check_fn=None):
    global passed, failed
    try:
        files = {'file': (filename, content, 'text/csv')}
        r = requests.post(f"{BASE_URL}/upload/csv", files=files, timeout=5)
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
            print(f"       Statut reçu : {r.status_code} | Réponse : {r.json()}")
            failed += 1
    except Exception as e:
        print(f"{ROUGE}❌ ERREUR{RESET} — {nom} : {e}")
        failed += 1


print("=" * 55)
print("  Tests Service 4 — Upload CSV → MySQL")
print("=" * 55)

# ── Upload valide ─────────────────────────────────────────────────
test_upload(
    "Upload CSV valide (201)",
    CSV_VALIDE, "test.csv", 201,
    lambda d: d["statut"] == "success" and d["lignes_inserees"] == 3
)

# ── Pas de fichier ─────────────────────────────────────────────────
r = requests.post(f"{BASE_URL}/upload/csv", timeout=5)
ok = r.status_code == 400
print(f"{VERT if ok else ROUGE}{'✅ PASS' if ok else '❌ FAIL'}{RESET} — Pas de fichier (400)")
if ok: passed += 1
else: failed += 1

# ── Mauvaise extension ────────────────────────────────────────────
test_upload(
    "Extension non .csv (400)",
    CSV_VALIDE, "data.txt", 400
)

# ── Colonnes manquantes ───────────────────────────────────────────
test_upload(
    "Colonne 'valeur' manquante (400)",
    CSV_SANS_VALEUR, "bad.csv", 400
)

# ── Toutes les valeurs invalides ──────────────────────────────────
test_upload(
    "Toutes valeurs non numériques (400)",
    CSV_VALEUR_NON_NUM, "bad_nums.csv", 400
)

# ── CSV mixte : lignes valides + invalides ────────────────────────
test_upload(
    "CSV mixte — lignes invalides ignorées (201)",
    CSV_MIXTE, "mixte.csv", 201,
    lambda d: d["lignes_inserees"] == 2 and d["lignes_invalides_ignorees"] == 1
)

# ── Liste des séries ──────────────────────────────────────────────
test_get(
    "Liste des séries (200)",
    f"{BASE_URL}/upload/series", 200,
    lambda d: "series" in d and "total" in d
)

# ── Fichier CSV de démo ───────────────────────────────────────────
demo_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'donnees_exemple.csv')
if os.path.exists(demo_path):
    with open(demo_path, 'rb') as f:
        test_upload(
            "Upload donnees_exemple.csv (201)",
            f.read(), "donnees_exemple.csv", 201,
            lambda d: d["lignes_inserees"] == 30
        )
else:
    print(f"\033[93m⚠️  SKIP{RESET} — donnees_exemple.csv introuvable")

print("=" * 55)
print(f"  Résultat : {passed} réussi(s), {failed} échoué(s)")
print("=" * 55)
