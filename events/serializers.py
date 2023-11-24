from rest_framework import serializers
from .models import Event
from ticket.models import Ticket

class EventSerializer(serializers.ModelSerializer):
    espai = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    enllacos_list = serializers.ListField(read_only=True, required=False, source='get_enllac')
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatge')
    assistents = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        exclude = ['enllac', 'imatge']

    def get_espai(self, obj):
        return obj.espai_info

    def get_tags(self, obj):
        return obj.tags_info
    
    def get_assistents(self, obj):
        ts = Ticket.objects.filter(event=obj.id)
        assistents = []
        for t in ts:
            assistents.append(t.user.id)
        return assistents
        

class EventListSerializer(serializers.ModelSerializer):
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatge')
    espai = serializers.SerializerMethodField()
    assistents = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ['id', 'nom', 'descripcio', 'dataIni', 'imatges_list', 'espai', 'preu', 'assistents']

    def get_espai(self, obj):
        return obj.espai_info
    
    def get_assistents(self, obj):
        ts = Ticket.objects.filter(event=obj.id)
        assistents = []
        for t in ts:
            assistents.append(t.user.id)
        return assistents
    
class EventCreateSerializer(serializers.ModelSerializer):
    espai = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatge')
    
    class Meta:
        model = Event
        fields = '__all__'

    def get_espai(self, obj):
        return obj.espai_info

    def get_tags(self, obj):
        return obj.tags_info