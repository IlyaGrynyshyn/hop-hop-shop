from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from datetime import timedelta

from authentication.managers import UserManager


class Customer(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(_("phone number"), max_length=17, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class PasswordReset(models.Model):
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    user = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        self.expires_at = self.created_at + timedelta(days=1)
        super().save(*args, **kwargs)
