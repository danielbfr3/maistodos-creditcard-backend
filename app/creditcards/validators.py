import calendar
from datetime import date

from creditcard import CreditCard
from creditcard.exceptions import BrandNotFound
from django.core.exceptions import ValidationError


def validate_exp_date(value):
    """Validate exp_date field."""
    today = date.today()
    current_year = today.year
    current_month = today.month

    # Check if value is in format MM/YYYY
    if len(value) != 7:
        raise ValidationError("Exp format must be MM/YYYY")

    # Check if value is numeric
    month, year = value.split("/")
    if len(year) != 4:
        raise ValidationError("Year must have 4 digits")

    # Check if month has 2 digits
    if len(month) != 2:
        raise ValidationError("Month must have 2 digits")

    # Check if month is between 01 and 12
    if int(month) < 1 or int(month) > 12:
        raise ValidationError("Month must be between 01 and 12")

    # Check if year is greater than current year
    if int(year) <= current_year:
        raise ValidationError("Year must be greater or equal than current year")

    # Check if month is greater than current month
    if int(year) == current_year and int(month) < current_month:
        raise ValidationError("Month must be greater or equal than current month")

    # Check if year is less than 10 years than current year
    if int(year) > current_year + 10:
        raise ValidationError("Year must be less than 10 years than current year")

    return value


def validate_cvv(value):
    """Validate cvv field."""

    # Check if value is numeric
    if not value.isnumeric():
        raise ValidationError("CVV must be numeric")

    # Check if value has 3 or 4 digits
    if len(value) < 3 or len(value) > 4:
        raise ValidationError("CVV must have 3 or 4 digits")

    return value


def validate_number(value):
    """Validate number field."""

    creditcard = CreditCard(value)

    # Check if value is numeric
    if not value.isnumeric():
        raise ValidationError("Number must be numeric")

    # Check if value has 13 to 16 digits
    if len(value) < 13 or len(value) > 16:
        raise ValidationError("Number must have 13 to 16 digits")

    # Check if number is valid
    if not creditcard.is_valid():
        raise ValidationError("Number is not valid")

    return value


def validate_holder(value):
    """Validate holder field."""

    # Check if value has at least 2 characters
    if len(value) < 2:
        raise ValidationError("Holder must have at least 2 characters")

    return value


def validate_brand(value):
    """Validate brand field."""

    creditcard = CreditCard(value)

    # Check if brand is supported
    # CreditCard class raises BrandNotFound exception if brand is not supported
    # We don't want to expose this exception to the user
    # WWe can't accept a creditcard with an unsupported brand
    try:
        brand = creditcard.get_brand()
        if not brand:
            raise ValidationError("Brand not supported")
    except BrandNotFound:
        raise ValidationError("Brand not supported")

    return brand


def generate_valid_date(value):
    """Generate a valid date for exp_date to persist."""

    # Format value to YYYY-MM-DD
    # DD is the last day of the month
    month, year = value.split("/")
    _, last_day = calendar.monthrange(int(year), int(month))
    return f"{year}-{month}-{last_day}"
