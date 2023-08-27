from django.urls import path

from store.views.views import CategoryListAPIView, PostCreateAPIView, PostListAPIView

urlpatterns = [
    path('categories-with-childs', CategoryListAPIView.as_view(), name='categories-with-childs'),
    path('ads', PostCreateAPIView.as_view(), name='create ads'),
    path('ads_list', PostListAPIView.as_view(), name='ads list'),
]
