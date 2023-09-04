from creditcards.validators import (
    generate_valid_date,
    validate_brand,
    validate_cvv,
    validate_exp_date,
    validate_holder,
    validate_number,
)
from cryptography.fernet import Fernet
from django.db import models


class Creditcard(models.Model):
    _encryption_key = Fernet.generate_key()

    def __init__(self, *args, **kwargs):
        super(Creditcard, self).__init__(*args, **kwargs)
        self._cipher_suite = Fernet(self._encryption_key)

    holder = models.CharField(max_length=255, validators=[validate_holder])
    number = models.CharField(max_length=255, validators=[validate_number])
    brand = models.CharField(max_length=255)
    exp_date = models.CharField(max_length=10, validators=[validate_exp_date])
    cvv = models.CharField(max_length=4, validators=[validate_cvv])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.holder} - {self.brand}"

    def _encrypt_number(self, number):
        """Encrypt the credit card number."""
        return self._cipher_suite.encrypt(number.encode()).decode()

    def _decrypt_number(self, encrypted_number):
        """Decrypt the encrypted credit card number."""
        return self._cipher_suite.decrypt(encrypted_number.encode()).decode()

    def save(self, *args, **kwargs):
        """Save the credit card."""

        # Validate the credit card number and generate the brand
        self.brand = validate_brand(self.number)

        # Encrypt the credit card number
        self.number = self._encrypt_number(self.number)

        # Generate a valid expiration date to persist in the database
        self.exp_date = generate_valid_date(self.exp_date)
        super(Creditcard, self).save(*args, **kwargs)

    @property
    def decrypted_number(self):
        """Return the decrypted credit card number."""
        return self._decrypt_number(self.number)
