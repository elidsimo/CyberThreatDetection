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

## Jalon 2 — Modele de detection

- `scripts/entrainer_modele.py` entraine un modele de regression logistique
  sur le dataset Kaggle "Phishing website dataset" (Akash Kumar, 11 055 lignes,
  30 caracteristiques deja numeriques).
- Le modele entraine est sauvegarde dans `data/modele_phishing.pkl`.
- Taux de reussite obtenu : 92.9% (accuracy).
- Sur 980 sites de phishing reels dans le jeu de test, 886 sont correctement
  detectes et 94 sont manques (faux negatifs, rappel de 90%).
- Sur 1231 sites legitimes, 1168 sont correctement reconnus et 63 sont
  signales a tort comme phishing (faux positifs).

## Jalon 3 — Prototype complet

- `app/dashboard.py` : tableau de bord Streamlit permettant de charger un CSV
  d'URLs, d'obtenir une prediction (phishing/legitime) via le modele du Jalon 2,
  et de declencher une alerte email.
- `scripts/envoyer_alerte.py` : envoi d'une alerte email via smtplib lorsqu'une
  menace est detectee.
- `docs/fiches_reflexes.md` : 3 fiches pratiques a destination d'une PME.

### Lancer le prototype

powershell
pip install -r requirements.txt
streamlit run app/dashboard.py


## Extension — Détection d'IP malveillantes (AbuseIPDB)

- `scripts/telecharger_ips.py` récupère une liste d'IPs malveillantes via
  l'API gratuite AbuseIPDB (endpoint `/blacklist`, confiance >= 90%).
- Contrairement au phishing, cette détection ne nécessite pas de modèle ML :
  une simple vérification par liste (l'IP est-elle dans la blacklist ?) suffit.
- Le dashboard propose un second onglet permettant de consulter la liste
  complète ou de vérifier une IP précise.

  ## Extension — Domaines malveillants (URLhaus) et signatures de malwares (MalwareBazaar)

- `scripts/telecharger_domaines.py` récupère une liste de domaines malveillants
  via le flux hostfile d'URLhaus.
- `scripts/telecharger_hashes_malwares.py` récupère une liste de hashes SHA256
  de malwares connus via MalwareBazaar (abuse.ch).
- `scripts/verifier_hash.py` calcule le hash d'un fichier local et le compare
  à la liste de hashes connus.
- Ces deux briques suivent la même logique que la détection d'IP : comparaison
  par liste.