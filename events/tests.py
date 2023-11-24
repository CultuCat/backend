from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Event
from spaces.models import Space
from tags.models import Tag
from user.models import Perfil
from .views import EventView
from rest_framework.authtoken.models import Token

class EventViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = Perfil.objects.create(id=1, username='test_user', is_active=True, is_staff=True, is_superuser=True)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.tag1 = Tag.objects.create(nom='Tag1')
        self.tag2 = Tag.objects.create(nom='Tag2')
        self.tag3 = Tag.objects.create(nom='Tag3')

        self.event1 = Event.objects.create(
            id = 20231022001,
            dataIni='2023-10-22T10:00:00Z',
            dataFi='2023-10-22T14:00:00Z',
            nom='Evento 1',
            descripcio='Descripción del evento de prueba',
            preu='Gratis',
            horaris='10:00 AM - 2:00 PM',
            enllac='https://ejemplo.com',
            adreca='Dirección del evento',
            imatge='https://imagen.com/imagen.jpg',
            latitud=40.7128,
            longitud=-74.0060,
            espai=Space.objects.create(nom='Espacio de Prueba', latitud=40.7128, longitud=-74.0060)
        )

        self.event1.tags.add(self.tag1, self.tag2)

        self.event2 = Event.objects.create(
            id = 20231022002,
            dataIni='2023-10-23T11:00:00Z',
            dataFi='2023-10-23T15:00:00Z',
            nom='Evento 2',
            latitud=40.7128,
            longitud=-74.0060,
            espai=self.event1.espai
        )
        self.event2.tags.add(self.tag2, self.tag3)   

        self.event3 = Event.objects.create(
            id = 20231022003,
            dataIni='2023-10-24T12:00:00Z',
            dataFi='2023-10-24T16:00:00Z',
            nom='Evento 3',
            latitud=35.6895,
            longitud=139.6917,
            espai=Space.objects.create(nom='Otro Espacio', latitud=35.6895, longitud=139.6917)
        )
        self.event3.tags.add(self.tag1, self.tag2)

    def test_create_event(self):
        EventView.apply_permissions = False
        data = {
            'dataIni': '2023-10-25T10:00:00Z',
            'dataFi': '2023-10-25T14:00:00Z',
            'nom': 'Evento de Prueba',
            'descripcio': 'Descripción del evento de prueba',
            'preu': 'Gratis',
            'horaris': '10:00 AM - 2:00 PM',
            'enllac': 'https://ejemplo.com',
            'adreca': 'Dirección del evento',
            'imatge': 'https://imagen.com/imagen.jpg',
            'latitud': 41.7128,
            'longitud': -74.1060,
            'espai': 'Espacio de Prueba 2',
            'tags': ['tag4', 'tag5']
        }
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        response = self.client.post('/events/', data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 4)
        self.assertEqual(Space.objects.count(), 3)
        self.assertEqual(Tag.objects.count(), 5)

    def test_create_event_espai_existent(self):
        EventView.apply_permissions = False
        data = {
            'dataIni': '2023-10-26T10:00:00Z',
            'dataFi': '2023-10-26T14:00:00Z',
            'nom': 'Evento de Prueba',
            'descripcio': 'Descripción del evento de prueba',
            'preu': 'Gratis',
            'horaris': '10:00 AM - 2:00 PM',
            'enllac': 'https://ejemplo.com',
            'adreca': 'Dirección del evento',
            'imatge': 'https://imagen.com/imagen.jpg',
            'latitud': 41.7128,
            'longitud': -74.1060,
            'espai': 'Espacio de Prueba',
            'tags': ['tag4', 'tag5']
        }
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        response = self.client.post('/events/', data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 4)
        self.assertEqual(Space.objects.count(), 2)
        self.assertEqual(Tag.objects.count(), 5)

    def tearDown(self):
        EventView.apply_permissions = True
    
    def test_list_events(self):
        response = self.client.get('/events/?ordering=-dataIni')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_events_by_espai(self):
        espai_id = self.event1.espai.id
        response = self.client.get(f'/events/?espai={espai_id}')

        self.assertEqual(response.status_code, 200)
        events = response.data['results']
        self.assertTrue(events)

        event_in_response = next((event for event in events if event['id'] == self.event3.id), None)
        self.assertIsNone(event_in_response) 
    
    def test_get_specific_event(self):
        response = self.client.get(f'/events/{self.event1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['nom'], self.event1.nom)
        self.assertEqual(response.data['descripcio'], self.event1.descripcio)
        self.assertEqual(response.data['dataIni'], self.event1.dataIni)
        self.assertEqual(response.data['dataFi'], self.event1.dataFi)
        self.assertEqual(response.data['preu'], self.event1.preu)
        self.assertEqual(response.data['horaris'], self.event1.horaris)
        self.assertEqual(response.data['adreca'], self.event1.adreca)
        self.assertEqual(response.data['latitud'], self.event1.latitud)
        self.assertEqual(response.data['longitud'], self.event1.longitud)
        self.assertEqual(response.data['espai']['nom'], self.event1.espai.nom)