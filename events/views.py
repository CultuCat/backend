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
from user.permissions import IsAdmin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    models = Event
    permission_classes = [IsAuthenticatedOrReadOnly] 
    authentication_classes = [TokenAuthentication]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 50
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    ordering_fields = ['dataIni']
    filterset_fields = ['espai']

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.query_params.get('ordering'):
            queryset = queryset.order_by('dataIni')
        return queryset

    def get_permission_classes(self):
        if self.action == 'create':
            return [IsAdmin()]
        else:
            return [IsAuthenticatedOrReadOnly()]

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
        if not request.user.is_staff or not request.user.is_superuser:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        event_data = request.data.copy()

        # Per asegurar-se que l'id no es repeteix, agafarem el mes antic i li restarem 1
        last_event = Event.objects.all().order_by('id').first()
        if last_event:
            id = last_event.id - 1
        else:
            id = 99999999999
        event_data['id'] = id

        start_time = time.time()
        event = Event.create_event(event_data)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time > 2:
            print(f"La consulta tomó más de 2 segundos: {elapsed_time} segundos")
        else:
            print(f"La consulta tomó {elapsed_time} segundos")

        serializer = self.get_serializer(event)¡

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
