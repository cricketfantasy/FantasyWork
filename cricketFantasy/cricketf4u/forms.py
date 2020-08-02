from django import forms
from cricketf4u.models import UserInformation , League, Team
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email', 'first_name', 'last_name')

class UserInformationForm(forms.ModelForm):
    class Meta():
         model = UserInformation
         fields = ('gender', 'dateOfBirth')

class LeagueForm(forms.ModelForm):
    class Meta():
        model = League
        fields = ('leagueName', 'noOfTeams', 'toPublic')

class TeamForm(forms.ModelForm):
    class Meta():
        model = Team
        fields = ('teamName',)

class LeagueTeamForm(forms.Form):
    teamName = forms.CharField( max_length=50)
    userName = forms.CharField( max_length=50)
