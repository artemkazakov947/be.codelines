from django.conf import settings
from django.core.mail import send_mail, get_connection, EmailMessage

from apps.website.models import EmailForPostNotification, Post


def send_new_post_notification(post) -> None:
    emails = [email.email for email in EmailForPostNotification.objects.all()]
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject=post.title, message=post.content, from_email=email_from, recipient_list=emails)

# def send_new_post_notification() -> None:
#     with get_connection(
#             host=settings.EMAIL_HOST,
#             port=settings.EMAIL_PORT,
#             username=settings.EMAIL_HOST_USER,
#             password=settings.EMAIL_HOST_PASSWORD,
#             use_tls=settings.EMAIL_USE_TLS
#     ) as connection:
#         subject = "Test"
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = ["artemkazakov947@gmail.com", ]
#         message = "message"
#         EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
