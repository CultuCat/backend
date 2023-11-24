from django.db import models
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from tags.models import Tag
from spaces.models import Space

class FriendshipRequest(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey('Perfil', related_name='friendship_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey('Perfil', related_name='friendship_requests_received', on_delete=models.CASCADE)
    is_answered = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def accept(self):
        self.is_answered = True
        self.is_accepted = True
        self.save()

    def decline(self):
        self.is_answered = True
        self.save()

class Perfil(User):
    imatge = models.CharField(default='https://www.calfruitos.com/es/fotos/pr_223_20190304145434.png')    
    bio = models.CharField(max_length=200, default="Hey there, I'm using CultuCat", null=True, blank=True, verbose_name=_('Bio'))
    puntuacio = models.IntegerField(null=False, default=0, verbose_name=_('Puntuacio'))
    isBlocked = models.BooleanField(default=False, verbose_name=_('Està bloquejat a la aplicacio'))
    wantsToTalk = models.BooleanField(default=True, verbose_name=_('La resta dels usuaris poden parlar amb ell'))
    isVisible = models.BooleanField(default=True,verbose_name=_('La resta dels usuaris el poden trobar'))

    tags_preferits = models.ManyToManyField(Tag, blank=True, related_name='perfils', verbose_name=("Tags preferits"))
    espais_preferits = models.ManyToManyField(Space, blank=True, related_name='perfils', verbose_name=("Espais preferits"))

    def send_friend_request(self, to_user):
        if not FriendshipRequest.objects.filter(from_user=self, to_user=to_user, is_accepted=True).exists() and \
            not FriendshipRequest.objects.filter(from_user=self, to_user=to_user, is_answered=False).exists() and \
            not FriendshipRequest.objects.filter(from_user=to_user, to_user=self, is_accepted=True).exists() and \
            not FriendshipRequest.objects.filter(from_user=to_user, to_user=self, is_answered=False).exists():
            FriendshipRequest.objects.create(from_user=self, to_user=to_user)
            return True
        return False
            
    def get_pending_friend_requests(self):
            return FriendshipRequest.objects.filter(to_user=self, is_answered=False)
    
    def get_pending_friend_requests_sent(self):
            return FriendshipRequest.objects.filter(from_user=self, is_answered=False)

    def get_friends(self):
            friends = []
            sent_requests = FriendshipRequest.objects.filter(from_user=self, is_answered=True, is_accepted=True)
            received_requests = FriendshipRequest.objects.filter(to_user=self, is_answered=True, is_accepted=True)

            for request in sent_requests:
                friends.append(request.to_user)

            for request in received_requests:
                friends.append(request.from_user)

            return friends
    
    def wants_to_talk_status(self, wants_to_talk):
        if wants_to_talk != self.wantsToTalk:
            self.wantsToTalk = wants_to_talk
            self.save()

    def is_visible_status(self, is_visible):
        if is_visible != self.isVisible:
            self.isVisible = is_visible
            self.save()
    
    @property
    def espais_info(self):
        espais = self.espais_preferits.all()
        if espais:
            return [
                {'id': espai.id, 'nom': espai.nom} for espai in espais
            ]
        return None

    @property
    def tags_info(self):
        tags = self.tags_preferits.all()
        if tags:
            return [
                {'id': tag.id, 'nom': tag.nom} for tag in tags
            ]
        return None