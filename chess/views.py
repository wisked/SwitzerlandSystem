from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from . import models, calculations
from .forms import *
import math
from django.forms.models import modelformset_factory
from django.contrib import auth
# Create your views here.


def index(request):
    return render_to_response('chess/index.html', {'username': auth.get_user(request).username})


# Создание соревнования
def addCompetition(request):
    if request.method == 'POST':
        form = CompetitionForm(request.POST)

        if form.is_valid():
            # time = form.cleaned_data['delivery_time']
            comp = form.save(commit=False)
            comp.save()
            return HttpResponseRedirect('/chess/competition/')

    else:
        form = CompetitionForm()

    competitions = models.Competition.objects.raw('SELECT * FROM competition')
    competition_count = models.Competition.objects.count()
    return render(request, 'chess/addCompetition.html', {'competitions': competitions, 'comp_count': competition_count,
                                                         'form': form, 'username': auth.get_user(request).username })


# Регистрация игроков
def registerPlayers(request, pk):
    name = None
    round_count = models.Round.objects.filter(competition_id=int(pk)).count()
    if request.method == 'POST':
        form = PlayerForm(request.POST)

        if form.is_valid():
            player = form.save(commit=False)
            player.competition_id = int(pk)
            name = player.name
            playerObject = Player.objects.filter(name=name)

            if len(playerObject) > 0:
                name = 0
            else:
                player.save()

    else:
        form = PlayerForm()

    # competitions = models.Competition.objects.raw('SELECT * FROM competition')
    return render(request, 'chess/registerPlayers.html', {'form': form, 'name': name, 'num_comp': int(pk), 'round_count': round_count,
                                                          'username': auth.get_user(request).username})


# Добавление столов и раундов
def startCompetition(request, pk):
    players = models.Player.objects.raw('SELECT id, name, curr_ello_rate FROM player WHERE competition_id={0} '
                                        'ORDER BY name ASC '.format(int(pk)))
    players_count = models.Player.objects.filter(competition_id=pk).count()
    round_count = models.Round.objects.filter(competition_id=pk).count()

    if round_count == 0:

        if request.method == 'POST':
            form = AddPlacesForms(request.POST)

            if form.is_valid():
                amount_place = form.cleaned_data['places']
                round_count = math.trunc(math.log2(players_count) + math.log2(amount_place))
                call = calculations.Query()

                for i in range(1, round_count+1):
                    call.makeQuery('INSERT INTO round VALUES (NULL, %s, %s)', [i, int(pk)])

                for i in range(1, players_count//2+1):
                    call.makeQuery('INSERT INTO table VALUES (NULL, %s, %s)', [i, int(pk)])
                # return render(request, 'chess/startCompetition.html', {'players': players, 'form': form, 'rounds': amount_round})

        else:
            form = AddPlacesForms()
        return render(request, 'chess/startCompetition.html', {'players': players, 'form': form, 'rounds': round_count,
                                                               'num_comp': int(pk), 'players_count': players_count,
                                                               'username': auth.get_user(request).username})

    return render(request, 'chess/startCompetition.html', {'players': players, 'rounds': round_count, 'num_comp': int(pk),
                                                           'players_count': players_count})


def allRounds(request, pk):
    rounds = models.Round.objects.filter(competition_id=int(pk))
    return render_to_response('chess/allRounds.html', {'rounds': rounds, 'comp_id': pk})


def round(request, comp_id, pk):
    players_count = models.Player.objects.filter(competition_id=comp_id).count()
    tables_count = players_count//2
    pair = calculations.PairCalculation(players_count, tables_count, int(pk), int(comp_id))
    query = calculations.Query()

    if int(pk) == 1:
        pair.makePairsForFirstRound()
    else:
        pair.makePairsForNextRound()
    # pair.addResults()

    resultNull_count = query.returnQuery('SELECT COUNT(id) FROM results WHERE result IS NULL ')[0][0]

    players_for_round_query = query.returnQuery('SELECT player.id, player.name, results.num_table, results.result FROM player LEFT '
                                               'JOIN results ON player.id=results.player_id WHERE results.competition_id=%s', [int(pk)])

    for i in players_for_round_query:
        print(i)

    players_for_round = {field[0]: {'name': [], 'result': []} for field in players_for_round_query}


    pair = []
    result = []

    for i in players_for_round:
        for j in players_for_round_query:
            if i == j[0]:
                pair.append(j[1])
                result.append(j[2])
                if len(pair) == 2:
                    players_for_round[i]['name'] = pair
                    players_for_round[i]['result'] = result
                    pair = []
                    result = []
    """
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
    }
    """

    if resultNull_count > 0:
        # ResultFormSet = modelformset_factory(queryset=models.Results.objects.filter(id=2))
        ResultFormSet = modelformset_factory(models.Results, fields=('result',), max_num=players_count)
        if request.method == 'POST':
            formset = ResultFormSet(request.POST, request.FILES, queryset=models.Results.objects.filter(competition_id=comp_id, num_round=pk))
            if formset.is_valid():
                instances = formset.save(commit=False)
                for i in instances:
                    print(i.player_id)
                    i.save()


        else:
            formset = ResultFormSet(queryset=models.Results.objects.filter(competition_id=comp_id, num_round=pk))

        return render(request, 'chess/round.html', {'num_round': int(pk), 'players': players_for_round, 'resultNull': resultNull_count,
                                                'num_comp': comp_id, 'formset': formset})

    return render(request, 'chess/round.html', {'num_round': int(pk), 'players': players_for_round, 'resultNull': resultNull_count,
                                                'num_comp': comp_id})

