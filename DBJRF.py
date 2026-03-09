import subprocess
import datetime
import os
import time
import requests
import json

with open(f"/var/www/mpoesie/appsettings.json") as f:
        data = json.load(f)
        NomMachine = data["machine"]

source = "/home/henry/screenshots"
os.makedirs(source, exist_ok=True)

RETENTION_DAYS = 10
DELAI = 600
URL_SERVER = "http://172.16.127.130/uploadfich/lecture"

print("Capture Wayland avec grim lancée...")

try:
    while True:
        # Capture d'écran
        maintenant = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        chemin_capture = os.path.join(source, f"screenshot_{maintenant}.png")

        try:
            subprocess.run(["grim", chemin_capture], check=True)
            print(f"Capture sauvegardée : {chemin_capture}")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la capture : {e}")
            time.sleep(10)
            continue

        # Gestion des fichiers (Envoi et Nettoyage)
        limite_retention = time.time() - (RETENTION_DAYS * 86400)

        for fichier in os.listdir(source):
            chemin_fichier = os.path.join(source, fichier)

            if not os.path.isfile(chemin_fichier):
                continue

            # Nettoyage si trop vieux
            if os.path.getmtime(chemin_fichier) < limite_retention:
                os.remove(chemin_fichier)
                print(f"Supprimé (ancien) : {fichier}")
                continue # On passe au suivant

            # On n'envoie que le fichier qu'on vient de créer pour éviter les doublons
            if chemin_fichier == chemin_capture:
                try:
                    with open(chemin_fichier, "rb") as f:
                        req = requests.post(f"http://172.16.127.128/uploadfich/lecture?LeChemin={NomMachine}", files={"fichieraudio": f}, timeout=10)

                    if req.status_code == 200 or req.status_code == 201:
                        print(f"Succès : {fichier} envoyé.")
                    else:
                        print(f"Échec serveur ({req.status_code}) pour {fichier} : {req.text}")
                except Exception as e:
                    print(f"Erreur réseau pour {fichier} : {e}")

        time.sleep(DELAI)

except KeyboardInterrupt:
    print("\nArrêt du programme.")