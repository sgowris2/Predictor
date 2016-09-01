__author__ = 'sudeep'

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


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
