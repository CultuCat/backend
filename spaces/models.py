from django.db import models

class Space(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(null=True, unique=True)
    latitud = models.FloatField()
    longitud = models.FloatField()

    @classmethod
    def get_or_createSpace(cls, nom, latitud, longitud):
        try:
            space = cls.objects.get(nom=nom)
        except cls.DoesNotExist:
            space = cls(nom=nom, latitud=latitud, longitud=longitud)
            space.save()
        return space