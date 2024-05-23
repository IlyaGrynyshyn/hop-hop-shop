from django.urls import path, include
from rest_framework.routers import DefaultRouter
from email_subscription.views import EmailSubscriptionView

router = DefaultRouter()
router.register("", EmailSubscriptionView)


urlpatterns = [
    path("", include(router.urls)),
]
