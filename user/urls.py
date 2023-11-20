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
    re_path('delete', views.delete_perfil),
    re_path(r'^(?P<user_id>\d+)/tags_preferits/(?P<tag_name>\w+)/$', views.TagsPreferits.as_view(), name='tags_preferits'),
]