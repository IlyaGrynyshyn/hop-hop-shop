from rest_framework import viewsets, mixins
from email_subscription.serializers import EmailSubscriptionSerializer
from email_subscription.models import SubscribedUser


class EmailSubscriptionView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Endpoint for processing news subscriptions via email.
    Supports only POST requests to create new subscriptions.
    """

    queryset = SubscribedUser.objects.all()
    serializer_class = EmailSubscriptionSerializer
