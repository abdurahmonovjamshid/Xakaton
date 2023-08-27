from core.serializers import *
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView


class RegionListAPIView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    @swagger_auto_schema(operation_description="Retrieve a list of regions", tags=['Common'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
