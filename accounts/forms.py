from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)
    
class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password Confirmation")
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        
    # 'magic function' to clean password2
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 != password2:
            raise ValidationError("Please make sure both passwords are the same")
            
        if not password1 or not password2:
            raise ValidationError("Please enter your password twice")
    
        return password2
        
    def clean_email(self):
        # extract the email from the request
        # (cleaned_data means data that has been processed to remove special characters etc.)
        email = self.cleaned_data.get('email')
        
        # find out if there is any user using that email
        user = User.objects.filter(email=email)
        
        if user.exists() is True:
            raise ValidationError("This email is already in use!")
            
        return email