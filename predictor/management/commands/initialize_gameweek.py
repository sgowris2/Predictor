import csv, sys
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from predictor.models import Match, Gameweek, Team, Prediction
from pytz import timezone

class Command(BaseCommand):

    help = 'Calculates and updates the scores in for all predictions in a gameweek'

    def add_arguments(self, parser):
        parser.add_argument('gameweek_name')

    def handle(self, *args, **options):
        try:
            gameweek_name = options['gameweek_name']
            add_matches(gameweek_name)
        except:
            raise CommandError('Matches were not added :(')
        self.stdout.write('Successfully added matches')


def add_matches(gameweek_name):
    lines = []
    with open('predictor/data/' + gameweek_name + '.csv'    , 'r') as f:
        for line in f.readlines():
            lines.append(line.strip('\n').strip('\r'))
    try:
        first_line = lines[0].split(',')
        gameweek_number = (first_line[0].split(' '))[1]
        gameweek = Gameweek.objects.get(name=first_line[0])
    except:
        last_gameweek = Gameweek.objects.get(name='Gameweek ' + (int(gameweek_number) - 1).__str__())
        start_time = last_gameweek.end_time
        end_time = datetime.datetime.strptime(first_line[1], '%d/%b/%Y %H:%M')
        london = timezone('Europe/London')
        end_time = london.localize(end_time)
        gameweek = Gameweek.objects.create(name=first_line[0], start_time=start_time, end_time=end_time)

    gameweek_id = gameweek.id
    try:
        for match in lines[1:]:
            home,away = match.split(',')
            try:
                home_team = Team.objects.get(name=home)
                away_team = Team.objects.get(name=away)
                home_team_id = home_team.id
                away_team_id = away_team.id
                try:
                    Match.objects.get(gameweek_id=gameweek_id, home_team_id=home_team_id, away_team_id=away_team_id)
                except:
                    Match.objects.create(gameweek_id=gameweek_id,home_team_id=home_team_id,away_team_id=away_team_id)
                    print("Match added - " + home_team.name + " vs. " + away_team.name)
            except:
                print("There are errors in the csv file.")

        for user in User.objects.all():
            for match in Match.objects.filter(gameweek=gameweek):
                existing_predictions = Prediction.objects.filter(match=match, user=user)
                if not existing_predictions:
                    Prediction.objects.create(user=user, match=match, is_default=True)
                    prediction = Prediction.objects.filter(user=user, match=match, is_default=True)[0]
                    prediction.save()
    except:
        print("There are probably errors in the csv file")


