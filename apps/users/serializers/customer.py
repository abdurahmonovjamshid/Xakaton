from rest_framework import serializers
from users.models import Customer, Profile


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('full_name', 'phone_number', 'profile_photo', 'address')

    def get_address(self, obj):
        return obj.get_address()

    
