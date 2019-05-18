from django import forms
from django.contrib.auth.models import User
from .models import Profile, SQLCommand
from django.core.exceptions import ValidationError
from sqlparse.exceptions import SQLParseError
import sqlparse

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# Form for new user registration
class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(max_length=12,widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=12, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','first_name','email']

    # konwencja - walidacja dla danego pola to clean_<field>
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


# User forms
class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


# SQL command form
class SQLCommandForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(SQLCommandForm, self).clean()
        command = cleaned_data.get("command")
        if not command:
            raise ValidationError(('%(command) is empty!'), params={'command': command},)
        # Validate command using sqlparse module
        try:
            sqlparse.parse(command)
        except SQLParseError:
            raise ValidationError(_('%(command) is not proper SQL command!'), params={'command': command}, )

    class Meta:
        model = SQLCommand
        fields = ('command',)




