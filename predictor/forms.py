__author__ = 'sudeep'

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True, max_length=75)
    full_name = forms.CharField(required=True, max_length=70)
    first_name = forms.CharField(required=False, max_length=35)
    last_name = forms.CharField(required=False, max_length=35)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'username', 'password1', 'password2')

    def clean(self):
        form_data = self.cleaned_data
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            self._errors["email"] = ["This email is already taken."] # Will raise a error message
            del form_data['email']
        return form_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        split_name = self.cleaned_data['full_name'].split(" ", 1)
        user.first_name = split_name[0]
        user.last_name = split_name[1]
        if commit:
            user.save()
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
