from django.shortcuts import render
from predictor.models import Team, User

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
    context = {}
    return render(request, 'predictor/user_current_gameweek.html', context)
