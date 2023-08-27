from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from store.models import Category, Post

from ..serializers import (CategorySerializer, PostListSerializer,
                           PostSerializer)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(children__isnull=False)
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_description="List categories with children",
        responses={200: CategorySerializer(many=True)},
        tags=['Store']
    )
    def get(self, request, *args, **kwargs):
        """
        Get a list of categories with children.
        """
        return self.list(request, *args, **kwargs)


class PostCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @swagger_auto_schema(
        operation_description="Create Post",
        responses={200: PostSerializer()},
        tags=['Store']
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    @swagger_auto_schema(
        operation_description="Post List",
        responses={200: PostListSerializer()},
        tags=['Store']
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)