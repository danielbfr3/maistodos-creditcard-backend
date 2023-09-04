from datetime import datetime

from creditcards.models import Creditcard
from rest_framework import serializers


class CreditcardSerializer(serializers.ModelSerializer):
    """Serializer for creditcard objects."""

    brand = serializers.CharField(read_only=True)

    class Meta:
        model = Creditcard
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert the date to the format "MM/YYYY"
        year, month, day = instance.exp_date.split("-")
        representation["exp_date"] = datetime(int(year), int(month), int(day)).strftime(
            "%m/%Y"
        )
        # Decrypt the credit card number
        representation["number"] = instance.decrypted_number
        return representation
