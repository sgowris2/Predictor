from predictor.models import Leaderboard


def get_rank(user):
    try:
        user_points = Leaderboard.objects.get(user=user)
        higher_ranked_users = Leaderboard.objects.filter(total_points__gt=user_points)
        return higher_ranked_users.count() + 1
    except:
        return 0
