# Journal de Bord & Documentation du Mini-Projet (R5.C.06)

> **Module** : R5.C.06 - Exploitation de bases de données  
> **Formation** : BUT Informatique - Semestre 5  
> **Sujet** : Système Décisionnel d'Implantation Optimale de Bornes de Recharge Électriques (IRVE)  
> **Contrainte maîtresse** : **Modélisation mathématique et optimisation HORS Machine Learning**  
> **Dépôt Git** : [mini-proj](https://github.com/UGODPC/mini-proj.git)

---

## 1. Contexte & Problématique Métier

### 1.1 Problème décisionnel
Dans le cadre de la transition énergétique, les collectivités et opérateurs d'infrastructures de recharge pour véhicules électriques (IRVE) doivent décider de l'implantation de nouvelles bornes sous de fortes contraintes :
* **Contrainte budgétaire** : Enveloppe financière annuelle limitée pour l'achat et l'installation.
* **Contrainte de puissance et de maillage** : Éviter les zones saturées, combler les déserts de recharge, équilibrer entre recharge accélérée (22 kW) et recharge ultra-rapide (> 150 kW).
* **Contrainte d'accessibilité** : Prioriser les emplacements accessibles 24/7 et stratégiques.

### 1.2 Objectif du système
Concevoir un outil d'aide à la décision capable de :
1. **Évaluer et scorer** chaque zone candidate (communes/arrondissements) selon plusieurs critères contradictoires.
2. **Résoudre un problème d'optimisation combinatoire (PLNE)** pour sélectionner la combinaison exacte d'implantations qui maximise le gain d'utilité collective sous un budget alloué $B$.
3. **Fournir une simulation dynamique** (démo live) où le décideur peut tester différents scénarios budgétaires et pondérations politiques.

---

## 2. Référencement & Traçabilité des Données (Open Data)

Toutes les données utilisées sont ouvertes, officielles et vérifiables :

| Source | Description | URL / Référence | Format |
|---|---|---|---|
| **Point d'Accès National (PAN)** | Base nationale consolidée des infrastructures de recharge pour véhicules électriques (IRVE - données statiques) | [transport.data.gouv.fr/datasets/base-nationale-des-points-de-recharge-pour-vehicules-electriques-en-france-irve](https://transport.data.gouv.fr/datasets/base-nationale-des-points-de-recharge-pour-vehicules-electriques-en-france-irve) | CSV |
| **Etalab** | Schéma national officiel des données IRVE statiques | [schema.data.gouv.fr/etalab/schema-irve-statique](https://schema.data.gouv.fr/etalab/schema-irve-statique/) | Spécification v2.3.1 |
| **data.gouv.fr** | Identifiants et métadonnées nationales consolidées chaque nuit | [data.gouv.fr - IRVE France](https://www.data.gouv.fr/fr/datasets/base-nationale-des-points-de-recharge-pour-vehicules-electriques-en-france-irve/) | API & CSV |
| **INSEE (optionnel)** | Populations et découpages géographiques communaux (COG) | [insee.fr/fr/information/2560452](https://www.insee.fr) | CSV |

### Caractéristiques principales des données IRVE :
* `id_station_itinerance` / `id_pdc_itinerance` : Identifiants uniques normalisés.
* `nom_station` & `nom_amenageur` : Opérateur responsable.
* `coordonneesXY` : Géolocalisation `[longitude, latitude]`.
* `puissance_nominale` : Puissance de charge délivrée (en kW).
* `prise_type_2`, `prise_type_combo_ccs`, `prise_type_chademo` : Types de prises.
* `accessibilite_pmr`, `horaires` : Disponibilité 24/7 et PMR.
* `code_insee_commune` : Rapprochement territorial.

---

## 3. Modélisation Mathématique (100% Hors ML)

Le projet couple deux méthodes reconnues en recherche opérationnelle et décisionnel :

### 3.1 Méthode 1 : Scoring Multicritère TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)
Pour chaque zone candidate $i \in \{1, \dots, m\}$ et pour chaque critère $j \in \{1, \dots, n\}$ :
1. **Matrice de décision normalisée** :
   $$r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{k=1}^m x_{kj}^2}}$$
2. **Matrice pondérée** (avec $\sum w_j = 1$) :
   $$v_{ij} = w_j \cdot r_{ij}$$
3. **Solutions idéales positive ($A^+$) et négative ($A^-$)** :
   $$A^+ = \{ \max_i v_{ij} \text{ si critère à maximiser}, \min_i v_{ij} \text{ si critère à minimiser} \}$$
   $$A^- = \{ \min_i v_{ij} \text{ si critère à maximiser}, \max_i v_{ij} \text{ si critère à minimiser} \}$$
4. **Distances euclidiennes** :
   $$S_i^+ = \sqrt{\sum_{j=1}^n (v_{ij} - v_j^+)^2}, \quad S_i^- = \sqrt{\sum_{j=1}^n (v_{ij} - v_j^-)^2}$$
5. **Indice de proximité relative (Score final)** :
   $$C_i = \frac{S_i^-}{S_i^+ + S_i^-} \quad \in [0, 1]$$
   Plus $C_i$ est proche de 1, plus la zone candidate est prioritaire pour accueillir une borne.

### 3.2 Méthode 2 : Programmation Linéaire en Nombres Entiers (PLNE - 0/1 Knapsack)
Une fois les scores $C_i$ calculés, le décideur dispose d'un budget total $B$. Chaque projet d'implantation $i$ a un coût estimé $c_i$.

* **Variable de décision binaire** :
  $$x_i \in \{0, 1\} \quad \text{(1 si on implante la borne dans la zone } i\text{, 0 sinon)}$$
* **Fonction objectif (Maximisation de l'utilité globale)** :
  $$\max \sum_{i=1}^m C_i \cdot x_i$$
* **Contrainte budgétaire stricte** :
  $$\sum_{i=1}^m c_i \cdot x_i \le B$$
* **Contraintes géographiques optionnelles** (ex: au moins $k$ bornes par sous-secteur).

---

## 4. Architecture Prévue du Projet

```text
mini-proj/
├── consigne/
│   └── Rendu de mini projet.pdf
├── data/
│   ├── raw/                  # Données brutes téléchargées (CSV IRVE)
│   └── processed/            # Données nettoyées et agrégées par zone
├── src/
│   ├── __init__.py
│   ├── data_loader.py        # Chargement, filtrage et nettoyage
│   ├── eda.py                # Visualisations et statistiques descriptives
│   ├── topsis.py             # Implémentation mathématique de TOPSIS
│   └── optimizer.py          # Résolution du problème d'optimisation (PuLP / SciPy)
├── notebooks/
│   └── 01_exploration.ipynb  # Analyse exploratoire et graphiques pour le rapport
├── app.py                    # Démo interactive (Streamlit ou CLI riche) pour l'oral
├── report/                   # Éléments rédigés du rapport final
├── DOCUMENTATION.md          # Le présent document de traçabilité
├── requirements.txt          # Dépendances (pandas, numpy, scipy, pulp, matplotlib, streamlit)
└── README.md                 # Guide d'exécution
```

---

## 5. Journal des Actions & Historique

* **2026-11-23** :
  * Analyse approfondie des consignes du mini-projet (`consigne/Rendu de mini projet.pdf`).
  * Confirmation de la contrainte stricte : **Modèle mathématique / statistique HORS Machine Learning**.
  * Choix validé de la thématique : **Base Nationale IRVE (Infrastructures de Recharge pour Véhicules Électriques)**.
  * Formalisation mathématique : Couplage **TOPSIS** (Aide à la décision multicritère) + **PLNE** (Optimisation sac à dos budgétaire).
  * Création de la documentation et du journal de bord (`DOCUMENTATION.md`).
