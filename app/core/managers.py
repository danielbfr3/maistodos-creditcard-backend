from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, name, author_pseudonym=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Users must have a password")

        if not name:
            raise ValueError("Users must have a name")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.name = name
        user.author_pseudonym = author_pseudonym
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password, email)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
