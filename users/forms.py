from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import models

from django import forms

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta(UserCreationForm.Meta):
        # model = get_user_model()
        model = CustomUser

        fields = ('first_name', 'last_name', 'email', 'username')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'username',
        )


class PurchaseForm(forms.Form):
    address = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Your shipping address'}),
    )
    city = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Your city'}),
    )
    state = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Your state'}),
    )
    zipcode = forms.IntegerField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Your city zip code'}),
    )
