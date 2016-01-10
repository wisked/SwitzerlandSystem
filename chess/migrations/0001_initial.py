# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('information', models.CharField(verbose_name='Информация', max_length=100, blank=True)),
                ('date', models.DateField(verbose_name='Дата')),
            ],
            options={
                'db_table': 'competition',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='Имя игрока', max_length=100)),
                ('age', models.PositiveIntegerField(verbose_name='Возраст')),
                ('curr_ello_rate', models.PositiveIntegerField(verbose_name='Ello рэйтинг', help_text='Текущий рейтинг')),
                ('new_ello_rate', models.PositiveIntegerField(blank=True, null=True)),
                ('competition', models.ForeignKey(null=True, to='chess.Competition')),
            ],
            options={
                'db_table': 'player',
            },
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('num_round', models.PositiveIntegerField(null=True)),
                ('num_table', models.PositiveIntegerField(null=True)),
                ('result', models.FloatField(choices=[(1, 'Победа'), (0.5, 'Ничья'), (0, 'Проигрыш')], blank=True, null=True)),
                ('competition', models.ForeignKey(to='chess.Competition')),
                ('player', models.ForeignKey(to='chess.Player')),
            ],
            options={
                'db_table': 'results',
            },
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('num_round', models.PositiveIntegerField()),
                ('competition', models.ForeignKey(null=True, to='chess.Competition')),
            ],
            options={
                'db_table': 'round',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('num_table', models.PositiveIntegerField()),
                ('num_competition', models.ForeignKey(null=True, to='chess.Competition')),
            ],
            options={
                'db_table': 'table',
            },
        ),
    ]
