__author__ = 'sudeep'

from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from predictor.models import Match, Prediction, Gameweek


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True, max_length=75)
    full_name = forms.CharField(required=True, max_length=70)
    first_name = forms.CharField(required=False, max_length=35)
    last_name = forms.CharField(required=False, max_length=35)
    reg_agree = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'username', 'password1', 'password2', 'reg_agree')

    def clean(self):
        form_data = self.cleaned_data
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        reg_agree = self.cleaned_data['reg_agree']

        if User.objects.filter(email=email).exists():
            self._errors['email'] = ["This email is already taken."]  # Will raise a error message
            del form_data['email']
        if User.objects.filter(username=username).exists():
            self._errors['username'] = ["This username already exists."]  # Will raise a error message
            del form_data['username']
        if not reg_agree:
            self._errors["reg_agree"] = ["You must agree to the terms."]
            del form_data['reg_agree']
        return form_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        try:
            split_name = self.cleaned_data['full_name'].split(" ", 1)
            user.first_name = split_name[0]
            user.last_name = split_name[1]
        except:
            user.first_name = self.cleaned_data['full_name']
            user.last_name = ''
        if commit:
            user.save()
            now = timezone.now()
            try:
                gameweek = Gameweek.objects.get(start_time__lte=now, end_time__gte=now)
                for match in Match.objects.filter(gameweek=gameweek):
                    existing_predictions = Prediction.objects.filter(match=match, user=user)
                    if not existing_predictions:
                        Prediction.objects.create(user=user, match=match)
                        prediction = Prediction.objects.filter(user=user, match=match)[0]
                        prediction.save()
            except:
                # do nothing
                a = 1
        return user


class PredictionForm(forms.Form):

    id = forms.IntegerField(label='id', widget=forms.HiddenInput)
    home_score = forms.IntegerField(label='home_score',
                                    required=True,
                                    min_value=0,
                                    max_value=99,
                                    validators=[MinValueValidator(0), MaxValueValidator(99)],
                                    widget=forms.NumberInput(attrs={'class': 'score-input'}))
    away_score = forms.IntegerField(label='away_score',
                                    required=True,
                                    min_value=0,
                                    max_value=99,
                                    validators=[MinValueValidator(0), MaxValueValidator(99)],
                                    widget=forms.NumberInput(attrs={'class': 'score-input'}))


class ContactForm(forms.Form):

    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 10, 'cols': 25}), max_length=5000)