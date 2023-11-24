from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import Perfil
from events.models import Event
from trophy.models import Trophy
from spaces.models import Space
from tags.models import Tag
from .models import Ticket
from .views import TicketsView
from rest_framework.authtoken.models import Token

ruta = '/tickets/'

class TestTicketsPost(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        
        self.user = Perfil.objects.create(id=1,username='test_user', is_active=True)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.user2 = Perfil.objects.create(id=2,username='test_user2', is_active=True)
        self.token2 = Token.objects.create(user=self.user2)
        self.space = Space.objects.create(id=1, nom="Bcn", latitud=3.3, longitud=3.3)
        self.tag1 = Tag.objects.create(id=1, nom="tag1")
        self.tag2 = Tag.objects.create(id=2, nom="tag2")

        self.esdeveniment1 = Event.objects.create(id=1, nom="test_event1", dataIni="2023-11-01 01:00:00+01", espai=self.space, imatge="a")
        self.esdeveniment1.tags.set([self.tag1, self.tag2])
        self.esdeveniment2 = Event.objects.create(id=2, nom="test_event2", dataIni="2024-11-01 01:00:00+01", espai=self.space, imatge="a") #esdeveniment2 es posterior a esdeveniment1
        #creamos ticket para user 1 en evento 2
        self.ticket1 = Ticket.objects.create(
            user = self.user,
            event = self.esdeveniment2
        )
        
        #creamos ticket para user 2 en evento 2
        self.ticket2 = Ticket.objects.create(
            user = self.user2,
            event = self.esdeveniment2
        )
        
        self.trophy = Trophy.objects.create(
            nom = "Més esdeveniments",
            descripcio = "Quants esdeveniments has assist",
            punts_nivell1 = 2,
            punts_nivell2 = 3,
            punts_nivell3 = 5
        )

    def test_creations_self(self):
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Perfil.objects.count(), 2)
        self.assertEqual(Ticket.objects.count(), 2)
        self.assertEqual(Trophy.objects.count(), 1)
        
    def test_post_ticket(self):
        #creamos un ticket para el user 1 en evento 1, deja crear
        data = {
            'event': 1
        }
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        response = self.client.post(ruta, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 3)
        self.assertTrue(self.user.espais_preferits.filter(id=self.space.id).exists())
        self.assertTrue(self.user.tags_preferits.filter(id=self.tag1.id).exists())
        self.assertTrue(self.user.tags_preferits.filter(id=self.tag2.id).exists())
        
        #creamos un ticket para el user 1 en evento 2, no deja crear, ya existe
        data = {
            'event': 2
        }
        response = self.client.post(ruta, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Ticket.objects.count(), 3)
    
    def test_get_specific_ticket(self):
        #hacemos get de ticket1
        response = self.client.get(f'/tickets/?event={self.ticket1.event.id}&user={self.ticket1.user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event'], self.ticket1.event.id) #2 2
        self.assertEqual(response.data[0]['user'], self.ticket1.user.id) #1 2
        
        #hacemos get de ticket2
        response = self.client.get(f'/tickets/?event={self.ticket2.event.id}&user={self.ticket2.user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['event'], self.ticket2.event.id)
        self.assertEqual(response.data[0]['user'], self.ticket2.user.id)
        
    def test_get_tickets_by_user(self):
        self.ticket3 = Ticket.objects.create(
            user = self.user2,
            event = self.esdeveniment1
        )
        response = self.client.get(f'/tickets/?user={self.ticket3.user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['nomEvent'], self.ticket3.event.nom) #primero aparece el que tiene dataIni más peq, es decir el evento1, osea ticket3
        self.assertEqual(response.data[1]['nomEvent'], self.ticket2.event.nom) #1
        
        #hacemos get de ticket2
        response = self.client.get(f'/tickets/?user={self.ticket1.user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nomEvent'], self.ticket1.event.nom)
        
    def test_list_tickets(self):
        response = self.client.get(ruta)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    