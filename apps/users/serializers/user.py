from rest_framework import serializers

from users.models import User


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number')
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'read_only': True},
        }
