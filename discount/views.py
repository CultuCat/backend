from rest_framework.response import Response
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Discount
from .serializers import DiscountSerializer
import time

class DiscountsView(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userDiscount']

    def create(self, request, *args, **kwargs):
        discount = request.data.copy()
        discount['userDiscount'] = 1 #request.user #1
        serializer = self.get_serializer(data=discount)
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
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
