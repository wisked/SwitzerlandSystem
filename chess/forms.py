# __author__ = 'aliaksandr'

from django import forms
from django.forms.widgets import Widget
from chess.models import Competition, Player, Results
from django.forms.models import BaseModelForm


class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['date', 'information']
        # localized_fields = ('date', 'time')
        # widgets = {
        #     'time': (forms.TimeInput(format='%H:%M')),
        # }
        # help_texts = {
        #     'time': ('00:00'),
        # }

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['new_ello_rate', 'num_table', 'num_round', 'competition']
        widgets = {
            'name': forms.Textarea(attrs={'cols': 30, 'rows': 1})
        }

class AddPlacesForms(forms.Form):
    # max_amount = Player.objects.all().count()
    places = forms.IntegerField(label="Введите количество призовых мест")
