import datetime
import pytz
from predictor.models import Leaderboard, FeedbackMessage


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
        print cutoff_time
        if len(FeedbackMessage.objects.filter(user=user, timestamp__gt=cutoff_time)) > 0:
            return False
        else:
            return True
    except:
        return True
