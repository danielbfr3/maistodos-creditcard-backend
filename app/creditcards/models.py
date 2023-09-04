from creditcards.validators import (
    generate_valid_date,
    validate_brand,
    validate_cvv,
    validate_exp_date,
    validate_holder,
    validate_number,
)
from django.db import models


class Creditcard(models.Model):
    holder = models.CharField(max_length=255, validators=[validate_holder])
    number = models.CharField(max_length=16, unique=True, validators=[validate_number])
    brand = models.CharField(max_length=255)
    exp_date = models.CharField(max_length=10, validators=[validate_exp_date])
    cvv = models.CharField(max_length=4, validators=[validate_cvv])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.holder} - {self.brand}"

    def save(self, *args, **kwargs):
        self.brand = validate_brand(self.number)
        self.exp_date = generate_valid_date(self.exp_date)
        super(Creditcard, self).save(*args, **kwargs)
