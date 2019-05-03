from django import forms
from django.contrib.auth.models import User


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



