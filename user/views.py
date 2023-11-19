from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from user.serializers import PerfilSerializer
from user.models import Perfil
from tags.models import Tag

import time

class PerfilView(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

    @action(methods=['GET', 'PUT'], detail=False)
    def profile(self, request):

        if self.request.auth is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': "El token d'autentificació no ha sigut donat."})

        user = Token.objects.get(key=self.request.auth.key).user

        if request.method == 'PUT':
            newImage = request.data.get('imatge', None)
            newBio = request.data.get('bio', None)

            if newImage is not None:
                user.perfil.imatge = newImage
            if newBio is not None:
                user.perfil.bio = newBio
            start_time = time.time()
            user.save()
            user.perfil.save()
            end_time = time.time()
            elapsed_time = end_time - start_time

            if elapsed_time > 2:
                print(f"La consulta tomó más de 2 segundos: {elapsed_time} segundos")
            else:
                print(f"La consulta tomó {elapsed_time} segundos")

        serializer = PerfilSerializer(user.perfil)
        return Response(status=status.HTTP_200_OK, data={*serializer.data, *{'message': "S'ha actualitzat el perfil"}})
    
@api_view(['POST'])
def signup_perfil(request):
    serializer = PerfilSerializer(data=request.data)
    email = request.data.get('email')
    if Perfil.objects.filter(email=email).exists():
        return Response({'email: This email is already used'}, status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():

        serializer.save()
        user = Perfil.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        start_time = time.time()
        user.save()
        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time > 2:
            print(f"La consulta tomó más de 2 segundos: {elapsed_time} segundos")
        else:
            print(f"La consulta tomó {elapsed_time} segundos")
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_perfil(request):
    start_time = time.time()
    user = get_object_or_404(Perfil, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"L'usuari o el password no són correctes"}, status=status.HTTP_404_NOT_FOUND)
    start_time = time.time()
    token, _ = Token.objects.get_or_create(user=user)
    end_time = time.time()
    elapsed_time = end_time - start_time

    if elapsed_time > 2:
        print(f"La consulta tomó más de 2 segundos: {elapsed_time} segundos")
    else:
        print(f"La consulta tomó {elapsed_time} segundos")
    serializer = PerfilSerializer(instance=user)
    return Response({'token': token.key, 'user': serializer.data})

class TagsPreferits(APIView):
    def delete(self, request, user_id, tag_name):
        try:
            user = Perfil.objects.get(id=user_id)
            tag = Tag.objects.get(nom=tag_name)

            start_time = time.time()
            user.tags_preferits.remove(tag)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if elapsed_time > 2:
                print(f"La consulta tomó más de 2 segundos: {elapsed_time} segundos")
            else:
                print(f"La consulta tomó {elapsed_time} segundos")
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Perfil.DoesNotExist:
            return Response({"error": f"El usuario {user.username} no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Tag.DoesNotExist:
            return Response({"error": f"El tag con ID {tag_name} no existe"}, status=status.HTTP_404_NOT_FOUND)