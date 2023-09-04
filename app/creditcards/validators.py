import calendar
from datetime import date

from creditcard import CreditCard
from creditcard.exceptions import BrandNotFound
from django.core.exceptions import ValidationError


def validate_exp_date(value):
    today = date.today()
    current_year = today.year
    current_month = today.month

    if len(value) != 7:
        raise ValidationError("Exp format must be YYYY/MM")

    year, month = value.split("/")
    if len(year) != 4:
        raise ValidationError("Year must have 4 digits")

    if len(month) != 2:
        raise ValidationError("Month must have 2 digits")

    if int(month) < 1 or int(month) > 12:
        raise ValidationError("Month must be between 01 and 12")

    if int(year) <= current_year:
        raise ValidationError("Year must be greater or equal than current year")

    if int(month) < current_month and int(year) >= current_year:
        raise ValidationError("Month must be greater or equal than current month")

    if int(year) > current_year + 10:
        raise ValidationError("Year must be less than 10 years than current year")

    return value


def validate_cvv(value):
    if len(value) < 3 or len(value) > 4:
        raise ValidationError("CVV must have 3 or 4 digits")

    if not value.isnumeric():
        raise ValidationError("CVV must be numeric")

    return value


def validate_number(value):
    creditcard = CreditCard(value)

    if len(value) < 13 or len(value) > 16:
        raise ValidationError("Number must have 13 to 16 digits")

    if not value.isnumeric():
        raise ValidationError("Number must be numeric")

    if not creditcard.is_valid():
        raise ValidationError("Number is not valid")

    return value


def validate_holder(value):
    if len(value) < 2:
        raise ValidationError("Holder must have at least 2 characters")

    return value


def validate_brand(value):
    creditcard = CreditCard(value)

    try:
        brand = creditcard.get_brand()
        if not brand:
            raise ValidationError("Brand not supported")
    except BrandNotFound:
        raise ValidationError("Brand not supported")

    return brand


def generate_valid_date(value):
    year, month = value.split("/")
    _, last_day = calendar.monthrange(int(year), int(month))
    return f"{year}-{month}-{last_day}"
