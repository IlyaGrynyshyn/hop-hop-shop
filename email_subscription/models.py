from django.db import models


class SubscribedUser(models.Model):
    email = models.EmailField(unique=True, max_length=50)
