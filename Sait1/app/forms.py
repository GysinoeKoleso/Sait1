"""
Definition of forms.
"""

from django.db import models
from.models import Comment
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Blog
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель 
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "КоммеSнтарий"} # метка к полю формы textS