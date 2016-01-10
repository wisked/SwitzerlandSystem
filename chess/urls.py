# __author__ = 'aliaksandr'

from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^competition/$', views.addCompetition, name='addCompetition'),
    url(r'^competition/(?P<pk>[0-9]+)/$', views.registerPlayers, name='registerPlayers'),
    url(r'^competition/(?P<pk>[0-9]+)/start/', views.startCompetition, name='startCompetition'),
    url(r'^competition/(?P<pk>[0-9]+)/rounds/', views.allRounds, name='allRounds'),
    url(r'^competition/(?P<comp_id>\d)/round/(?P<pk>[0-9]+)/$', views.round, name='round'),
    #url(r'^competition/(?P<competition_id>[0-9]+)/round/(?P<pk>[0-9]+)/$', views.round, name='round'),
]
