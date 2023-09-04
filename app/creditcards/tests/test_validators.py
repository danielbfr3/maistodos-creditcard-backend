from datetime import datetime, timedelta

from creditcards.validators import (
    validate_brand,
    validate_cvv,
    validate_exp_date,
    validate_holder,
    validate_number,
)
from django.core.exceptions import ValidationError
from django.test import TestCase


class CreditCardValidatorsTests(TestCase):
    def setUp(self):
        """Set up data for tests."""

        # Create invalid data for exp_date
        today = datetime.now()
        invalid_format = today.strftime("%Y/%M/%d")
        month_must_have_2_digits = today.strftime("%M/%Y")[0:6]
        year_must_have_4_digits = today.strftime("%M/%Y")[1:7]
        month_must_be_between_01_and_12 = today.strftime("%M/%Y")[0:5] + "13"
        year_must_be_greater_or_equal_than_current_year = (
            f"{str(today.month).zfill(2)}/{today.year - 1}"
        )
        month_must_be_greater_or_equal_than_current_year_and_month = (
            f"{str((today - timedelta(days=31)).month).zfill(2)}/{today.year}"
        )
        year_must_be_less_than_19_years_than_current_year = (
            f"{str(today.month).zfill(2)}/{today.year + 20}"
        )
        self.invalid_exp_date_data = [
            {"exp_date": invalid_format},
            {"exp_date": month_must_have_2_digits},
            {"exp_date": year_must_have_4_digits},
            {"exp_date": month_must_be_between_01_and_12},
            {"exp_date": year_must_be_greater_or_equal_than_current_year},
            {"exp_date": month_must_be_greater_or_equal_than_current_year_and_month},
            {"exp_date": year_must_be_less_than_19_years_than_current_year},
        ]
        # Create valid data for exp_date
        self.valid_exp_date = f"{str(today.month).zfill(2)}/{today.year + 2}"

        # Create invalid data for cvv
        more_than_4_numbers = "12345"
        not_numeric = "123a"
        less_than_3_numbers = "12"
        self.invalid_cvv_data = [
            {"cvv": more_than_4_numbers},
            {"cvv": not_numeric},
            {"cvv": less_than_3_numbers},
        ]
        # Create valid data for cvv
        self.valid_cvv = "123"

        # Create invalid data for credit card number
        less_than_13_numbers = "123456789012"
        more_than_16_numbers = "12345678901234567"
        not_numeric = "123456789012345a"
        self.invalid_number_credit_card_data = [
            {"number": less_than_13_numbers},
            {"number": more_than_16_numbers},
            {"number": not_numeric},
        ]
        # Create valid data for credit card number
        self.valid_number = "5447732384411540"

        # Create invalid data for holder
        less_than_2_characters = "J"
        self.invalid_holder_credit_card_data = [
            {"holder": less_than_2_characters},
        ]
        # Create valid data for holder
        self.valid_holder = "John Doe"

        # Create invalid data for brand
        invalid_brand = "1111199746610016"
        self.invalid_brand_credit_card_data = [
            {"brand": invalid_brand},
        ]
        # Create valid data for brand
        self.valid_brand_number = "5447732384411540"
        self.valid_brand_name = "master"

    def test_validate_exp_date(self):
        """Test validate_exp_date function."""

        for data in self.invalid_exp_date_data:
            with self.assertRaises(ValidationError):
                validate_exp_date(data["exp_date"])

        self.assertEqual(validate_exp_date(self.valid_exp_date), self.valid_exp_date)

    def test_validate_cvv(self):
        """Test validate_cvv function."""

        for data in self.invalid_cvv_data:
            with self.assertRaises(ValidationError):
                validate_cvv(data["cvv"])

        self.assertEqual(validate_cvv(self.valid_cvv), self.valid_cvv)

    def test_validate_number(self):
        """Test validate_number function."""
        for data in self.invalid_number_credit_card_data:
            with self.assertRaises(ValidationError):
                validate_number(data["number"])

        self.assertEqual(validate_number(self.valid_number), self.valid_number)

    def test_validate_holder(self):
        """Test validate_holder function."""
        for data in self.invalid_holder_credit_card_data:
            with self.assertRaises(ValidationError):
                validate_holder(data["holder"])

        self.assertEqual(validate_holder(self.valid_holder), self.valid_holder)

    def test_validate_brand(self):
        """Test validate_brand function."""
        for data in self.invalid_brand_credit_card_data:
            with self.assertRaises(ValidationError):
                validate_brand(data["brand"])

        self.assertEqual(validate_brand(self.valid_brand_number), self.valid_brand_name)
