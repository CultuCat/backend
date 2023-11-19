from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    enllacos_list = serializers.ListField(read_only=True, required=False, source='get_enllac')
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatge')
    class Meta:
        model = Event
        exclude = ['enllac', 'imatge']

class EventListSerializer(serializers.ModelSerializer):
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatge')
    
    class Meta:
        model = Event
        fields = ['id', 'nom', 'descripcio', 'dataIni', 'imatges_list', 'espai', 'preu']

class EventCreateSerializer(serializers.ModelSerializer):
    imatges_list = serializers.ListField(read_only=True, required=False, source='get_imatge')
    
    class Meta:
        model = Event
        fields = '__all__'