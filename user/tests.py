from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Perfil, FriendshipRequest
from spaces.models import Space
from tags.models import Tag
from rest_framework.authtoken.models import Token


class TestUsers(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        
        self.user = Perfil.objects.create(id=1,username='test_user', is_active=True, puntuacio=1)
        self.user2 = Perfil.objects.create(id=2,username='test_user2', is_active=True, puntuacio=2)
        self.user3 = Perfil.objects.create(id=3,username='test_user3', is_active=True, puntuacio=3)
        self.admin = Perfil.objects.create(id=4, username='test_admin', is_active=True, is_staff=True)
        self.space = Space.objects.create(id=1, nom="Bcn", latitud=3.3, longitud=3.3)
        self.space2 = Space.objects.create(id=2, nom="Bdn", latitud=3.2, longitud=3.2)
        self.tag1 = Tag.objects.create(id=1, nom="tag1")
        self.tag2 = Tag.objects.create(id=2, nom="tag2")
        self.user.tags_preferits.set([self.tag1, self.tag2])
        self.user.espais_preferits.set([self.space, self.space2])

    def test_creations_self(self):
        self.assertEqual(Space.objects.count(), 2)
        self.assertEqual(Perfil.objects.count(), 4)
        self.assertEqual(Tag.objects.count(), 2) 

    def test_delete_espai_preferit(self):
        response = self.client.delete("/users/1/espais_preferits/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user.espais_preferits.count(), 1)

    def test_delete_tag_preferit(self):
        response = self.client.delete("/users/1/tags_preferits/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user.tags_preferits.count(), 1)
    
    def test_send_and_accept_request(self):
        data = {
            'to_user': 3
        }
        response = self.client.post("/users/1/send_friend_request/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendshipRequest.objects.count(), 1)

        data = {
            'id': 1,
            'is_accepted': True
        }
        response = self.client.post("/users/1/accept_friend_request/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=3, from_user=1).first().is_answered, True)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=3, from_user=1).first().is_accepted, True)

    def test_send_and_decline_request(self):
        data = {
            'to_user': 2
        }
        response = self.client.post("/users/1/send_friend_request/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendshipRequest.objects.count(), 1)

        data = {
            'id': 2,
            'is_accepted': False
        }
        response = self.client.post("/users/1/accept_friend_request/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=2, from_user=1).first().is_answered, True)
        self.assertEqual(FriendshipRequest.objects.filter(to_user=2, from_user=1).first().is_accepted, False)

    ##Tests privacitat users
    def test_wants_to_talk_true(self):
        data = {
            'wantsToTalk': True
        }
        response = self.client.put("/users/1/wants_to_talk_perfil/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db() 
        self.assertTrue(self.user.wantsToTalk)
    
    def test_wants_to_talk_false(self):
        data = {
            'wantsToTalk': False
        }
        response = self.client.put("/users/1/wants_to_talk_perfil/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db() 
        self.assertFalse(self.user.wantsToTalk)

    def test_is_visible_true(self):
        data = {
            'isVisible': True
        }
        response = self.client.put("/users/1/is_visible_perfil/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db() 
        self.assertTrue(self.user.isVisible)

    def test_is_visible_false(self):
        data = {
            'isVisible': False
        }
        response = self.client.put("/users/1/is_visible_perfil/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db() 
        self.assertFalse(self.user.isVisible)

    ##Tests permisos
    def test_is_perfil(self):
        response = self.client.get("/users/1/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user.is_staff)

    def test_is_admin(self):
        response = self.client.get("/users/4/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.admin.is_staff)

    ##Test ranking punts
    def test_ranking_punts(self):
        response = self.client.get("/users/?ordering=-puntuacio", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        users = response.data
        self.assertEqual(users[0]['id'], self.user3.id) #user3 té la puntuacio més alta
        self.assertEqual(users[1]['id'], self.user2.id) #user2 la segona
        self.assertEqual(users[2]['id'], self.user.id)  #user1 la més baixa

    ##Tests get user by username
    def test_get_user_by_username(self):
        response = self.client.get("/users/?username=test_user", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
    
    ##Tests bloquejar user
    def test_block_as_admin_true(self):
        admin_token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
        data = {
            'isBlocked': True
        }
        response = self.client.put("/users/1/block_profile/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db() 
        self.assertTrue(self.user.isBlocked)

    def test_block_as_admin_false(self):
        admin_token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
        data = {
            'isBlocked': False
        }
        response = self.client.put("/users/1/block_profile/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db() 
        self.assertFalse(self.user.isBlocked)

    def test_block_as_perfil_true(self):
        user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
        data = {
            'isBlocked': True
        }
        response = self.client.put("/users/2/block_profile/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.user2.refresh_from_db() 
        self.assertFalse(self.user2.isBlocked)

    def test_block_as_perfil_false(self):
        user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
        data = {
            'isBlocked': False
        }
        response = self.client.put("/users/2/block_profile/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.user2.refresh_from_db() 
        self.assertFalse(self.user2.isBlocked)




    #tests edit perfil i get

