from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
import re
from tasks.forms import StyleFormMixin


class RegisterForm(UserCreationForm):
    class Meta:
        model = User

        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CustomRegistrationForm(StyleFormMixin,forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1','confirm_password']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []
        regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if len(password1) < 8:
            errors.append('password must be atleast 8 charecter long')
        if not re.match(regex, password1):
            raise forms.ValidationError("Password must be at least 8 characters long, contain one uppercase letter, one number, and one special character.")


        if errors:
            raise forms.ValidationError(errors)
        
        return password1
    
    def clean(self):    #non field error
        clean_data = super().clean()
        password1 = clean_data.get('password1')
        confirm_password = clean_data.get('confirm_password')

        if password1 != confirm_password:
            raise forms.ValidationError('password did not match')
        
        return clean_data
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different email.")
        return email


