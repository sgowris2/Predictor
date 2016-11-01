from django.contrib import admin
from predictor.models import Team, Gameweek, Match, Prediction, PredictionResult, GameweekResult, GameweekAggregateResult, Leaderboard, \
                            FeedbackMessage, UserProfile

# Register your models here.

admin.site.register(Team)
admin.site.register(Gameweek)
admin.site.register(Match)
admin.site.register(Prediction)
admin.site.register(PredictionResult)
admin.site.register(GameweekResult)
admin.site.register(GameweekAggregateResult)
admin.site.register(Leaderboard)
admin.site.register(FeedbackMessage)
admin.site.register(UserProfile)

