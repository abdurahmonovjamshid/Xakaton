from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from users.models import Token
from users.serializers.sign_in import UserSignInSerializer


class SignInView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSignInSerializer

    @swagger_auto_schema(request_body=UserSignInSerializer, tags=['User'])
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            token = Token.objects.filter(user=user)
            if token.exists():
                token.delete()

            token = Token.objects.create(user=user)
            serializer = UserSignInSerializer(user)
            return Response({
                # "user": serializer.data,
                "access_token": token.access,
                "refresh_token": token.refresh,
            }, 200)
        return Response({"error": _("User not found!")}, 401)
