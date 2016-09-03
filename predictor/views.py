import re
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.forms import formset_factory
from django.utils import timezone
from predictor.models import Team, User, Match, Gameweek, Prediction, PredictionResult, GameweekResult
from predictor.forms import PredictionForm

#  Variables
PredictionFormSet = formset_factory(PredictionForm, extra=0)

# Methods
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# View Definitions


def index(request):
    if request.user.is_authenticated():
        users_list = User.objects.order_by('username')
    else:
        users_list = Team.objects.order_by('name')

    context = {'users_list': users_list}
    return render(request, 'predictor/index.html', context)


def error404(request):
    return render(request, 'predictor/404.html')


def adminscripts(request):
    if (not request.user.is_authenticated()) or (not request.user.is_staff()):
        return render(request, 'predictor/404.html')


def home(request):
    return render(request, 'predictor/home.html')


def predict(request):

    if request.user.is_authenticated():
        show_status_message = False
        save_success = True
        now = timezone.now()

        current_gameweek_number = Gameweek.objects.filter(start_time__lte=now, end_time__gte=now)

        # if there is no gameweek available for the current time, then just display the latest gameweek
        if not current_gameweek_number:
            return redirect('/predictor/gameweek/' + re.findall(r'\d+', Gameweek.objects.order_by('-end_time')[0].name)[0])

        current_gameweek_number = current_gameweek_number[0]
        matches_list = Match.objects.filter(gameweek=current_gameweek_number)
        predictions_list = Prediction.objects.filter(user=request.user).filter(match__in=matches_list)
        predictions_dict = {x.pk: x for x in predictions_list}

        if request.method == 'POST':
            show_status_message = True
            try:
                fs = PredictionFormSet(request.POST)
                data = fs.cleaned_data
                for data_point in data:
                    prediction = Prediction.objects.filter(pk=data_point['id'])[0]
                    prediction.home_score = data_point['home_score']
                    prediction.away_score = data_point['away_score']
                    prediction.save()
                save_success = True
            except:
                save_success = False

        initial_list = []
        for prediction in predictions_list:
            initial_list.append(dict(id=prediction.pk,
                                     home_score=prediction.home_score,
                                     away_score=prediction.away_score))
        fs = PredictionFormSet(initial=initial_list)

        context = {
            'fs': fs,
            'current_gameweek_number': current_gameweek_number,
            'predictions_dict': predictions_dict,
            'show_status_message': show_status_message,
            'save_success': save_success
        }
        return render(request, 'predictor/user_current_gameweek.html', context)
    else:
        return redirect('/predictor/')


def gameweek(request, gameweek):

    if request.user.is_authenticated():
        gameweek_instance = Gameweek.objects.filter(name='Gameweek ' + gameweek)[0]
        now = timezone.now()
        if gameweek_instance:
            if gameweek_instance.end_time <= now:

                matches_list = Match.objects.filter(gameweek=gameweek_instance)
                predictions_list = Prediction.objects.filter(user=request.user).filter(match__in=matches_list)
                prediction_results_list = PredictionResult.objects.filter(prediction__in=predictions_list)
                gameweek_result = GameweekResult.objects.get(user=request.user, gameweek=gameweek_instance)

                context = {'gameweek': gameweek,
                           'matches_list': matches_list,
                           'prediction_results_list': prediction_results_list,
                            'gameweek_result': gameweek_result}
                return render(request, 'predictor/user_gameweek.html', context)

            elif gameweek_instance.start_time <= now and gameweek_instance.end_time >= now:
                return redirect('/predictor/predict')
            else:
                return redirect('/predictor/404')
        else:
            return redirect('/predictor/404')
    else:
        return redirect('/predictor/')