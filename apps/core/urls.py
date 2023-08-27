from django.urls import path
from .views.views import RegionListAPIView

urlpatterns = [
    path('regions-with-districts', RegionListAPIView.as_view(), name='region-list'),
]