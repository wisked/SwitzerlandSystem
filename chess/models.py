from django.db import models
# import datetime.date
from django.utils import timezone
# Create your models here.


class Competition(models.Model):
    information = models.CharField('Информация', max_length=100, blank=True)
    date = models.DateField('Дата')
    # time = models.CharField('Время', max_length=20)

    class Meta:
        db_table = 'competition'

    def __str__(self):
        return str(self.id)


class Round(models.Model):
    competition = models.ForeignKey(Competition, null=True)
    num_round = models.PositiveIntegerField()

    class Meta:
        db_table = 'round'


class Table(models.Model):
    num_competition = models.ForeignKey(Competition, null=True)
    num_table = models.PositiveIntegerField()

    class Meta:
        db_table = 'table'


class Player(models.Model):
    competition = models.ForeignKey(Competition, null=True)
    name = models.CharField('Имя игрока',max_length=100)
    age = models.PositiveIntegerField('Возраст')
    curr_ello_rate = models.PositiveIntegerField('Ello рэйтинг', help_text='Текущий рейтинг')
    new_ello_rate = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'player'


class Results(models.Model):
    RESULTS = (
        (1, 'Победа'),
        (0.5, 'Ничья'),
        (0, 'Проигрыш'),
    )
    player = models.ForeignKey(Player)
    competition = models.ForeignKey(Competition)
    num_round = models.PositiveIntegerField(null=True)
    num_table = models.PositiveIntegerField(null=True)
    result = models.FloatField(choices=RESULTS, null=True, blank=True)

    class Meta:
        db_table = 'results'