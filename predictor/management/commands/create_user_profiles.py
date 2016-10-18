from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from predictor.models import UserProfile


class Command(BaseCommand):

    help = 'Sends reminder emails for all users who have subscribed to them'

    def handle(self, *args, **options):
        create_user_profiles()


def create_user_profiles():

    users = User.objects.all()
    for user in users:
        try:
            UserProfile.objects.get(user=user)
        except:
            UserProfile.objects.create(user=user, reminders=True, updates=True)
