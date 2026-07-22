# Extension - Calcul du hash SHA256 d'un fichier et verification
# contre la liste de hashes malveillants connus

import hashlib
import pandas as pd


def calculer_sha256(chemin_fichier):
    sha256 = hashlib.sha256()
    with open(chemin_fichier, "rb") as f:
        for bloc in iter(lambda: f.read(8192), b""):
            sha256.update(bloc)
    return sha256.hexdigest()


def normaliser_colonnes(df):
    df.columns = [str(c).strip().strip('"').lstrip("#").strip().lower() for c in df.columns]
    return df


def verifier_fichier(chemin_fichier, chemin_liste_hashes="data/hashes_malwares.csv"):
    hash_calcule = calculer_sha256(chemin_fichier)
    df = pd.read_csv(chemin_liste_hashes)
    df = normaliser_colonnes(df)

    if "sha256_hash" not in df.columns:
        print("Le CSV est invalide. Colonnes disponibles :", list(df.columns))
        print("Relance d'abord scripts\\telecharger_hashes_malwares.py")
        return False, None

    resultat = df[df["sha256_hash"] == hash_calcule]

    if not resultat.empty:
        print("ALERTE : le fichier correspond à un malware connu !")
        colonnes = [c for c in ["file_name", "signature"] if c in resultat.columns]
        if colonnes:
            print(resultat[colonnes].to_string(index=False))
        return True, resultat

    print(f"Aucune correspondance trouvée pour le hash {hash_calcule}")
    return False, None


if __name__ == "__main__":
    chemin_test = "data/dataset.csv"
    verifier_fichier(chemin_test)