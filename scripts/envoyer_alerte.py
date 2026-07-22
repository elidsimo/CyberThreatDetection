
# Jalon 3 - Envoi d'une alerte email lorsqu'une URL de phishing est detectee
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EXPEDITEUR = os.getenv("EMAIL_EXPEDITEUR")
MOT_DE_PASSE = os.getenv("EMAIL_MOT_DE_PASSE")
DESTINATAIRE = os.getenv("EMAIL_DESTINATAIRE")


def envoyer_alerte(url_suspecte: str | list[str]):
    if isinstance(url_suspecte, list):
        urls_texte = "\n".join(url_suspecte)
        introduction = "Plusieurs URLs suspectes ont ete detectees par le systeme de surveillance :"
    else:
        urls_texte = url_suspecte
        introduction = "Une URL suspecte a ete detectee par le systeme de surveillance :"

    sujet = "Alerte - URL de phishing detectee"
    corps = (
        f"{introduction}\n\n"
        f"{urls_texte}\n\n"
        f"Merci de ne pas cliquer sur ce lien et de le signaler a votre "
        f"responsable informatique.\n\n"
        f"-- Systeme de detection precoce des cybermenaces (CMRPI/EMC)"
    )

    message = MIMEText(corps, "plain", "utf-8")
    message["Subject"] = sujet
    message["From"] = EXPEDITEUR
    message["To"] = DESTINATAIRE

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as serveur:
        serveur.login(EXPEDITEUR, MOT_DE_PASSE)
        serveur.sendmail(EXPEDITEUR, DESTINATAIRE, message.as_string())

    print(f"Alerte envoyee pour : {urls_texte}")


if __name__ == "__main__":
    envoyer_alerte("http://exemple-phishing-test.com/login")