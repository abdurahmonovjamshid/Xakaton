from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Profile, User
from users.serializers.customer import CustomerSerializer, ProfileSerializer
from users.serializers.sign_up import UserSignUpSerializer


class CustomerCreateAPIView(APIView):
    @swagger_auto_schema(request_body=CustomerSerializer, tags=['User'])
    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: ProfileSerializer(),
            404: "Profile not found."
        },
        tags=['User']
    )
    def get(self, request, format=None):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile, many=False)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"error": "Profile not found."}, status=404)


# class SignUpView(APIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = UserSignUpSerializer

#     @swagger_auto_schema(request_body=UserSignUpSerializer, tags=['User'])
#     def post(self, request):
#         serializer = UserSignUpSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(password=make_password(request.data['password']))
#         return Response(serializer.data, 201)
