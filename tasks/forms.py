from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm, \
    SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Task, TaskPhoto


class RegistrationsFrom(UserCreationForm):
    username = forms.CharField(label='Enter Username', min_length=3, max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Enter email', required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = UsernameField(label='Enter Username',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}))
    password = forms.CharField(label='Enter Password', strip=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'current-password'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Enter Email', max_length=254,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}))


class MyPasswordSetForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'new-password'}))


class MyChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', strip=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'current-password', 'autofocus': True}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplete': 'new-password'}))


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'is_complete']


class TaskPhotoForm(forms.ModelForm):
    class Meta:
        model = TaskPhoto
        fields = ['task', 'photo']

    def __init__(self, *args, **kwargs):
        super(TaskPhotoForm, self).__init__(*args, **kwargs)
        # Add a dropdown menu for selecting the task title
        self.fields['task'].widget = forms.Select(attrs={'class': 'form-control'})
