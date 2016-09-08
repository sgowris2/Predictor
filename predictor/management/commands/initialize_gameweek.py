import csv, sys
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from predictor.models import Match, Gameweek, Team, Prediction


class Command(BaseCommand):

    help = 'Calculates and updates the scores in for all predictions in a gameweek'

    def handle(self, *args, **options):
        try:
            add_matches()
        except:
            raise CommandError('Matches were not added :(')
        self.stdout.write('Successfully added matches')


def add_matches():
    lines = []
    with open('predictor/matches.csv', 'r') as f:
        for line in f.readlines():
            lines.append(line.strip('\n').strip('\r'))
    try:
        print lines[0]
        gameweek = Gameweek.objects.get(name=lines[0])

    except:
        Gameweek.objects.create(name=lines[0])
        gameweek = Gameweek.objects.get(name=lines[0])
        print "Gameweek added - " + gameweek

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
                    print "Match added - " + home_team.name + " vs. " + away_team.name
            except:
                print "There are errors in the csv file."

        for user in User.objects.all():
            for match in Match.objects.filter(gameweek=gameweek):
                existing_predictions = Prediction.objects.filter(match=match, user=user)
                if not existing_predictions:
                    Prediction.objects.create(user=user, match=match)
                    prediction = Prediction.objects.filter(user=user, match=match)[0]
                    prediction.save()
    except:
        print "There are probably errors in the csv file"


