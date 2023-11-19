from rest_framework import generics, viewsets, status
from .models import Event
from spaces.models import Space
from tags.models import Tag
from .serializers import EventSerializer, EventListSerializer, EventCreateSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.permissions import IsAdmin
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import time

class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    models = Event
    pagination_class = PageNumberPagination
    pagination_class.page_size = 50
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    ordering_fields = ['dataIni']

    filterset_fields = ['espai']

    apply_permissions = False

    def get_permissions(self):
        if self.action == 'create' and self.apply_permissions:
            return [IsAdmin()]
        else:
            return []

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action == 'create':    
            return EventCreateSerializer
        return EventSerializer
    
    def list(self, *args, **kwargs):
        start_time = time.time()
        resultado = super().list(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time > 2:
            print(f"La consulta tomó más de 2 segundos: {elapsed_time} segundos")
        else:
            print(f"La consulta tomó {elapsed_time} segundos")

        return resultado

    def create(self, request, *args, **kwargs):
        event = request.data.copy()

        # Per asegurar-se que l'id no es repeteix, agafarem el mes antic i li restarem 1
        last_event = Event.objects.all().order_by('id').first()
        if last_event:
            id = last_event.id - 1
        else:
            id = 99999999999
        event['id'] = id
        Space.get_or_createSpace(nom = event['espai'], latitud = event['latitud'], longitud = event['longitud'])
        
        tags_data = event.get('tags')
        
        if tags_data:
            for tag_name in tags_data:
                Tag.get_or_createTag(nom=tag_name)

        event['isAdminCreated'] = True

        serializer = self.get_serializer(data=event)
        serializer.is_valid(raise_exception=True)

        start_time = time.time()
        self.perform_create(serializer)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time > 2:
            print(f"La consulta tomó más de 2 segundos: {elapsed_time} segundos")
        else:
            print(f"La consulta tomó {elapsed_time} segundos")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
