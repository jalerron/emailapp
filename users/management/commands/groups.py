from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        manager_group, created = Group.objects.get_or_create(name='Manager')
        if created:
            permissions = Permission.objects.filter(
                codename__in=['view_mailings', 'set_active', 'view_user', 'set_active']
            )

            manager_group.permissions.set(permissions)
