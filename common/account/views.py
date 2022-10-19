from django.contrib.auth import get_user_model
from .serializers import SignUpSerializer
from rest_framework import generics


class SignUpView(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
