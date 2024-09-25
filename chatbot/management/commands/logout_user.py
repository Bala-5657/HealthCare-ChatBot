from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Log out all users when the server starts"

    def handle(self, *args, **kwargs):
        User.objects.all().update(is_active=False)
        self.stdout.write(self.style.SUCCESS('Successfully logged out all users'))
