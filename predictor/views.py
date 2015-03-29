from django.shortcuts import render, redirect
from time import timezone
from predictor.models import Team, User, Match, Gameweek, Prediction

# Create your views here.

def index(request):
    teams_list = Team.objects.order_by('name')
    if request.user.is_authenticated():
        users_list = User.objects.order_by('username')
    else:
        users_list = Team.objects.order_by('name')

    context = {'users_list': users_list}
    return render(request, 'predictor/index.html', context)

def current_gameweek(request):
    if request.user.is_authenticated():
        current_gw = Gameweek.objects.order_by('end_time').last()
        matches_list = Match.objects.filter(gameweek=current_gw)
        predictions_list = Prediction.objects.filter(user=request.user).filter(match__in=matches_list)
    else:
        return redirect('/predictor/')

    context = {'matches_list': matches_list, 'predictions_list': predictions_list}
    return render(request, 'predictor/user_current_gameweek.html', context)
