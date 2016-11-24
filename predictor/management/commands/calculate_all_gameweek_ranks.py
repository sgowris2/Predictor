from django.core.management.base import BaseCommand
from predictor.models import Gameweek, GameweekResult


class Command(BaseCommand):

    help = 'Sends reminder emails for all users who have subscribed to them'

    def add_arguments(self, parser):
        parser.add_argument('gameweek_number')

    def handle(self, *args, **options):
        gameweek_number = options['gameweek_number']
        gameweek = Gameweek.objects.get(name='Gameweek ' + gameweek_number)
        calculate_gameweek_ranks(gameweek)


def calculate_gameweek_ranks(gameweek):
    try:
        gameweek_results = sorted(GameweekResult.objects.filter(gameweek=gameweek),
                                  key=lambda x: x.total_points,
                                  reverse=True)
        for i in range(len(gameweek_results)):
            points = gameweek_results[i].total_points
            gameweek_results[i].rank = len(GameweekResult.objects.filter(gameweek=gameweek, total_points__gt=points)) + 1
            gameweek_results[i].save()
    except:
        print('Gameweek ranks not updated.')