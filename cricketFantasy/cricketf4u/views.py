from django.shortcuts import render, redirect
from cricketf4u.forms import UserForm, UserInformationForm, LeagueForm, TeamForm, LeagueTeamForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.crypto import get_random_string
from cricketf4u.models import Team, League, TeamLeagueLink, Players, PlayerPosition
from django.contrib.auth.models import User

@csrf_protect
def loginorregister(request):
    if request.method == "POST":
        registered = False
        if(
            request.POST.get('action') == "signUP"
        ):
            userform = UserForm(data=request.POST)
            infoform = UserInformationForm(data=request.POST)
            if userform.is_valid() and infoform.is_valid():
                user = userform.save()
                user.set_password(user.password)
                user.save()
                info = infoform.save(commit=False)
                info.user = user
                info.save()
                registered = True
                return HttpResponse("Your account is registered.")
            else:
                print(userform.errors,infoform.errors)
        elif(
                request.POST.get('action') == "login"
            ):
                username = request.POST.get('username')
                password = request.POST.get('pwd')
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request,user,)
                        #return reverse('home', args=[username])
                        return redirect('cricketf4u:home', username = username)
                    else:
                        return HttpResponse("Your account was inactive.")
                else:
                    print("Someone tried to login and failed.")
                    print("They used username: {} and password: {}".format(username,password))
                    return HttpResponse("Invalid login details given")

    return render (request, 'cricketf4u/login.html')

@login_required
def home(request, username):
    username = request.user.username
    if request.method == "POST":
        if(
            request.POST.get('action') == "createleague"
         ):
             leagueform = LeagueForm(data=request.POST)
             teamform = TeamForm(data=request.POST)
             if leagueform.is_valid() and teamform.is_valid():
                 league = leagueform.save(commit=False)
                 league.leagueCode = get_random_string (length=8, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                 league.user = request.user
                 league.save()
                 team= teamform.save(commit=False)
                 team.user = request.user
                 team.save()
                 teamLeagueLink = TeamLeagueLink(team=team, league=league)
                 teamLeagueLink.save()
                 return HttpResponse("Your League is created")
             else:
                 print(leagueform.errors,teamform.errors)
        elif(
             request.POST.get('action') == "joinleague"
             ):
                teamform = TeamForm(data=request.POST)
                if  teamform.is_valid():
                    team= teamform.save(commit=False)
                    team.user = request.user
                    team.save()
                    invitecode = request.POST.get('invitecode')
                    league = League.objects.get(leagueCode = invitecode)
                    teamLeagueLink = TeamLeagueLink(team=team, league=league)
                    teamLeagueLink.save()
                    return HttpResponse("Your have joined in League")
                else:
                    print(teamform.errors)

    return render(request, 'cricketf4u/home.html', {'username':username})


@login_required
def logoutuser(request):
    logout(request)
    return redirect('cricketf4u:login')

@login_required
def schedule(request):
    username = request.user.username
    return render (request, 'cricketf4u/schedule.html', {'username':username})

@login_required
def testjs(request):
    loggedin_user = request.user.username
    data = {
        'username' : loggedin_user
    }

    return JsonResponse(data)

@login_required
def myleagues(request):
    loggedin_user = request.user.username
    userid = User.objects.values_list('id', flat=True).get(username = loggedin_user)
    teamList = Team.objects.filter(user = userid).values_list('id', 'teamName')
    myLeagues = []
    for team in teamList:
        teamLeagueLink = TeamLeagueLink.objects.values('team', 'league').get(team = team[0])
        league = League.objects.values('leagueName').get(id = teamLeagueLink['league'])
        teamName = team[1]
        leagueName = league['leagueName']
        data = {
            'username' : loggedin_user,
            'teamName' : teamName,
            'leagueName' : leagueName,
            'leagueID' : teamLeagueLink['league']
            }
        myLeagues.append(data)

    return JsonResponse(myLeagues, safe = False)

@login_required
def myteams(request):
    loggedin_user = request.user.username
    userid = User.objects.values_list('id', flat=True).get(username = loggedin_user)
    teamList = Team.objects.filter(user = userid).values_list('id', 'teamName')
    myTeams = []
    for team in teamList:
        teamLeagueLink = TeamLeagueLink.objects.values('team', 'league').get(team = team[0])
        league = League.objects.values('leagueName').get(id = teamLeagueLink['league'])
        teamName = team[1]
        leagueName = league['leagueName']
        data = {
            'username' : loggedin_user,
            'teamName' : teamName,
            'teamID' : team[0],
            'leagueName' : leagueName,
            }
        myTeams.append(data)
    return JsonResponse(myTeams, safe = False)

@login_required
def leaguehome(request, leagueID):
    leagueTeamList = []
    teamLeagueLink = TeamLeagueLink.objects.filter(league = leagueID).values_list('team')
    for leagueTeams in teamLeagueLink:
        team = Team.objects.values('teamName', 'user').get(id = leagueTeams[0])
        userName = User.objects.values('username').get(id = team['user'])
        data = {
            'teamName' : team['teamName'],
            'teamUser' : userName['username']
        }
        leagueTeamList.append(data)
    username = request.user.username
    return render (request, 'cricketf4u/leaguehome.html', {'username':username, 'leagueTeamList' : leagueTeamList})

@login_required
def maganeteam(request, username, teamID):
    playersList = []
    username = request.user.username
    players = Players.objects.values('id', 'playerName', 'playerSalary', 'playerPosition', 'playerTeam').all()
    for player in players:
        playerPosition = PlayerPosition.objects.values('position').get(id = player['playerPosition'])
        data = {
            'id' : player['id'],
            'playerName' : player['playerName'],
            'playerSalary' : player['playerSalary'],
            'playerPositionid' : player['playerPosition'],
            'playerPosition' : playerPosition['position'],
            'playerTeam' : player['playerTeam']
        }
        playersList.append(data)
    return render (request, 'cricketf4u/manageteam.html', {'username':username, 'playersList' : playersList})
