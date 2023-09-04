from datetime import datetime

from creditcards.models import Creditcard
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase


class CreditCardModelTests(TestCase):
    def setUp(self):
        today = datetime.now()
        valid_exp_date = f"{today.year + 2}/{str(today.month).zfill(2)}"

        self.valid_credit_card = {
            "holder": "John Doe",
            "number": "5447732384411540",
            "exp_date": valid_exp_date,
            "cvv": "123",
        }
        self.valid_brand = "master"

        self.invalid_credit_card_data = {
            "holder": "John Doe",
            "number": "1111732384411540",
            "exp_date": valid_exp_date,
            "cvv": "123",
        }

        self.same_credit_card_number = {
            "holder": "John Brand",
            "number": "5447732384411540",
            "exp_date": valid_exp_date,
            "cvv": "345",
        }

    def test_create_valid_creditcard(self):
        credit_card = Creditcard.objects.create(**self.valid_credit_card)
        self.assertEqual(credit_card.holder, self.valid_credit_card["holder"])
        self.assertEqual(credit_card.number, self.valid_credit_card["number"])
        self.assertEqual(credit_card.exp_date, self.valid_credit_card["exp_date"])
        self.assertEqual(credit_card.cvv, self.valid_credit_card["cvv"])
        self.assertEqual(credit_card.brand, self.valid_brand)

    def test_create_invalid_credit_card(self):
        with self.assertRaises(ValidationError):
            Creditcard.objects.create(**self.invalid_credit_card_data)

    def test_create_duplicated_credit_card(self):
        creditcard = Creditcard.objects.get_or_create(**self.valid_credit_card)
        self.assertEqual(creditcard[1], True)
        with self.assertRaises(IntegrityError):
            Creditcard.objects.create(**self.same_credit_card_number)
