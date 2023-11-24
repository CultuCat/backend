from rest_framework import routers
from . import views
from django.urls import re_path
from .views import PerfilView


router = routers.DefaultRouter()

router.register(r'', PerfilView, 'Perfils')

urlpatterns = [
    *router.urls,
    re_path('login', views.login_perfil),
    re_path('signup', views.signup_perfil),
    re_path(r'^(?P<pk>\d+)/edit/$', PerfilView.as_view({'put': 'update_profile'}), name='update_profile'),
    re_path(r'^(?P<user_id>\d+)/tags_preferits/(?P<tag_id>\w+)/$', views.TagsPreferits.as_view(), name='tags_preferits'),
    re_path(r'^(?P<user_id>\d+)/espais_preferits/(?P<space_id>\w+)/$', views.SpacesPreferits.as_view(), name='espais_preferits'),
    re_path(r'^(?P<user_id>\d+)/send_friend_request/$', PerfilView.as_view({'post': 'send_friend_request'}), name='send_friend_request'),
    re_path(r'^(?P<user_id>\d+)/accept_friend_request/$', PerfilView.as_view({'post': 'accept_friend_request'}), name='accept_friend_request'),
    re_path(r'^(?P<user_id>\d+)/wants_to_talk_perfil/$', PerfilView.as_view({'put': 'wants_to_talk_perfil'}), name='wants_to_talk_perfil'),
    re_path(r'^(?P<user_id>\d+)/is_visible_perfil/$', PerfilView.as_view({'put': 'is_visible_perfil'}), name='is_visible_perfil'),
    re_path(r'^(?P<user_id>\d+)/block_profile/$', PerfilView.as_view({'put': 'block_profile'}), name='block_profile'),

]