import os

from django.core.mail import send_mail


def send_reset_password_email(user_id, token, email):
    reset_url = f"{os.environ['PASSWORD_RESET_BASE_URL']}&token={token}&id={user_id}"

    subject = "Password reset"
    from_email = "no-replay@hop-hop-shop.me"

    send_mail(subject=subject, message=reset_url, from_email=from_email, recipient_list=[email])