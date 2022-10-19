from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoutineViewSet

router = DefaultRouter()
router.register(r'', RoutineViewSet, basename='routines')

urlpatterns = [
    path('', include(router.urls)),
]