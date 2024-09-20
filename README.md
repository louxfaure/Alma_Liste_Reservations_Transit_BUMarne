# Alma liste des exemplaires en Transit vers la BU Marne pour Alimentaion des casiers NEDAP
Ce script produit un fichier CSV utile à l'alimentaion des casiers "Connectés NEDAP".
Le fichier CSV produit la liste tous les documents ayant une résevation active et en transit pour Marne.\
Le script tourne pour l'environnement Alma **33PUDB_UB** et utilise la clef d'API nommé **33PUDB_UB_Alma_Liste_Pour_Alimentation_Casiers_NEDAP**
## Récupération de la liste des documents en transit Alma/AlmaSet.py
On récupère les resultats de l'ensemble logique "TEST_Liste_Transit_Pour_Alimentation_Casiers" (ID 7372627370004672). La requête construite à partir de la recherche Alma liste tous les exemplaires appartenant aux bibliothèques du **périmètre Campus Marne** ayant un statut **en transit**.

## Identifiaction des documents avec une résevation en transit pour la  BU Marne AlmaRequests.py repere_transit_pour_marne() 
Pour chaque exemplaires le script appelle le web **service get requests**. Si il y a une demande associée à l'exemplaire et que celle-ci est une demande de réservation (request_sub-type ='PATRON_PHYSICAL'), que l'étape de traitement est le transit ('Transit Item') et que la bibliothèque de retrait est la BU MARNE, le script récupère le titre et le code de l'exemplaire.\
Il va ensuite utiliser l'API get user (AlmaUser.py) pour récupérer le code barres et le nom de l'utilisateur sur la base de l'identifiant principal de ce dernier.
> [!IMPORTANT]  
> Si l'utilisateur n'a pas de code-barres sa réservation est ignorée

## Mise en forme du fichier et dépôt sur le serveur sftp