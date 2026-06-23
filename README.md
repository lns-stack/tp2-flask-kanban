# flask-services-kanban

Projet BUT Informatique 1ère Année — TP #2  
Développement de microservices web Python Flask, géré avec GitHub Projects & Kanban.

## Architecture

| Service | Description | Port |
|---------|-------------|------|
| service1_matrices | Calculs matriciels (NumPy) | 5001 |
| service2_statistiques | Statistiques sur données JSON (SciPy) | 5002 |
| service3_stats_mysql | Statistiques depuis MySQL | 5003 |
| service4_csv_mysql | Chargement CSV → MySQL | 5004 |
| service5_c_python | Fonctions C appelées via ctypes | 5005 |

## Lancement rapide

### Pré-requis
- Python 3.10+
- MySQL 8.0+
- gcc (pour le Service 5)

### Base de données (Services 3 & 4)
```bash
mysql -u root -p < sql/init_db.sql
```

### Lancer chaque service
```bash
cd service1_matrices
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Répéter pour les services 2, 3, 4, 5.

### Charger les données de démo (Service 4 → Service 3)
```bash
curl -X POST http://localhost:5004/upload/csv \
     -F 'file=@data/donnees_exemple.csv'
```

## Workflow Git

```
main       ← code validé et testé
develop    ← intégration des features
feature/s1-nom-tache  ← développement
fix/s1-nom-bug        ← corrections
```

## Convention de commits

```
feat(s1): ajoute la route POST /matrices/add
fix(s3): corrige la connexion MySQL
docs(s2): met à jour le README
test(s1): ajoute les tests unitaires
```

## Équipe

| Rôle | Service |
|------|---------|
| Étudiant A (Chef de projet) | Service 1 — Matrices |
| Étudiant B | Service 2 — Statistiques |
| Étudiant C | Service 3 — Stats MySQL |
| Étudiant D | Service 4 — CSV MySQL |
