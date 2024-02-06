from django.core.management import BaseCommand
from main.models import Mailings, Message, Client, Logs
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('dumpdata', 'main', 'users', output='data.json')
        Mailings.objects.all().delete()
        Message.objects.all().delete()
        Client.objects.all().delete()
        Logs.objects.all().delete()
