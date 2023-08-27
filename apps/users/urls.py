from django.urls import path

from users.views.confirmation_email import EmailConfirmationView, EmailConfirmView
from users.views.sign_up import CustomerCreateAPIView, ProfileAPIView
from users.views.sign_in import SignInView
from users.views.token import TokenView

urlpatterns = [
    path('seller/registration', CustomerCreateAPIView.as_view(), name='sign-up'),
    path('login', SignInView.as_view(), name='sign-in'),
    path('me', ProfileAPIView.as_view(), name='sign-in'),
    path('refresh/', TokenView.as_view(), name='token'),
    # path('send-confirmation-code/', EmailConfirmationView.as_view(), name='send-confirmation-code'),
    # path('confirm-email/', EmailConfirmView.as_view(), name='confirm-email'),
]
