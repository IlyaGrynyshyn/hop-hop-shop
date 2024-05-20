from online_store.settings.base import *

ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1"]

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydatabase",
        "USER": "myuser",
        "PASSWORD": "mypassword",
        "HOST": "db",
        "PORT": "5432",
    }
}
