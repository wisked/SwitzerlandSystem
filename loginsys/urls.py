from django.conf.urls import patterns, url, include
from . import views

urlpatterns = [
                url(r'^login/', views.login, name='login'),
                url(r'^logout/', views.logout, name='logout'),
              ]