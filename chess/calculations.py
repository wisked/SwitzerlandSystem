# __author__ = 'aliaksandr'
from django.db import connection
from . import models

class Query:

    def makeQuery(self, query, *args):
        try:
            c = connection.cursor()
            c.execute(query, *args)
        except:
            print('error in SQL')

        finally:
            c.close()


    def returnQuery(self, query, *args):
        with connection.cursor() as c:

            c.execute(query, *args)
            return c.fetchall()


class PairCalculation:
    def __init__(self, amount_players, amount_tables, num_round, comp_id):
        self.amount_players = amount_players
        self.amount_tables = amount_tables
        self.num_round = num_round
        self.competition_id = comp_id
        self.query = Query()

    def addResults(self):
        players_id = self.query.returnQuery('SELECT id FROM player WHERE competition_id=%s ', [self.competition_id])
        for id in players_id:
            self.query.makeQuery('INSERT INTO results VALUES (NULL, %s, NULL, NULL, %s, %s )', [self.num_round, self.competition_id, id[0]])


    def makePairsForFirstRound(self):
        first_part = models.Player.objects.raw('SELECT * FROM player WHERE competition_id=%s ORDER BY curr_ello_rate '
                                               'DESC LIMIT %s', [self.competition_id, self.amount_players//2])
        second_part = models.Player.objects.raw('SELECT * FROM player WHERE competition_id=%s ORDER BY curr_ello_rate '
                                                'DESC LIMIT %s, %s', [self.competition_id, self.amount_players//2, self.amount_players])

        """self.query.makeQuery('delimiter//'
                             'create procedure insertResult(in nRound int, in tRound int, in compId int, in playerId int)'
                             'if not exists (select id from results where num_round=1 and competition_id=1 and player_id=playerId)'
                             'then insert into results values (null, nRound, tRound, null, compId, playerId);'
                             'end if;//')"""
        self.query.makeQuery('insert into results VALUES (NULL, 2, 3, NULL, 1, 2) if not exists (select id from results'
                             'where num_round=1 and competition_id=1)')
        # for i in range(self.amount_tables):
        # self.query.makeQuery('call insertResult(1,2,1,3)')
            # self.query.makeQuery('call()', [self.num_round, i+1, self.competition_id, first_part[i].id])
            # self.query.makeQuery('call(%s, %s, %s, %s)', [self.num_round, i+1,  self.competition_id, second_part[i].id])


    def makePairsForNextRound(self):
        # winners = models.Results.objects.raw('SELECT * FROM chess_results WHERE competition_id=%s AND num_round=%s AND result=1')
        # tie = models.Results.objects.raw('SELECT * FROM chess_results WHERE competition_id=%s AND num_round=%s AND result=0')
        # losers = models.Results.objects.raw('SELECT * FROM chess_results WHERE competition_id=%s AND num_round=%s AND result=0')

        # winners_count = models.Results.objects.filter(competition_id=self.competition_id, num_round=self.num_round, result=1).count()
        # print(winners_count)
        # tie_count = models.Results.objects.filter(competition_id=self.competition_id, num_round=self.num_round, result=0.5).count()
        # print(tie_count)
        losers_count = models.Results.objects.filter(competition_id=self.competition_id, num_round=2, result=0).count()
        print(losers_count)

        if losers_count % 2 != 0:
            self.query.makeQuery('SELECT player.id FROM player JOIN results ON player.id=results.player_id'
                                 'WHERE result.result=0 AND results.num_round=%s AND result.competition_id=%s '
                                 'ORDER BY player.curr_ello_rate DESC ', [self.num_round, self.competition_id])




    def makeResult(self):
        self.query.makeQuery('INSERT INTO results VALUES (NULL, %s, NULL, %s, %s )', [])





