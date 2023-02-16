from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Room


class RegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participant', 'created', 'updated']

class UpdateUserProfie(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio', 'image']