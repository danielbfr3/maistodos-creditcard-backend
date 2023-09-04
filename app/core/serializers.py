from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        credentials = {"email": "", "password": attrs.get("password")}

        email = attrs.get("email")

        if email:
            credentials["email"] = email
        else:
            raise ValidationError("Email field may not be blank")

        return super().validate(credentials)
