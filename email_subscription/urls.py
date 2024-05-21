from django.urls import path, include
from rest_framework.routers import DefaultRouter
from email_subscription.views import EmailSubscriptionViewSet

router = DefaultRouter()
router.register("", EmailSubscriptionViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
