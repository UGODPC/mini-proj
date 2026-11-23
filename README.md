# Mini-Projet R5.C.06 - Système Décisionnel d'Implantation Optimale de Bornes IRVE

Projet universitaire d'exploitation de bases de données et d'aide à la décision (BUT Informatique Semestre 5).

## 🎯 Problématique Métier
Optimiser le déploiement et l'implantation de nouvelles bornes de recharge pour véhicules électriques (IRVE) à l'échelle d'un territoire (ex: département ou région) sous contrainte budgétaire, sans recourir au Machine Learning.

## 📐 Modélisation Mathématique
1. **Scoring Multicritère (TOPSIS)** : Évaluation et hiérarchisation des zones d'implantation prioritaires selon des critères contradictoires (puissance installée, desserte, disponibilité, maillage).
2. **Optimisation Combinatoire (PLNE / Sac à dos 0-1)** : Sélection optimale des projets d'implantation sous contrainte d'enveloppe budgétaire avec un solveur linéaire (`PuLP`).

## 📁 Structure du Projet
```text
├── consigne/             # Sujet et critères d'évaluation officiels
├── data/
│   ├── raw/              # Données brutes (Base Nationale IRVE)
│   └── processed/        # Données agrégées et nettoyées
├── src/                  # Code source modulaire
│   ├── download_data.py  # Script de téléchargement automatique
│   ├── data_loader.py    # Prétraitement et filtres territoriaux
│   ├── topsis.py         # Moteur de décision multicritère
│   └── optimizer.py      # Moteur d'optimisation sous contraintes
├── notebooks/            # Analyses exploratoires et visualisations (EDA)
├── app.py                # Application interactive pour la démo live (Streamlit)
├── DOCUMENTATION.md      # Journal de bord complet et traçabilité mathématique
└── requirements.txt      # Dépendances Python
```

## 🚀 Installation & Exécution
```bash
# 1. Création de l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# 2. Installation des dépendances
pip install -r requirements.txt

# 3. Téléchargement des données IRVE
python src/download_data.py

# 4. Lancement de la démonstration interactive
streamlit run app.py
```
