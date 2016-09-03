__author__ = 'sudeep'

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from predictor.models import Prediction, PredictionResult, Match, Gameweek, GameweekResult


class Command(BaseCommand):

    help = 'Creates default predictions for all users for a gameweek if they do not already exist'

    def add_arguments(self, parser):
        parser.add_argument('gameweek_number', nargs='+', type=int)

    def handle(self, *args, **options):
        for gameweek_number in args[0]:
            try:
                create_default_predictions(gameweek_number)
            except:
                raise CommandError('Gameweek was not successfully set up :(')
        self.stdout.write('Successfully set up gameweek "%s"' % gameweek_number)


def create_default_predictions(gameweek_number):

    gameweek = Gameweek.objects.filter(name='Gameweek ' + gameweek_number)[0]
    for user in User.objects.all():
        for match in Match.objects.filter(gameweek=gameweek):
            existing_predictions = Prediction.objects.filter(match=match, user=user)
            if not existing_predictions:
                Prediction.objects.create(user=user, match=match)
                prediction = Prediction.objects.filter(user=user, match=match)[0]
                prediction.save()
