from datetime import datetime

from creditcards.models import Creditcard
from creditcards.validators import generate_valid_date
from django.core.exceptions import ValidationError
from django.test import TestCase


class CreditCardModelTests(TestCase):
    def setUp(self):
        """Set up data for tests."""

        # Create valid data for credit card
        today = datetime.now()
        valid_exp_date = f"{str(today.month).zfill(2)}/{today.year + 2}"
        self.valid_credit_card = {
            "holder": "John Doe",
            "number": "5447732384411540",
            "exp_date": valid_exp_date,
            "cvv": "123",
        }
        self.valid_brand = "master"

        # Create invalid data for credit card
        self.invalid_credit_card_data = {
            "holder": "John Doe",
            "number": "1111732384411540",
            "exp_date": valid_exp_date,
            "cvv": "123",
        }

        # Create duplicated data for credit card
        self.same_credit_card_number = {
            "holder": "John Brand",
            "number": "5447732384411540",
            "exp_date": valid_exp_date,
            "cvv": "345",
        }

    def test_create_valid_creditcard(self):
        """Test create a valid credit card."""
        credit_card = Creditcard.objects.create(**self.valid_credit_card)
        self.assertEqual(credit_card.holder, self.valid_credit_card["holder"])
        self.assertEqual(credit_card.decrypted_number, self.valid_credit_card["number"])
        self.assertEqual(credit_card.cvv, self.valid_credit_card["cvv"])
        self.assertEqual(credit_card.brand, self.valid_brand)

        exp_date = generate_valid_date(self.valid_credit_card["exp_date"])
        self.assertEqual(credit_card.exp_date, exp_date)

    def test_create_invalid_credit_card(self):
        """Test create a invalid credit card."""
        with self.assertRaises(ValidationError):
            Creditcard.objects.create(**self.invalid_credit_card_data)
