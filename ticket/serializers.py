from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    imatgeEvent = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = ['user', 'event', 'imatgeEvent', 'image']
        
    def get_imatgeEvent(self, obj):
        imatges = split_colon(obj.event.imatge if obj.event else None)
        if imatges:
            enllac_imatges = []
            for imatge in imatges:
                img_split = imatge.split('://')[0]
                if img_split != 'http' and img_split != 'https':
                    return 'http://agenda.cultura.gencat.cat' + imatge
                else:
                    return imatge
            return enllac_imatges
        return imatges

class TicketSerializer_byEvent(serializers.ModelSerializer):
    idUser = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = ['idUser', 'nickname', 'name', 'avatar']
        
    def get_idUser(self, obj):
        return obj.user.id if obj.user else None
    
    def get_nickname(self, obj):
        return obj.user.username if obj.user else None

    def get_name(self, obj):
        return obj.user.first_name if obj.user else None
    
    def get_avatar(self, obj):
        return obj.user.imatge if obj.user else None
        
def split_colon(obj):
        if obj:
            return obj.split(',')
        else:
            return None
        
class TicketSerializer_byUser(serializers.ModelSerializer):
    nomEvent = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()
    espai = serializers.SerializerMethodField()
    imatge = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = ['id', 'nomEvent', 'data', 'espai', 'imatge']
        
    def get_nomEvent(self, obj):
        return obj.event.nom if obj.event else None

    def get_data(self, obj):
        return obj.event.dataIni if obj.event else None
    
    def get_espai(self, obj):
        return obj.event.espai.nom if obj.event else None
    
    def get_imatge(self, obj):
        imatges = split_colon(obj.event.imatge if obj.event else None)
        if imatges:
            enllac_imatges = []
            for imatge in imatges:
                img_split = imatge.split('://')[0]
                if img_split != 'http' and img_split != 'https':
                    return 'http://agenda.cultura.gencat.cat' + imatge
                else:
                    return imatge
            return enllac_imatges
        return imatges
    