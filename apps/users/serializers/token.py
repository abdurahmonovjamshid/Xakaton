from rest_framework import serializers

from users.models import Token


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('access', 'refresh')

        extra_kwargs = {
            'refresh': {'write_only': True},
            'access': {'read_only': True},
        }
