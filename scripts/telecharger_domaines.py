# Extension - Collecte des noms de domaine malveillants via URLhaus (hostfile)
import requests
import pandas as pd

URL = "https://urlhaus.abuse.ch/downloads/hostfile/"


def telecharger_domaines():
    reponse = requests.get(URL)
    reponse.raise_for_status()

    lignes = reponse.text.splitlines()

    domaines = []
    for ligne in lignes:
        ligne = ligne.strip()
        if ligne.startswith("#") or not ligne:
            continue
        parties = ligne.split()
        if len(parties) == 2:
            domaines.append(parties[1])

        # Le fichier hosts contient des lignes de commentaire (#) et des lignes
        # au format : "127.0.0.1 domaine-malveillant.com"
    df = pd.DataFrame({"domaine": domaines})
    df = df.drop_duplicates().reset_index(drop=True)

    print(f"{len(df)} domaines malveillants recuperes.")
    print(df.head())

    df.to_csv("data/domaines_malveillants.csv", index=False)
    print("Sauvegarde dans data/domaines_malveillants.csv")

    return df


if __name__ == "__main__":
    telecharger_domaines()