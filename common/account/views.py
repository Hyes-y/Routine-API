from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import SignUpSerializer


class SignUpView(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
