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


class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'category')

    def get_category(self, obj):
        parent = obj.parent
        if parent:
            return
        return None


class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = PostImage
        fields = ('post', 'image',)


class PostSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(
        max_length=1000000, allow_empty_file=False, use_url=False), write_only=True, required=True)
    sub_category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(parent__isnull=False))
    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('name', 'sub_category', 'price', 'currency', 'description',
                  'phone_number', 'seller', 'images')

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        post = Post.objects.create(**validated_data)
        for image in images_data:
            PostImage.objects.create(post=post, image=image)
        return post

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update related images if available
        if images_data:
            PostImage.objects.filter(post=instance).delete()
            for image in images_data:
                PostImage.objects.create(post=instance, image=image)
        return instance


class PostListSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()
    extra = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'name', 'slug', 'sub_category', 'photos', 'price', 'currency',
            'published_at', 'description', 'phone_number', 'seller', 'extra'
        )

    def get_sub_category(self, obj):
        return {
            "id": obj.sub_category.id,
            "name": obj.sub_category.name,
            "category": {
                "id": obj.sub_category.parent.id,
                "name": obj.sub_category.parent.name,
                "ads_count": obj.sub_category.parent.get_post_count(),
                "icon": obj.sub_category.parent.icon_url
            }
        }

    def get_photos(self, obj):
        photos = []
        if obj.images:
            # print(obj.images)
            for image in obj.images.all():
                photos.append(image.photo_url)
        return photos

    def get_seller(self, obj):
        return {
            'id': obj.seller.id,
            'full_name': obj.seller.full_name,
            'profile_photo': obj.seller.profile_set.first().profile_photo.url
        }

    def get_extra(self, obj):
        return {
            # You can specify the logic for 'is_mine' field here
            'is_mine': True if obj.seller == self.context['request'].user else False,
            'status': 'active',  # Replace with the actual status value
            'expires_at': '2023-08-27'  # Replace with the actual expiration date
        }
