from django.contrib import admin
from predictor.models import Team, Gameweek, Match, Prediction, GameweekResult

# Register your models here.

admin.site.register(Team)
admin.site.register(Gameweek)
admin.site.register(Match)
admin.site.register(Prediction)
admin.site.register(GameweekResult)

