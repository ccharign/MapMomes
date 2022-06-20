from django.db import models, transaction

# Modèles issus de l’appli dijk
from dijk.models import Ville


def dico_nettoyé(d:dict, champs_à_garder:list, champs_obligatoires:list, conversions:dict):
    """
    Entrée:
        conversions ((str -> fonction) dict), dico champ -> fonction à appliquer
    - AssertionError s’il manque un champ obligatoire.
    - Les autres champs manquant seront complétés avec None.
    """
    
    assert all(c in d for c in champs_obligatoires), f"Il manque un champ dans {d} :{[c for c in champs_obligatoires if c not in d]}"

    d_nettoyé = {
        c: conversions.get(c, lambda x:x)( d.get(c, None)) for c in champs_à_garder
    }
    return d_nettoyé



@transaction.atomic()
def ajoute_des_many_to_many(table, ds_rel):
    """
    table (class) : la table d’association (genre Truc.machin.through)
    ds_rel (dic list) : liste de dictionnaires (nom du champ, valeur). Typequement {truc_id: pk de truc, machin_id : pk de machin}.
    """
    for d in ds_rel:
        rel = table(**d)
        rel.save()
    
    
class TypeLieu(models.Model):
    nom = models.TextField()
    description = models.TextField(null=True, blank=True, default=None)
    def __str__(self):
        return self.nom

    
class Équipement(models.Model):
    nom = models.TextField()
    description = models.TextField(null=True, blank=True, default=None)
    def __str__(self):
        return self.nom

    
class Lieu(models.Model):
    """
    Un lieu précis

    lien_officiel : lien vers le site du lieu.
    texte_autres_liens (text): liens séparés par des |
    """
    nom = models.TextField()
    adresse = models.TextField()
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    lon = models.FloatField()
    lat = models.FloatField()
    lien_officiel = models.URLField(default=None, blank=True, null=True)
    texte_autres_liens = models.TextField(default=None, blank=True, null=True)
    typeLieu = models.ManyToManyField(TypeLieu)
    équipement = models.ManyToManyField(Équipement)

    def __str__(self):
        return self.nom
    
    def coords(self):
        return self.lon, self.lat

    def __lt__(self, autre):
        return True

    def autres_liens(self):
        return self.texte_autres_liens.split("|")

    @classmethod
    def of_dico(cls, d):
        """
        Entrée : d, contient éventuellement trop de champs.
        Liste des champs:
            "nom",
            "adresse",
            "ville" (instance de dijk.models.Ville),
            "lon",
            "lat",
            "lien_officiel",
            "autres_liens" (liste),
            "typesLieux" (liste),
            "équipement" (liste)
        """
        
        champs_à_garder=[
            "nom",
            "adresse",
            "ville",
            "lon",
            "lat",
            "lien_officiel",
            "autres_liens",
            "typesLieux",
            "équipements"
        ]

        champs_obligatoires=[
            "nom",
            "adresse",
            "ville",
            "lon",
            "lat"
        ]

        conversions= {
            "lon": float,
            "lat": float,
            
        }

        d_nettoyé=dico_nettoyé(d, champs_à_garder, champs_obligatoires, conversions)

        autres_liens = d_nettoyé.pop("autres_liens")
        if autres_liens:
            d_nettoyé["texte_autres_liens"]=";".join(autres_liens)
        
        types_lieux = d_nettoyé.pop("typesLieux")
        équipements = d_nettoyé.pop("équipements")
        res = cls(**d_nettoyé)
        res.save() # ajout d’un many to many possible uniquement si objet sauvé (sinon il n’a pas encore de pk)

        ## Les many to many
        ## Types de lieux
        à_créer = []
        for t in types_lieux:
            try:
                t_d = TypeLieu.objects.get(nom=t)
                à_créer.append({"lieu_id":res.pk, "typelieu_id": t_d.pk})
            except Exception as e:
                raise ValueError(f"type de lieu pas trouvé : {t}. Erreur : {e}")
        ajoute_des_many_to_many(Lieu.typeLieu.through, à_créer )
        
        ## Équipements
        à_créer = []
        for é in équipements:
            try:
                é_d = Équipement.objects.get(nom=é)
                à_créer.append({"lieu_id":res.pk, "équipement_id": é_d.pk})
            except Exception as e:
                raise ValueError(f"Équipement pas trouvé : {é}. Erreur : {e}")
        ajoute_des_many_to_many(Lieu.équipement.through, à_créer )
            
        res.save()
        return res
