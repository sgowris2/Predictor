__author__ = 'sudeep'

import operator
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum
from predictor.models import User, Prediction, PredictionResult, Match, Team, Gameweek, GameweekResult, Leaderboard

RESULT_HOME_WIN = 1
RESULT_AWAY_WIN = 2
RESULT_TIE = 3

RESULT_POINTS = 3
SCORED_POINTS = 1
GOALS_POINTS = 2
EXACT_BONUS_POINTS = 3


class Command(BaseCommand):

    help = 'Calculates and updates the scores in for all predictions in a gameweek'


    def handle(self, *args, **options):
        try:
            gameweek_number = enter_results()
            calculate_scores(gameweek_number)
        except:
            raise CommandError('Predictions were not updated :(')
        self.stdout.write('Successfully updated prediction scores "%s"' % gameweek_number)


def enter_results():

    lines = []
    with open('predictor/results.csv', 'r') as f:
            for line in f.readlines():
                lines.append(line.strip('\n').strip('\r'))
    try:
        print lines[0]
        gameweek = Gameweek.objects.get(name=lines[0])
        gameweek_id = gameweek.id
        for match_line in lines[1:]:
            home,away,home_score,away_score = match_line.split(',')
            try:
                home_team = Team.objects.get(name=home)
                away_team = Team.objects.get(name=away)
                home_team_id = home_team.id
                away_team_id = away_team.id
                try:
                    match = Match.objects.get(home_team_id=home_team_id,
                                              away_team_id=away_team_id,
                                              gameweek_id=gameweek_id,
                                              has_ended=False)
                    match.home_score = home_score
                    match.away_score = away_score
                    match.has_ended = True
                    match.save()
                    print match
                except:
                    print "There are errors in the csv file. Either match was not found or the scores were not integers."
            except:
                print "There are errors in the csv file."
        return gameweek.name
    except:
        print "Gameweek was probably not found."


def calculate_scores(gameweek_number):

    current_gameweek = Gameweek.objects.filter(name=gameweek_number)[0]
    matches = Match.objects.filter(gameweek=current_gameweek)
    predictions = Prediction.objects.filter(match__in=matches)

    for prediction in predictions:
        try:
            prediction_result = PredictionResult.objects.get(prediction=prediction)
            prediction_result.points = calculate_prediction_score(prediction)
            prediction_result.save()
        except:
            PredictionResult.objects.create(prediction=prediction, points=calculate_prediction_score(prediction))
            PredictionResult.objects.get(prediction=prediction).save()

    for user in User.objects.all():
        try:
            gameweek_result = GameweekResult.objects.get(user=user, gameweek=current_gameweek)
            gameweek_result.total_points = get_gameweek_points(predictions.filter(user=user))
            gameweek_result.save()
        except:
            GameweekResult.objects.create(user=user,
                                          gameweek=current_gameweek,
                                          total_points=get_gameweek_points(predictions.filter(user=user)))
            GameweekResult.objects.get(user=user, gameweek=current_gameweek).save()

    calculate_leaderboard()


def calculate_leaderboard():

    leaderboard = {}
    for user in User.objects.all():
        total_points = GameweekResult.objects.filter(user=user).aggregate(Sum('total_points'))
        leaderboard[user] = total_points

    sorted_leaderboard = sorted(leaderboard.items(), key=operator.itemgetter(1), reverse=True)
    Leaderboard.objects.all().delete()
    for item in sorted_leaderboard:
        print
        Leaderboard.objects.create(user=item[0], total_points=item[1]['total_points__sum'])


def calculate_prediction_score(prediction):

    match = prediction.match
    if match.has_ended:
        points = get_result_points(match, prediction)
        points += get_scored_points(match, prediction)
        points += get_goals_points(match, prediction)
        points += get_exact_bonus_points(match, prediction)
        return points
    else:
        return 0


def get_gameweek_points(predictions_list):

    points = 0
    for prediction_result in PredictionResult.objects.filter(prediction__in=predictions_list):
        points += prediction_result.points
    return points


def get_result(home_score, away_score):

    if home_score > away_score:
        return RESULT_HOME_WIN
    if away_score > home_score:
        return RESULT_AWAY_WIN
    return RESULT_TIE


def get_scored(match_score, prediction_score):

    if match_score > 0 and prediction_score > 0:
        return True
    elif match_score == 0 and prediction_score == 0:
        return True
    return False


def get_result_points(match, prediction):

    if get_result(match.home_score, match.away_score) == get_result(prediction.home_score, prediction.away_score):
        return RESULT_POINTS
    return 0


def get_scored_points(match, prediction):

    points = 0
    if get_scored(match.home_score, prediction.home_score):
        points += SCORED_POINTS
    if get_scored(match.away_score, prediction.away_score):
        points += SCORED_POINTS
    return points


def get_goals_points(match, prediction):

    points = 0
    if match.home_score == prediction.home_score:
        points += GOALS_POINTS
    if match.away_score == prediction.away_score:
        points += GOALS_POINTS
    return points


def get_exact_bonus_points(match, prediction):

    if match.home_score == prediction.home_score and match.away_score == prediction.away_score:
        return EXACT_BONUS_POINTS
    return 0
