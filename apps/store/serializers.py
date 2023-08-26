from rest_framework import serializers

from .models import Category, Post, PostImage


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'icon', 'children')

    def get_children(self, obj):
        serializer = self.__class__(obj.children.all(), many=True)
        return serializer.data


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, required=False)
    sub_category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(parent__isnull=False))


    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['slug']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        post = Post.objects.create(**validated_data)
        for image_data in images_data:
            PostImage.objects.create(post=post, **image_data)
        return post
    
