from users.models import EmailRegisterData
from users.serializers.email import EmailSerializer, ConfirmEmailSerializer
from users.utils.email import send_confirmation_email, random_code
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions


class EmailConfirmView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ConfirmEmailSerializer

    @swagger_auto_schema(request_body=ConfirmEmailSerializer, tags=['accounts'])
    def post(self, request):
        serializer = ConfirmEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        code = serializer.data['code']
        EmailRegisterData.objects.filter(is_used=False, email=email, code=code).update(is_used=True)
        return Response({'status': "ok", 'email': email}, 201)


class EmailConfirmationView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EmailSerializer

    @swagger_auto_schema(request_body=EmailSerializer, tags=['accounts'])
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = random_code()
        serializer.save(code=code)
        send_confirmation_email(request=request, email=request.data['email'], code=code)
        return Response(serializer.data, 201)
