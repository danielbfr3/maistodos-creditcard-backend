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
        today = datetime.now()
        invalid_format = today.strftime("%Y/%M/%d")
        month_must_have_2_digits = today.strftime("%Y/%M")[0:6]
        year_must_have_4_digits = today.strftime("%Y/%M")[1:7]
        month_must_be_between_01_and_12 = today.strftime("%Y/%M")[0:5] + "13"
        year_must_be_greater_or_equal_than_current_year = (
            f"{today.year - 1}/{str(today.month).zfill(2)}"
        )
        month_must_be_greater_or_equal_than_current_year_and_month = (
            f"{today.year}/{str((today - timedelta(days=31)).month).zfill(2)}"
        )
        year_must_be_less_than_19_years_than_current_year = (
            f"{today.year + 20}/{str(today.month).zfill(2)}"
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
        self.valid_exp_date = f"{today.year + 2}/{str(today.month).zfill(2)}"

        more_than_4_numbers = "12345"
        not_numeric = "123a"
        less_than_3_numbers = "12"
        self.invalid_cvv_data = [
            {"cvv": more_than_4_numbers},
            {"cvv": not_numeric},
            {"cvv": less_than_3_numbers},
        ]
        self.valid_cvv = "123"

        less_than_13_numbers = "123456789012"
        more_than_16_numbers = "12345678901234567"
        not_numeric = "123456789012345a"
        self.invalid_number_credit_card_data = [
            {"number": less_than_13_numbers},
            {"number": more_than_16_numbers},
            {"number": not_numeric},
        ]
        self.valid_number = "5447732384411540"

        less_than_2_characters = "J"
        self.invalid_holder_credit_card_data = [
            {"holder": less_than_2_characters},
        ]
        self.valid_holder = "John Doe"

        invalid_brand = "1111199746610016"
        self.invalid_brand_credit_card_data = [
            {"brand": invalid_brand},
        ]
        self.valid_brand_number = "5447732384411540"
        self.valid_brand_name = "master"

    def test_validate_exp_date(self):
        for data in self.invalid_exp_date_data:
            with self.assertRaises(ValidationError):
                validate_exp_date(data["exp_date"])

        self.assertEqual(validate_exp_date(self.valid_exp_date), self.valid_exp_date)

    def test_validate_cvv(self):
        for data in self.invalid_cvv_data:
            with self.assertRaises(ValidationError):
                validate_cvv(data["cvv"])

        self.assertEqual(validate_cvv(self.valid_cvv), self.valid_cvv)

    def test_validate_number(self):
        for data in self.invalid_number_credit_card_data:
            with self.assertRaises(ValidationError):
                validate_number(data["number"])

        self.assertEqual(validate_number(self.valid_number), self.valid_number)

    def test_validate_holder(self):
        for data in self.invalid_holder_credit_card_data:
            with self.assertRaises(ValidationError):
                validate_holder(data["holder"])

        self.assertEqual(validate_holder(self.valid_holder), self.valid_holder)

    def test_validate_brand(self):
        for data in self.invalid_brand_credit_card_data:
            with self.assertRaises(ValidationError):
                validate_brand(data["brand"])

        self.assertEqual(validate_brand(self.valid_brand_number), self.valid_brand_name)
