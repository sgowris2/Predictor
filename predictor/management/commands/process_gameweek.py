__author__ = 'sudeep'

import operator
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum, Max, Avg
from predictor.models import User, Prediction, PredictionResult, Match, Team, Gameweek, GameweekResult, GameweekAggregateResult, Leaderboard

HOME = 1
AWAY = 2

RESULT_HOME_WIN = 1
RESULT_AWAY_WIN = 2
RESULT_TIE = 3

RESULT_POINTS = 3
SCORED_POINTS = 1
GOALS_POINTS = 2
EXACT_BONUS_POINTS = 3


class Command(BaseCommand):

    help = 'Calculates and updates the scores in for all predictions in a gameweek'

    def add_arguments(self, parser):
        parser.add_argument('gameweek_name')

    def handle(self, *args, **options):
        try:
            gameweek_name = options['gameweek_name']
            gameweek_number = enter_results(gameweek_name)
            calculate_scores(gameweek_number)
        except:
            raise CommandError('Predictions were not updated :(')
        self.stdout.write('Successfully updated prediction scores "%s"' % gameweek_number)


def enter_results(gameweek_name):

    lines = []
    with open('predictor/data/' + gameweek_name + '_results.csv', 'r') as f:
            for line in f.readlines():
                lines.append(line.strip('\n').strip('\r'))
    try:
        print(lines[0])
        gameweek = Gameweek.objects.get(name=lines[0])
        gameweek_id = gameweek.id
        for match_line in lines[1:]:
            try:
                home,away,home_score,away_score = match_line.split(',')
                home_team = Team.objects.get(name=home)
                away_team = Team.objects.get(name=away)
                home_team_id = home_team.id
                away_team_id = away_team.id
                try:
                    match = Match.objects.get(home_team_id=home_team_id,
                                              away_team_id=away_team_id,
                                              gameweek_id=gameweek_id,
                                              )
                    match.home_score = home_score
                    match.away_score = away_score
                    match.has_ended = True
                    match.save()
                    print(match)
                except:
                    print("There are errors in the csv file. Either match was not found or the scores were not integers.")
            except:
                print("There are errors in the csv file.")
        return gameweek
    except:
        print("Gameweek was probably not found.")


def calculate_scores(gameweek):

    current_gameweek = Gameweek.objects.filter(name=gameweek.name)[0]
    matches = Match.objects.filter(gameweek=current_gameweek)
    predictions = Prediction.objects.filter(match__in=matches)

    for prediction in predictions:
        try:
            prediction_result = PredictionResult.objects.get(prediction=prediction)
            prediction_result.points = calculate_prediction_score(prediction)
            update_prediction_result_stats(prediction_result)
            prediction_result.save()
        except:
            PredictionResult.objects.create(prediction=prediction, points=calculate_prediction_score(prediction))
            update_prediction_result_stats(PredictionResult.objects.get(prediction=prediction))
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
    calculate_gameweekaggregateresult(current_gameweek)


def calculate_gameweekaggregateresult(current_gameweek):
    try:
        gameweek_aggregate_result = GameweekAggregateResult.objects.get(gameweek=current_gameweek)
    except:
        GameweekAggregateResult.objects.create(gameweek=current_gameweek,
                                               most_guessed_result=Match.objects.filter(gameweek=current_gameweek)[0],
                                               least_guessed_result=Match.objects.filter(gameweek=current_gameweek)[0])
        gameweek_aggregate_result = GameweekAggregateResult.get(gameweek=current_gameweek)

    gameweek_aggregate_result.highest_score = get_highest_score(current_gameweek)
    gameweek_aggregate_result.average_score = get_average_score(current_gameweek)
    gameweek_aggregate_result.most_guessed_result = get_most_guessed_result(current_gameweek)
    gameweek_aggregate_result.least_guessed_result = get_least_guessed_result(current_gameweek)
    gameweek_aggregate_result.save()

def calculate_leaderboard():

    leaderboard = {}
    for user in User.objects.all():
        total_points = GameweekResult.objects.filter(user=user).aggregate(Sum('total_points'))
        leaderboard[user] = total_points

    sorted_leaderboard = sorted(leaderboard.items(), key=operator.itemgetter(1), reverse=True)
    Leaderboard.objects.all().delete()
    rank = 1
    for item in sorted_leaderboard:
        Leaderboard.objects.create(rank=rank, user=item[0], total_points=item[1]['total_points__sum'])
        rank += 1


def calculate_prediction_score(prediction):

    match = prediction.match
    if match.has_ended:
        points =  get_result_points(match, prediction)
        points += get_scored_points(match, prediction)
        points += get_goals_points(match, prediction)
        points += get_exact_bonus_points(match, prediction)
        return points
    else:
        return 0


def update_prediction_result_stats(prediction_result):

    prediction = prediction_result.prediction
    match = prediction.match
    prediction_result.result = get_result_points(match, prediction) > 0
    prediction_result.home_scored = get_scored_points(match, prediction, HOME) > 0
    prediction_result.away_scored = get_scored_points(match, prediction, AWAY) > 0
    prediction_result.home_goals = get_goals_points(match, prediction, HOME) > 0
    prediction_result.away_goals = get_goals_points(match, prediction, AWAY) > 0
    prediction_result.scoreline = get_exact_bonus_points(match, prediction) > 0
    prediction_result.save()


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


def get_scored_points(match, prediction, home_or_away = 0):

    points = 0
    if home_or_away == HOME or home_or_away == 0:
        if get_scored(match.home_score, prediction.home_score):
            points += SCORED_POINTS
    if home_or_away == AWAY or home_or_away == 0:
        if get_scored(match.away_score, prediction.away_score):
            points += SCORED_POINTS
    return points


def get_goals_points(match, prediction, home_or_away = 0):

    points = 0
    if home_or_away == HOME or home_or_away == 0:
        if match.home_score == prediction.home_score:
            points += GOALS_POINTS
    if home_or_away == AWAY or home_or_away == 0:
        if match.away_score == prediction.away_score:
            points += GOALS_POINTS
    return points


def get_exact_bonus_points(match, prediction):

    if match.home_score == prediction.home_score and match.away_score == prediction.away_score:
        return EXACT_BONUS_POINTS
    return 0


def get_highest_score(gameweek):
    return GameweekResult.objects.filter(gameweek=gameweek).aggregate(Max('total_points'))['total_points__max']


def get_average_score(gameweek):
    return round(GameweekResult.objects.filter(gameweek=gameweek).aggregate(Avg('total_points'))['total_points__avg'], 0)


def get_most_guessed_result(gameweek):

    sum = 0
    result_match = None
    for match in Match.objects.filter(gameweek=gameweek):
        temp_sum = PredictionResult.objects.filter(prediction__match=match).aggregate(Sum('result'))['result__sum']
        if temp_sum > sum:
            sum = temp_sum
            result_match = match

    return result_match


def get_least_guessed_result(gameweek):

    sum = 99999999
    result_match = None
    for match in Match.objects.filter(gameweek=gameweek):
        temp_sum = PredictionResult.objects.filter(prediction__match=match).aggregate(Sum('result'))['result__sum']
        if temp_sum < sum:
            sum = temp_sum
            result_match = match

    return result_match
