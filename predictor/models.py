from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    reminders = models.BooleanField()
    updates = models.BooleanField()

    def __str__(self):
        return self.user.__str__() + ' - Reminders: ' + self.reminders.__str__() + ' - Updates: ' + self.updates.__str__()


class Team(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Gameweek(models.Model):
    name = models.CharField(max_length=15)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_complete = models.BooleanField(default=False)

    def number(self):
        return int(self.name.split(' ')[1])

    def __str__(self):
        return self.name


class Match(models.Model):
    gameweek = models.ForeignKey(Gameweek)
    home_team = models.ForeignKey(Team, related_name='match_home_team')
    away_team = models.ForeignKey(Team, related_name='match_away_team')
    has_ended = models.BooleanField(default=0)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)

    def __str__(self):
        return self.home_team.name + ' vs. ' + self.away_team.name

    def get_home_team_name(self):
        return self.home_team.name

    def get_away_team_name(self):
        return self.away_team.name


class Prediction(models.Model):
    user = models.ForeignKey(User)
    match = models.ForeignKey(Match)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    is_default = models.BooleanField(default=1)

    def __str__(self):
        return self.user.__str__() + ' - ' + self.match.__str__() + ' - ' + str(self.home_score) + ' - ' + str(self.away_score)

    def get_home_team_name(self):
        return self.match.get_home_team_name()

    def get_away_team_name(self):
        return self.match.get_away_team_name()


class PredictionResult(models.Model):
    prediction = models.ForeignKey(Prediction)
    result = models.BooleanField(default=False)
    home_scored = models.BooleanField(default=False)
    away_scored = models.BooleanField(default=False)
    home_goals = models.BooleanField(default=False)
    away_goals = models.BooleanField(default=False)
    scoreline = models.BooleanField(default=False)
    penalty_points = models.IntegerField(default=0)
    points = models.IntegerField(default=0)


class GameweekResult(models.Model):
    rank = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    gameweek = models.ForeignKey(Gameweek)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.__str__() + ' ' + self.gameweek.__str__() + ' ' + self.total_points.__str__()


class GameweekAggregateResult(models.Model):
    gameweek = models.ForeignKey(Gameweek)
    highest_score = models.IntegerField(default=0)
    average_score = models.IntegerField(default=0)
    most_guessed_result = models.ForeignKey(Match, related_name='most_guessed_result', default=None)
    least_guessed_result = models.ForeignKey(Match, related_name='least_guessed_result', default=None)

    def __str__(self):
        return self.gameweek.__str__() + ' aggregate result'


class Leaderboard(models.Model):
    rank = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.__str__() + ' - ' + self.total_points.__str__()


class FeedbackMessage(models.Model):

    user = models.ForeignKey(User)
    message = models.CharField(max_length=5000)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.user.__str__() + ' - ' + self.message.__str__()




