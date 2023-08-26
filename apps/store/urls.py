from django.urls import path

from store.views.views import CategoryListAPIView, PostCreateAPIView

urlpatterns = [
    path('categories-with-childs', CategoryListAPIView.as_view(), name='categories-with-childs'),
    path('ads', PostCreateAPIView.as_view(), name='create ads'),
]
