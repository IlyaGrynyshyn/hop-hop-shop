from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_reset_mail(reset_url: str, user_email: str) -> None:
    subject = "Password reset"
    from_email = "no-replay@hop-hop-shop.me"
#    html_message = render_to_string("order_confirmation.html")

    send_mail(subject, reset_url, from_email, [user_email])
