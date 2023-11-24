from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Ticket
from .serializers import TicketSerializer, TicketSerializer_byEvent, TicketSerializer_byUser
from discount.models import Discount
from user.permissions import IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend
from events.models import Event
from user.models import Perfil
from rest_framework.authentication import TokenAuthentication


from utility.new_discount_utils import verificar_y_otorgar_descuento

import time

class TicketsView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'user']
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        else:
            return []
        
    def get_serializer_class(self):
        user_param = self.request.query_params.get('user', None)
        event_param = self.request.query_params.get('event', None)

        # Determinar el serializer basado en la solicitud
        if user_param is not None and event_param is None:
            return TicketSerializer_byUser
        elif event_param is not None and user_param is None:
            return TicketSerializer_byEvent
        else:
            return TicketSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
    
        ticket = {
            'user': request.user.id,
            'event': request.data.get('event')
        }
        serializer = self.get_serializer(data=ticket)
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
        
        event = Event.objects.get(id=ticket['event'])

        event_tags = event.tags.all()
        event_espai = event.espai

        user = Perfil.objects.get(id=ticket['user'])  
        user.tags_preferits.add(*event_tags)
        user.espais_preferits.add(event_espai)


        #si se usa un descuento se marca como usado
        if request.data.get('discount') is not None:
            descuento = Discount.objects.get(codi=request.data.get('discount')) #si ja dejado hacer el post de entrada es porq ya se ha comprobado q el descuento existe y es válido
            # Cambia el valor de bool a True
            descuento.usat = True

            start_time = time.time()
            descuento.save()
            end_time = time.time()
            elapsed_time = end_time - start_time

            if elapsed_time > 2:
                print(f"La consulta tomó más de 2 segundos: {elapsed_time} segundos")
            else:
                print(f"La consulta tomó {elapsed_time} segundos")
            
        verificar_y_otorgar_descuento(ticket['user'], "Més esdeveniments", Ticket.objects.filter(user= ticket['user']).count())  
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
   
    
