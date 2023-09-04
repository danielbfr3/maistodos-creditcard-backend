from creditcards.models import Creditcard
from creditcards.serializers import CreditcardSerializer
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreditcardListCreateRetrieveView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Manage creditcards in the database."""

    queryset = Creditcard.objects.all()
    serializer_class = CreditcardSerializer
    serializer_create_class = CreditcardSerializer
    pagination_class = None
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
