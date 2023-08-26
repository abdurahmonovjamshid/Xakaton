from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import Token


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, access):
        token = Token.objects.filter(access=access, access_expiration__gte=timezone.now()).first()
        if token is None:
            raise AuthenticationFailed({'detail': _('Invalid or expired token.'), 'logout': 'true'})

        if not token.user.is_active:
            raise AuthenticationFailed({'detail': _('User inactive or deleted.'), 'logout': 'true'})

        return token.user, token