from django.core.cache import cache
from django.core.mail import send_mail

from emailapp import settings
from main.models import Client


def send_mass_mail(subject: str, message: str, client_list: list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        client_list
    )


def get_client_cache(user):
    key = 'client_list'
    client_list = cache.get(key)
    if client_list is None:
        client_list = Client.objects.filter(owner=user)
        cache.set(key, client_list)
    return client_list

