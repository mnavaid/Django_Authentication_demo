from django.forms import fields
from django.contrib.auth import forms
from django.contrib.auth.models import User, Group
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# User signup custome form
class signup_form(UserCreationForm):
    # Since password and password2  are part of UserCreationFor, we need to change the  labels here
    password2 = forms.CharField(label='Re-Password',  widget=forms.PasswordInput)
    # This will show the available groupd in a combobox 
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label='User Group')
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'group']
        # We can change the labels of above field as follows
        labels = {'email':'Email'}

# User edit custom Form
class EditUserProfileForm(UserChangeForm):
    password=None

    class Meta:
        model=User
        fields = ['username','first_name','last_name','email','date_joined', 'last_login']
        # We can change the labels of above field as follows
        labels = {'email':'Email'}

