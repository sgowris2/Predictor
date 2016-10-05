import datetime
import pytz
from predictor.models import Gameweek, GameweekResult, Leaderboard, FeedbackMessage


def get_rank(user):
    try:
        user_points = Leaderboard.objects.get(user=user)
        higher_ranked_users = Leaderboard.objects.filter(total_points__gt=user_points)
        return higher_ranked_users.count() + 1
    except:
        return 0


def contact_timeout_check(user):
    try:
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        cutoff_time = (now - datetime.timedelta(minutes=15))
        if len(FeedbackMessage.objects.filter(user=user, timestamp__gt=cutoff_time)) > 0:
            return False
        else:
            return True
    except:
        return True


def get_unresulted_gameweeks(user):

    unresulted_gameweeks = []
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    print(now)

    for gameweek in Gameweek.objects.filter(end_time__lte=now):
        try:
            GameweekResult.objects.get(gameweek=gameweek, user=user)
        except:
            unresulted_gameweeks.append(gameweek)
    return unresulted_gameweeks


def get_previous_gameweek(gameweek_number):

    try:
        gameweek_int = int(gameweek_number)
        if gameweek_int > 1:
            try:
                Gameweek.objects.get(name='Gameweek ' + (gameweek_int - 1).__str__())
                return gameweek_int - 1
            except:
                return 0
        return 0
    except:
        return 0


def get_next_gameweek(gameweek_number):
    try:
        gameweek_int = int(gameweek_number)
        if gameweek_int >= 1:
            try:
                Gameweek.objects.get(name='Gameweek ' + (gameweek_int + 1).__str__())
                return gameweek_int + 1
            except:
                return 0
        return 0
    except:
        return 0
