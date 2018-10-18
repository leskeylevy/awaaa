from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Projects, Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ('name','image','video','link')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('dp', 'bio','contact')


class Comments(forms.ModelForm):
    class Meta:
        fields =['comment']


rating_choices =[
    (1,'1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
]


class Rates(forms.Form):
    design = forms.CharField(label="How awesome is the apps design",widget=forms.RadioSelect(choices=rating_choices))
    usability = forms.CharField(label="How usable is the app", widget=forms.RadioSelect(choices=rating_choices))
    creativity = forms.CharField(label="How creative is the app", widget=forms.RadioSelect(choices=rating_choices))
    content = forms.CharField(label="how awesome is the apps content    ", widget=forms.RadioSelect(choices=rating_choices))