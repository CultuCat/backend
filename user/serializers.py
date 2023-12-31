from rest_framework import serializers
from .models import Perfil, FriendshipRequest,  TagPreferit, SpacePreferit
from discount.models import Discount

class PerfilShortSerializer(serializers.ModelSerializer):
    imatge = serializers.SerializerMethodField()
    class Meta:
        model = Perfil
        fields = ('id', 'username', 'first_name', 'imatge', 'puntuacio', 'isBlocked', 'wantsToTalk', 'isVisible')

    def get_imatge(self, obj):
        return obj.get_imatge()
        
class FriendshipRequestSerializer(serializers.ModelSerializer):
    from_user = PerfilShortSerializer(source='from_user.perfil', read_only=True)
    to_user = PerfilShortSerializer(source='to_user.perfil', read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = ('id', 'from_user', 'to_user', 'is_answered', 'is_accepted', 'timestamp')

class FriendshipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = ('id', 'to_user')

class FriendshipAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = ('id', 'is_accepted')

class PerfilSerializer(serializers.ModelSerializer):
    espais_preferits = serializers.SerializerMethodField()
    tags_preferits = serializers.SerializerMethodField()
    pending_friend_requests = serializers.SerializerMethodField()
    pending_friend_requests_sent = serializers.SerializerMethodField()
    friends = serializers.SerializerMethodField()
    imatge = serializers.SerializerMethodField()

    def get_pending_friend_requests(self, obj):
        pending_requests = obj.get_pending_friend_requests()
        serializer = FriendshipRequestSerializer(pending_requests, many=True)
        return serializer.data
    
    def get_pending_friend_requests_sent(self, obj):
        pending_requests = obj.get_pending_friend_requests_sent()
        serializer = FriendshipRequestSerializer(pending_requests, many=True)
        return serializer.data

    def get_friends(self, obj):
        sent_requests = FriendshipRequest.objects.filter(from_user=obj, is_answered=True, is_accepted=True)
        received_requests = FriendshipRequest.objects.filter(to_user=obj, is_answered=True, is_accepted=True)

        friends = []

        for request in sent_requests:
            friends.append(request.to_user)

        for request in received_requests:
            friends.append(request.from_user)

        serializer = PerfilShortSerializer(friends, many=True)
        return serializer.data
    
    def get_espais_preferits(self, obj):
        return obj.get_espais_preferits()

    def get_tags_preferits(self, obj):
        return obj.get_tags_preferits()
    
    def get_imatge(self, obj):
        return obj.get_imatge()
    
    class Meta(object):
        model = Perfil
        fields = ('id', 'username','email', 'first_name','is_staff','imatge', 'bio', 'puntuacio', 'isBlocked', 'wantsToTalk', 'wantsNotifications', 'isVisible', 'isGoogleUser', 'language', 'tags_preferits', 'espais_preferits', 'pending_friend_requests', 'pending_friend_requests_sent', 'friends')

class PerfilCreateSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Perfil
        fields = ('id', 'username', 'password', 'usernameGoogle', 'email', 'first_name', 'isGoogleUser', 'imatge_url')