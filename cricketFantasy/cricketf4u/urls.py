from django.conf.urls import url
from django.urls import path
from cricketf4u import views

app_name = 'cricketf4u'# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    path('login/',views.loginorregister,name='login'),
    path('<username>/home/',views.home,name='home'),
    path('logout/', views.logoutuser, name='logout'),
    path('schedule/', views.schedule, name='schedule'),
    path('testjs/', views.testjs, name='testjs'),
    path('myleagues/', views.myleagues, name='myleagues'),
    path('myteams/', views.myteams, name='myteams'),
    path('leaguehome/<leagueID>', views.leaguehome, name='leaguehome'),
    path('<username>/manageteam/<teamID>', views.maganeteam, name='maganeteam'),
]
