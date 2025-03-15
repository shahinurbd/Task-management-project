from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import Group,Permission
from django import forms
from django.core.validators import RegexValidator
import re
from tasks.forms import StyleFormMixin
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


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
    

class LoginForm(StyleFormMixin,AuthenticationForm):
    def __init__(self,*arg,**kwargs):
        super().__init__(*arg,**kwargs)



        
class AssignRoleForm(StyleFormMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )


class CreateGroupForm(StyleFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

class CustomPasswordChangeForm(StyleFormMixin,PasswordChangeForm):
    pass


class CustomPasswordResetForm(StyleFormMixin,PasswordResetForm):
    pass


class CustomPasswordResetConfirmForm(StyleFormMixin,SetPasswordForm):
    pass

"""
class EditProfileForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    bio = forms.CharField(required=False, widget=forms.Textarea, label='Bio')
    profile_image = forms.ImageField(required=False, label='Profile Image')

    def __init__(self, *args, **kwargs):
        self.userprofile = kwargs.pop('userprofile', None)
        super().__init__(*args, **kwargs)

        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_image'].initial = self.userprofile.profile_image

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profile_image = self.cleaned_data.get('profile_image')
            if commit:
                self.userprofile.save()

        if commit:
            user.save()
        
        return user

"""

class EditProfileForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'bio', 'profile_image']







