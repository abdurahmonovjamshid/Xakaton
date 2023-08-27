from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from users.models import Token, User
from users.serializers.token import UserTokenSerializer
from django.utils.translation import gettext_lazy as _


class TokenView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserTokenSerializer

    @swagger_auto_schema(request_body=UserTokenSerializer, tags=['accounts'])
    def post(self, request):
        refresh = request.data['refresh']
        token = Token.objects.filter(refresh=refresh).first()
        if token:
            token.delete()
            token = Token.objects.create(user=User.objects.get(id=token.user.id))
            return Response({
                "access": token.access,
                "refresh": token.refresh,
            }, 201)

        return Response({"error": _("Invalid token!")}, 401)
