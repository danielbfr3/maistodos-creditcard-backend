"""
Tests for the creditcard API.
"""
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_LIST_CREDITCARD_URL = reverse("creditcards:api-root")
CREATE_USER_URL = reverse("users:create")
TOKEN_URL = reverse("users:token")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class CreditCardApiTests(TestCase):
    """Test the creditcard API."""

    def setUp(self):
        """Set up data for tests."""
        self.client = APIClient()

        # Set up valid exp_date
        today = datetime.now()
        self.valid_exp_date = f"{str(today.month).zfill(2)}/{today.year + 2}"

        # Create user
        payload = {
            "email": "testeemail@testeprovider.com",
            "password": "Testeteste1234@",
            "name": "Teste",
        }

        self.user = create_user(**payload)
        response = self.client.post(
            TOKEN_URL,
            {
                "email": payload["email"],
                "password": payload["password"],
            },
        )

        self.token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_create_creditcard_success(self):
        """Test creating a creditcard is successful."""
        payload = {
            "holder": "John Doe",
            "number": "5447732384411540",
            "exp_date": self.valid_exp_date,
            "cvv": "123",
        }
        res = self.client.post(CREATE_LIST_CREDITCARD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["holder"], payload["holder"])
        self.assertEqual(res.data["number"], payload["number"])
        self.assertEqual(res.data["cvv"], payload["cvv"])
        self.assertEqual(res.data["brand"], "master")

        retrieve_url = reverse("creditcards:creditcard-detail", args=[res.data["id"]])
        res = self.client.get(retrieve_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["holder"], payload["holder"])
        self.assertEqual(res.data["number"], payload["number"])
        self.assertEqual(res.data["cvv"], payload["cvv"])
        self.assertEqual(res.data["brand"], "master")

    def test_create_creditcard_invalid_number(self):
        """Test creating a creditcard with invalid number."""
        payload = {
            "holder": "John Doe",
            "number": "1111732384411540",
            "exp_date": self.valid_exp_date,
            "cvv": "123",
        }
        response = self.client.post(CREATE_LIST_CREDITCARD_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["number"][0].code, "invalid")

    def test_create_creditcard_invalid_exp_date(self):
        """Test creating a creditcard with invalid exp_date."""
        payload = {
            "holder": "John Doe",
            "number": "5447732384411540",
            "exp_date": "12/2019",
            "cvv": "123",
        }
        response = self.client.post(CREATE_LIST_CREDITCARD_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["exp_date"][0].code, "invalid")

    def test_create_creditcard_invalid_cvv(self):
        """Test creating a creditcard with invalid cvv."""
        payload = {
            "holder": "John Doe",
            "number": "5447732384411540",
            "exp_date": self.valid_exp_date,
            "cvv": "12",
        }
        response = self.client.post(CREATE_LIST_CREDITCARD_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["cvv"][0].code, "invalid")

    def test_create_creditcard_without_token(self):
        """Test creating a creditcard without token."""
        payload = {
            "holder": "John Doe",
            "number": "5447732384411540",
            "exp_date": "12/2022",
            "cvv": "123",
        }
        self.client.credentials()
        res = self.client.post(CREATE_LIST_CREDITCARD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_creditcard_with_invalid_token(self):
        """Test creating a creditcard with invalid token."""
        payload = {
            "holder": "John Doe",
            "number": "5447732384411540",
            "exp_date": "12/2022",
            "cvv": "123",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "invalid_token")
        res = self.client.post(CREATE_LIST_CREDITCARD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
