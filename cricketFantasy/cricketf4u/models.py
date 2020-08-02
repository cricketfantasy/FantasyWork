from django.db import models
from django.contrib.auth.models import User

class UserInformation(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    dateOfBirth = models.DateField('date of birth')

    def __str__(self):
        return self.user.username

class League(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leagueName = models.CharField(max_length=50)
    noOfTeams = models.CharField(max_length=20)
    toPublic = models.CharField(max_length=10)
    leagueCode = models.CharField(max_length=10)

class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    teamName = models.CharField(max_length=50)

class TeamLeagueLink(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class PlayerPosition(models.Model):
    position = models.CharField(max_length=20)

class Players(models.Model):
    playerName = models.CharField(max_length=100)
    playerSalary = models.IntegerField()
    playerPosition =  models.ForeignKey(PlayerPosition, on_delete=models.CASCADE)
    playerTeam = models.CharField(max_length=50)
