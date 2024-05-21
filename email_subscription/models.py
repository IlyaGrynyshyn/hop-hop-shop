from django.db import models


class SubscribedUser(models.Model):
    email = models.CharField(unique=True, max_length=50)
