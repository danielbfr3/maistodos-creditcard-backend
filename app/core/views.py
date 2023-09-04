from core.serializers import EmailTokenObtainPairSerializer
from drf_spectacular.views import SpectacularAPIView
from rest_framework_simplejwt.views import TokenObtainPairView


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class CustomSpectacularAPIView(SpectacularAPIView):
    permission_classes = ()
