
# Extension - Collecte des adresses IP malveillantes via AbuseIPDB

import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ABUSEIPDB_API_KEY")

URL = "https://api.abuseipdb.com/api/v2/blacklist"

headers = {
    "Key": API_KEY,
    "Accept": "application/json",
}

params = {
    "confidenceMinimum": "90",   # ne garder que les IP a haute confiance de malveillance
    "limit": "1000",             # nombre max d'IPs recuperees
}


def telecharger_ips():
    reponse = requests.get(URL, headers=headers, params=params)
    reponse.raise_for_status()  # leve une erreur claire si la requete echoue

    donnees = reponse.json()["data"]
    df = pd.DataFrame(donnees)

    print(f"{len(df)} adresses IP malveillantes recuperees.")
    print(df.head())

    df.to_csv("data/ips_malveillantes.csv", index=False)
    print("Sauvegarde dans data/ips_malveillantes.csv")

    return df


if __name__ == "__main__":
    telecharger_ips()