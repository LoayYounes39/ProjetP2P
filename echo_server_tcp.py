#!/usr/bin/env python3
import socket
import os
import shutil

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serveur:
    # Un seul serveur TCP écoute sur le port 65432
    serveur.bind(("", 65432))
    serveur.listen()
    while True:
        client, adresse = serveur.accept()
        with client:
            # Attends du Client Commande = Download <chemin_du_fichier>
            commande = client.recv(1024).decode().strip()
            if commande.startswith("Download "):
                # Récupération du chemin de la commande
                chemin = commande.split(" ", 1)[1]
                if os.path.isfile(chemin):
                    # Récupération du nom du fichier depuis le chemin
                    nom = os.path.basename(chemin)
                    os.makedirs("./public-html", exist_ok=True)
                    # Copie du fichier dans le dossier public-html
                    shutil.copy(chemin, f"./public-html/{nom}")
                    lien = f"http://localhost:8080/{nom}"
                    # Envoie du lien au client
                    client.sendall(lien.encode())
                else:
                    client.sendall(b"Erreur : fichier introuvable")