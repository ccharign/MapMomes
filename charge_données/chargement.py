# -*- coding:utf-8 -*-
from django.db import transaction
import re

import mapmomes.models as mo
from dijk.models import Ville

from mapmomes.progs_python.petites_fonctions import affiche_dico


def csv_vers_dic_list(chemin:str) -> list:
    """
    Entrée : adresse d’un fichier csv dont la première ligne contient le nom des champs
    Sortie : liste des dico (nom du champ -> valeur)
    """
    res=[]
    with open(chemin) as entrée:
        champs = entrée.readline().strip().split(";")
        for ligne in entrée:
            données = ligne.strip().split(";")
            res.append({c:v for c,v in zip(champs, données)})
    return res


#@transaction.atomic() # empêche un many to many après une création
def lieux_csv_vers_bdd(ville, code_postal, chemin="mapmomes/données/Données_Lyon.csv"):

    # Pour les coords dans un lien googleMaps
    e = re.compile(".*@([0-9]*.[0-9]*),([0-9]*.[0-9]*),")

    
    #Recherche de la ville
    essai = Ville.objects.filter(nom_complet=ville)
    if essai:
        v_d = essai.first()
    else:
        # Création de la ville
        v_d = Ville(nom_complet=ville, code=code_postal)
        v_d.save()
    
    données = csv_vers_dic_list(chemin)
    for d in données:
        
        # Récup des coords
        
        if d["Lien Google Maps"]:
            essai = re.findall(e, d["Lien Google Maps"])
            if len(essai)==1:
                d["lon"], d["lat"] = map(float, essai[0])
            else:
                raise ValueError(f"pb dans la regexp pour trouver les coords dans le lien googleMaps : {d}")

        d["autres_liens"] = [d["Lien Google Maps"], d["Lien Apple Plans"]]
        d["ville"] = v_d
        d["typesLieux"] =[tl.strip() for tl in  d.pop("Type de lieu").split(",")]
        d["équipements"] =[tl.strip() for tl in  d.pop("Equipements").split(",")]
        affiche_dico(d)
        lieu = mo.Lieu.of_dico(d)
        print(lieu)
        lieu.save()
        
        
@transaction.atomic()
def équipements_csv_vers_bdd(chemin="mapmomes/données/équipements.csv"):
    with open(chemin) as entrée:
        for ligne in entrée:
            print(ligne)
            nom_éq = ligne.strip()
            éq_d = mo.Équipement(nom=nom_éq)
            éq_d.save()


@transaction.atomic()
def types_lieux_csv_vers_bdd(chemin="mapmomes/données/lieux.csv"):
    with open(chemin) as entrée:
        for ligne in entrée:
            nom_l = ligne.strip()
            t_d = mo.TypeLieu(nom=nom_l)
            t_d.save()
