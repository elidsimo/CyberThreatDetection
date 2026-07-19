# CyberThreatDetection

Projet de stage pour explorer des URLs suspectes et préparer un prototype de détection de phishing ciblant les PME.

## Objectif

Le projet compare deux sources publiques de Threat Intelligence:

- URLhaus pour les URLs liées aux malwares, loaders et botnets.
- PhishTank pour les URLs de phishing vérifiées.

L'objectif est de documenter les données, puis de préparer la suite du stage avec un jeu de données plus adapté au phishing.

## Arborescence

- `data/` : fichiers CSV téléchargés.
- `notebooks/` : notebooks d'exploration.
- `scripts/` : scripts de téléchargement.

## Scripts

- `scripts/urls_dow.py` télécharge le flux URLhaus.
- `scripts/telecharger_phishtank.py` télécharge le flux public PhishTank.

## Notebooks

- `notebooks/exploration.ipynb` explore URLhaus et documente le pivot de source.
- `notebooks/phishtank_exploration.ipynb` explore le flux PhishTank.

## Utilisation rapide

```powershell
python scripts/urls_dow.py
python scripts/telecharger_phishtank.py
```

Puis ouvrir les notebooks dans Jupyter ou VS Code pour examiner les données.

## Résultat attendu

Répondre à la question: à quoi ressemblent les données, et quelle source est la plus adaptée pour le phishing?
