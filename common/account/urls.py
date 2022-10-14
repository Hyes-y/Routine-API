from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from django.urls import path
from .views import SignUpView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('login/verify/', TokenVerifyView.as_view()),
    path('signup/', SignUpView.as_view()),
]