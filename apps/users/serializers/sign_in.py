from rest_framework import serializers

from users.models import User


class UserSignInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, trim_whitespace=True)
    password = serializers.CharField(required=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = ('username', 'password')
