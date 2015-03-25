from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Gameweek(models.Model):
    number = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.number


class Match(models.Model):
    gameweek = models.ForeignKey(Gameweek)
    home_team = models.ForeignKey(Team, related_name='match_home_team')
    away_team = models.ForeignKey(Team, related_name='match_away_team')
    has_ended = models.BooleanField(default=0)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)

    def __str__(self):
        return self.home_team + ' vs. ' + self.away_team

class Prediction(models.Model):
    user = models.ForeignKey(User)
    match = models.ForeignKey(Match)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    is_doubled = models.BooleanField(default=0)
    result = models.BooleanField(default=0)
    goal_difference = models.BooleanField(default=0)
    home_goals = models.BooleanField(default=0)
    away_goals = models.BooleanField(default=0)
    total_goals = models.BooleanField(default=0)
    scoreline = models.BooleanField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.name + ' - ' + self.match.__str__() + ' - ' + self.home_score + ' - ' + self.away_score


class GameweekResult(models.Model):
    user = models.ForeignKey(User)
    gameweek = models.ForeignKey(Gameweek)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.name + ' - Gameweek ' + self.gameweek.__str__()





