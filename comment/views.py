from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Comment
from discount.models import Discount
from .serializers import CommentSerializer
from user.permissions import IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication

from utility.new_discount_utils import verificar_y_otorgar_descuento

class CommentsView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event']
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        else:
            return []
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
    
        comment = request.data.copy()
        comment['user'] = request.user.id 
        serializer = self.get_serializer(data=comment)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        verificar_y_otorgar_descuento(comment['user'], "Reviewer", Comment.objects.filter(user= comment['user']).count())  
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
