# -*- coding: utf-8 -*-

# external imports
import json
import logging
import xml.etree.ElementTree as ET
from math import *
from . import Alma_api_fonctions, AlmaUser


class AlmaRequests(object):
    """ Remonte  les demandes portées sur un exemplaire"""

    def __init__(
        self,
        mms_id,
        holding_id,
        item_id,
        request_type = "HOLD",
        status = "active",
        accept="json",
        apikey="",
        service="",
    ):
        if apikey is None:
            raise Exception("Merci de fournir une clef d'APi")
        self.apikey = apikey
        self.service = service
        self.est_erreur = False
        self.mes_logs = logging.getLogger(service)
        self.appel_api = Alma_api_fonctions.Alma_API(
            apikey=self.apikey, service=self.service
        )
        status, response = self.appel_api.request(
            "GET",
            "https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/{}/holdings/{}/items/{}/requests?request_type={}&status={}".format(mms_id,holding_id,item_id,request_type,status),
            accept=accept,
        )
        # self.response = self.appel_api.extract_content(response)
        if status == "Error":
            self.est_erreur = True
            self.message_erreur = response
        else:
            self.record = self.appel_api.extract_content(response)
            self.mes_logs.debug(json.dumps(self.record,indent=4))


    def nb_de_demandes(self):
        return int(self.record["total_record_count"])

    def repere_transit_pour_marne(self):
        for demande in self.record['user_request'] :
            bib_retrait = demande['pickup_location_library']
            etape_traitement_demande = demande['task_name']
            type_de_demande = demande['request_sub_type']['value']
            # TODO valeur 'Rejected' à supprimer pour le passage en prod
            if bib_retrait =='1602000000' and  etape_traitement_demande == 'Transit Item' and type_de_demande == 'PATRON_PHYSICAL':
                #On récupère le nom et le code barre de l'utilisateur
                user_primary_id = demande['user_primary_id']
                user = AlmaUser.AlmaUser(user_id=user_primary_id,apikey=self.apikey,service=self.service)
                user_name = user.user_name()
                cb_user = user.barcode()
                # Si l'utilisateur n'a pas de CB on envoie pas la résas à l'automate
                if cb_user : 
                        return {    'N° carte' : cb_user,
                                    'Code barres' : demande['barcode'],
                                    'Adhérent' : user_name,
                                    'Titre' : demande['title']
                        }
