from django.db import models

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(null=True, unique=True)

    @classmethod
    def get_or_createTag(cls, nom):
        try:
            tag = cls.objects.get(nom=nom)
        except cls.DoesNotExist:
            tag = cls(nom=nom)
            tag.save()
        return tag