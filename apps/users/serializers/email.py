from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import EmailRegisterData


class ConfirmEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128, required=True)
    code = serializers.IntegerField(required=True)

    def validate(self, attrs):
        email_ = str(attrs['email']).lower()
        code = attrs['code']
        if EmailRegisterData.objects.filter(is_used=False, email=email_, code=code).exists():
            attrs['email'] = email_
        return attrs


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailRegisterData
        fields = ('email',)

    def validate(self, email):
        email_ = str(email['email']).lower()
        if EmailRegisterData.objects.filter(is_used=True, email=email_).exists():
            raise ValidationError(_("This user already exists"))
        EmailRegisterData.objects.filter(is_used=False, email=email_).delete()
        email['email'] = email_
        return email
