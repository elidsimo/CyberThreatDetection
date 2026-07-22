from pathlib import Path
import sys

import streamlit as st
import pandas as pd
import joblib

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.envoyer_alerte import envoyer_alerte

st.set_page_config(page_title="Détection de Cybermenaces - PME", layout="wide")

st.title("Système de détection de cybermenaces")
st.write("Prototype de veille et d'alerte précoce pour PME — Stage PFA CMRPI/EMC")

onglet_phishing, onglet_ips, onglet_domaines, onglet_malwares = st.tabs(
    ["Phishing (URLs)", "IPs malveillantes", "Domaines malveillants", "Signatures malwares"]
)

# ONGLET 1 - PHISHING (Jalon 3, inchangé, juste indenté)
with onglet_phishing:
    # Chargement du modele entraine au Jalon 2
    modele = joblib.load(ROOT_DIR / "data" / "modele_phishing.pkl")

    st.header("Analyser des URLs")
    st.write(
        "Cette version utilise le fichier CSV de caractéristiques déjà extraites "
    )

    fichier = st.file_uploader("Charger un fichier CSV d'URLs à analyser", type=["csv"])

    if fichier is not None:
        df = pd.read_csv(fichier)

        if "index" in df.columns:
            df = df.drop(columns=["index"])
        if "Result" in df.columns:
            df = df.drop(columns=["Result"])  # on ne garde pas la vraie etiquette si presente

        predictions = modele.predict(df)

        df_resultats = df.copy()
        df_resultats["Prediction"] = ["Phishing" if p == -1 else "Légitime" for p in predictions]

        st.subheader("Résultats")
        st.dataframe(df_resultats)

        nb_phishing = (df_resultats["Prediction"] == "Phishing").sum()
        nb_legitime = (df_resultats["Prediction"] == "Légitime").sum()

        col1, col2 = st.columns(2)
        col1.metric("URLs détectées phishing", nb_phishing)
        col2.metric("URLs légitimes", nb_legitime)

        if nb_phishing > 0:
            st.error(f"{nb_phishing} menace(s) de phishing détectée(s) !")
            if st.button("Envoyer une alerte", key="alerte_phishing"):
                urls_phishing = df_resultats[df_resultats["Prediction"] == "Phishing"]
                lignes_suspectes = ", ".join(str(url) for url in urls_phishing.index)
                message_alerte = (
                    f"{nb_phishing} URL(s) suspecte(s) détectée(s). "
                    f"Lignes concernées : {lignes_suspectes}"
                )
                envoyer_alerte(message_alerte)
                st.success("Alerte(s) envoyée(s) !")
        else:
            st.success("Aucune menace détectée dans ce lot.")
    else:
        st.info("Charge un fichier CSV pour lancer l'analyse.")

# ONGLET 2 - IPs MALVEILLANTES (AbuseIPDB)
with onglet_ips:
    st.header("Adresses IP malveillantes (source : AbuseIPDB)")

    chemin_ips = ROOT_DIR / "data" / "ips_malveillantes.csv"

    if chemin_ips.exists():
        df_ips = pd.read_csv(chemin_ips)

        st.write(f"{len(df_ips)} adresses IP recensées (score de confiance 100).")
        st.dataframe(df_ips)

        st.subheader("Répartition par pays")
        st.bar_chart(df_ips["countryCode"].value_counts().head(10))

        st.subheader("Vérifier une IP précise")
        ip_a_verifier = st.text_input("Entrer une adresse IP", key="recherche_ip")

        if ip_a_verifier:
            resultat = df_ips[df_ips["ipAddress"] == ip_a_verifier]
            if not resultat.empty:
                st.error(f" {ip_a_verifier} est présente dans la liste des IPs malveillantes.")
                st.dataframe(resultat)
                if st.button("Envoyer une alerte", key="alerte_ip"):
                    envoyer_alerte(f"Adresse IP malveillante détectée : {ip_a_verifier}")
                    st.success("Alerte envoyée !")
            else:
                st.success(f"{ip_a_verifier} n'est pas dans la liste (pas de garantie absolue).")
    else:
        st.warning("Aucune donnée IP disponible. Lance d'abord `python scripts\\telecharger_ips.py`.")

# ONGLET 3 - DOMAINES MALVEILLANTS (URLhaus)
with onglet_domaines:
    st.header("Noms de domaine malveillants (source : URLhaus)")

    chemin_domaines = ROOT_DIR / "data" / "domaines_malveillants.csv"

    if chemin_domaines.exists():
        df_domaines = pd.read_csv(chemin_domaines)
        st.write(f"{len(df_domaines)} domaines recensés.")
        st.dataframe(df_domaines)

        st.subheader("Vérifier un domaine")
        domaine_a_verifier = st.text_input("Entrer un nom de domaine", key="recherche_domaine")

        if domaine_a_verifier:
            resultat = df_domaines[df_domaines["domaine"] == domaine_a_verifier]
            if not resultat.empty:
                st.error(f"{domaine_a_verifier} est présent dans la liste des domaines malveillants.")
                if st.button("Envoyer une alerte", key="alerte_domaine"):
                    envoyer_alerte(f"Nom de domaine malveillant détecté : {domaine_a_verifier}")
                    st.success("Alerte envoyée !")
            else:
                st.success(f"{domaine_a_verifier} n'est pas dans la liste (pas de garantie absolue).")
    else:
        st.warning("Aucune donnée disponible. Lance d'abord `python scripts\\telecharger_domaines.py`.")

# ONGLET 4 - SIGNATURES DE MALWARES (MalwareBazaar)
with onglet_malwares:
    st.header("Signatures de malwares connus (source : MalwareBazaar)")

    chemin_hashes = ROOT_DIR / "data" / "hashes_malwares.csv"

    if chemin_hashes.exists():
        df_hashes = pd.read_csv(chemin_hashes)
        st.write(f"{len(df_hashes)} signatures recensées.")
        st.dataframe(df_hashes[["sha256_hash", "file_name", "signature"]])

        st.subheader("Vérifier un fichier local")
        fichier_a_verifier = st.file_uploader("Charger un fichier à vérifier", key="upload_malware")

        if fichier_a_verifier is not None:
            import hashlib
            hash_calcule = hashlib.sha256(fichier_a_verifier.getvalue()).hexdigest()
            st.write(f"Hash SHA256 calculé : `{hash_calcule}`")

            resultat = df_hashes[df_hashes["sha256_hash"] == hash_calcule]
            if not resultat.empty:
                st.error("Ce fichier correspond à un malware connu !")
                st.dataframe(resultat[["file_name", "signature"]])
            else:
                st.success("Aucune correspondance trouvée dans la base MalwareBazaar.")
    else:
        st.warning("Aucune donnée disponible. Lance d'abord `python scripts\\telecharger_hashes_malwares.py`.")