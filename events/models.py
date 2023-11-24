from django.db import models
from spaces.models import Space
from tags.models import Tag
from tags.serializers import TagSerializer
from django.utils.translation import gettext_lazy as _

def split_colon(obj):
    if obj:
        return obj.split(',')
    else:
        return None

class Event(models.Model):
    id = models.BigIntegerField(primary_key=True)
    dataIni = models.DateTimeField(null=True, blank=True)
    dataFi = models.DateTimeField(null=True, blank=True)
    nom = models.CharField(null=False, blank=False)
    descripcio = models.TextField(null=True, blank=True)
    preu = models.CharField(null=True, blank=True)
    horaris = models.TextField(null=True, blank=True)
    enllac = models.CharField(null=True, blank=True)
    adreca = models.CharField(null=True, blank=True)
    imatge = models.CharField(null=True, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    espai = models.ForeignKey(Space, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    isAdminCreated = models.BooleanField(null=False, default=False, blank=True)

    def get_enllac(self):
        return split_colon(self.enllac)

    def get_imatge(self):
        imatges = split_colon(self.imatge)
        if imatges:
            enllac_imatges = []
            for imatge in imatges:
                img_split = imatge.split('://')[0]
                if img_split != 'http' and img_split != 'https':
                    enllac_imatges.append('http://agenda.cultura.gencat.cat' + imatge)
                else:
                    enllac_imatges.append(imatge)
            return enllac_imatges
        return imatges

    @property
    def espai_info(self):
        if self.espai:
            return {
                'id': self.espai.id,
                'nom': self.espai.nom
            }
        return None

    @property
    def tags_info(self):
        tags = self.tags.all()
        if tags:
            return [
                {'id': tag.id, 'nom': tag.nom} for tag in tags
            ]
        return None

    @classmethod
    def create_event(cls, event_data):
        espai_nom = event_data.get('espai')
        latitud = event_data['latitud']
        longitud = event_data['longitud']

        espai = Space.get_or_createSpace(nom=espai_nom, latitud=latitud, longitud=longitud)

        event = cls.objects.create(
            id=event_data.get('id'),
            dataIni=event_data.get('dataIni'),
            dataFi=event_data.get('dataFi'),
            nom=event_data.get('nom'),
            descripcio=event_data.get('descripcio'),
            preu=event_data.get('preu'),
            horaris=event_data.get('horaris'),
            enllac=event_data.get('enllac'),
            adreca=event_data.get('adreca'),
            imatge=event_data.get('imatge'),
            latitud=latitud,
            longitud=longitud,
            espai=espai,
            isAdminCreated=True
        )

        tags_data = event_data.get('tags')
        if tags_data:
            for tag_name in tags_data:
                tag = Tag.get_or_createTag(nom=tag_name)
                event.tags.add(tag)

        return event
