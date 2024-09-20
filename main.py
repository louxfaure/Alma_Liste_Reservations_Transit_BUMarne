#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Modules externes
import os
import logging
import json
import csv
import paramiko

#Modules maison
 
from Services import logs,mail,fonctions
from Services.Alma import AlmaSet
import conf

#################################
# Initialisation des paramètres #
#################################

SERVICE = "Alma_Liste_Reservations_Transit_BUMarne"

LOGS_LEVEL = 'DEBUG'
LOGS_DIR = os.getenv('LOGS_PATH')
# Identifiant du jeux de résultat listant les documents en transi vers Marne
SET_ID = '7372627370004672'
autres_parametres = conf.recupere_parametres()
API_KEY = autres_parametres["clef_api"] 
# Informations de connexion SFTP
serveur_sftp = autres_parametres["serveur_sftp"]
port = 10022
utilsateur_sftp = autres_parametres["utilsateur_sftp"]
fichier_clef_privee = autres_parametres["fichier_clef_privee"]
# Nom du fichier CSV
fichier_csv = 'Sortie/reservations_pour_marne.csv'


#On initialise le logger
logs.setup_logging(name=SERVICE, level=LOGS_LEVEL,log_dir=LOGS_DIR)
mes_logs = logging.getLogger(SERVICE)

mes_logs.info("DEBUT DU TRAITEMENT")



######################################################
# Récupéraion de la liste des exemplaires en transit #
######################################################

mon_set = AlmaSet.AlmaSet(apikey=API_KEY,service=SERVICE,set_id=SET_ID)
data = mon_set.liste_transit_pour_marne
mes_logs.debug(json.dumps(data,indent=4))

##########################
# Création du fichier CSV#
##########################


# Création du fichier CSV
with open(fichier_csv, mode='w', newline='', encoding='utf-8') as file:
    # Extraction des en-têtes depuis les clés du premier dictionnaire
    fieldnames = data[0].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Écriture des en-têtes et des lignes de données
    writer.writeheader()
    writer.writerows(data)

mes_logs.info(f"Fichier {fichier_csv} créé avec succès.")

#################################
# Transfert du fichier via SFTP #
#################################

# Connexion au serveur SFTP
try:
    # Chargement de la clé privée
    key = paramiko.RSAKey.from_private_key_file(fichier_clef_privee)
    transport = paramiko.Transport((serveur_sftp, port))
    transport.connect(username=utilsateur_sftp, pkey=key)

    # Création de l'objet SFTP
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Envoi du fichier
    remote_path = f'/NEDAP_Marne/reservations_pour_marne.csv'  # Chemin distant où envoyer le fichier
    sftp.put(fichier_csv, remote_path)
    print(f"Fichier {fichier_csv} transféré avec succès à {remote_path}.")

    # Fermeture de la connexion SFTP
    sftp.close()
    transport.close()

except Exception as e:
    mes_logs.error(f"Une erreur est survenue : {e}")


mes_logs.info("FIN DU TRAITEMENT")