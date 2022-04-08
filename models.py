from django.db import models




class Ville(models.Model):
    nom_complet = models.CharField(max_length=100)
    nom_norm = models.CharField(max_length=100)
    code = models.IntegerField(null=True)
    code_insee = models.IntegerField()
    données_présentes = models.BooleanField(default=False)

    def __str__(self):
        return self.nom_complet

    def avec_code(self):
        return f"{self.code} {self.nom_complet}"

    
class TypeLieu(models.Model):
    nom = models.TextField()

    
class Équipement(models.Model):
    nom = models.TextField()

    
class Lieu(models.Model):
    nom = models.TextField()
    adresse = models.TextField()
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    typeLieu = models.ManyToManyField(TypeLieu)
    équipement = models.ManyToManyField(Équipement)
    lon = models.FloatField()
    lat = models.FloatField()

    def coords(self):
        return self.lon, self.lat
