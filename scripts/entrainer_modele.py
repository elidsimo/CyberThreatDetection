# Jalon 2 - Entrainement d'un modele de detection de phishing


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# 1. Chargement des donnees
df = pd.read_csv("data/dataset.csv")
df = df.dropna()

COLONNE_CIBLE = "Result"  # A adapter selon ton dataset

X = df.drop(columns=[COLONNE_CIBLE])
y = df[COLONNE_CIBLE]

# 2. Separation train / test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Entrainement
modele = LogisticRegression(max_iter=5000)
modele.fit(X_train, y_train)

# 4. Evaluation
y_pred = modele.predict(X_test)
print("Taux de reussite :", accuracy_score(y_test, y_pred))
print()
print(classification_report(y_test, y_pred))
print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))

# 5. Sauvegarde du modele
joblib.dump(modele, "data/modele_phishing.pkl")
print("Modele sauvegarde dans data/modele_phishing.pkl")