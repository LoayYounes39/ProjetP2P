
#!/usr/bin/env python3

import socket
import urllib.request
import os

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 65432))

    while True:
        #Envoi de la commande au serveur
        commande = input("Commande (FIN pour quitter) : ")
        if commande == "FIN":
            break
        s.sendall(commande.encode('utf-8'))
        # Récupération du lien envoyé après traitement sur la commande par le serveur
        lien = s.recv(1024).decode('utf-8')
        print("Reçu du serveur :", lien)

        if lien.startswith("http://"):
            os.makedirs("./fichiers_recus", exist_ok=True)
            fichier = os.path.basename(lien)
            # le client doit recevoir le nom du fichier dans l'URL, pas son chemin source complet.
            urllib.request.urlretrieve(
                lien, os.path.join("./fichiers_recus", fichier)
            )
            print("Fichier téléchargé :", fichier)
