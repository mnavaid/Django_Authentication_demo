from django.shortcuts import render, HttpResponseRedirect
#from django.contrib.auth.forms import UserCreationForm # for default inbuilt user creation form
from .forms import signup_form, EditUserProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib.auth.models import User, Group
# Create your views here.

def signup(request):
    if request.method == "POST":
        #frm = UserCreationForm(request.POST) # for defualt usercreation form
        frm = signup_form(request.POST)
        if frm.is_valid():
            user=frm.save()
           # group = Group.objects.get(frm.cleaned_data['group'])
           
            user.groups.add(frm.cleaned_data['group'])
            messages.success(request, 'Account created successfully !!!')
    else:
        #frm = UserCreationForm() # for defualt usercreation form
        frm = signup_form()
    return render (request,  'enroll/signup.html',{'form':frm})

# Login view function
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully !!!')
                    return HttpResponseRedirect('/profile/')
        else:
            fm = AuthenticationForm()
        return render(request, 'enroll/userlogin.html', {'frm':fm})
    else:
        return HttpResponseRedirect('/profile/')

# User profile view function
def user_profile(request):
    if request.user.is_authenticated:
        
        if request.method == 'POST':
            if request.user.is_superuser:
                user_list = User.objects.all()
            else:
                user_list = None
            fm = EditUserProfileForm(request.POST, instance=request.user)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Profile updated successfully !!!')
        else:        
            if request.user.is_superuser:
                user_list = User.objects.all()
            else:
                user_list = None
            fm = EditUserProfileForm(instance=request.user)
        return render(request,'enroll/userprofile.html', {'form':fm, 'users':user_list})
    else:
        return HttpResponseRedirect('/login/')

# User dashboard view function
def user_dashboard(request):
    if request.user.is_authenticated:
         return render(request,'enroll/dashboard.html', {'name':request.user.username})
    else:
        return HttpResponseRedirect('/login/')

# User log out view function
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

# Password change(with old password) view function

def pass_change(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                return HttpResponseRedirect('/profile/')
        else:        
            fm= PasswordChangeForm(user=request.user)
        return render(request, 'enroll/changepass.html',{'fm':fm})
    else:
        return HttpResponseRedirect('/login/')


# Password change(without old password) view function

def pass_set(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            fm = SetPasswordForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                return HttpResponseRedirect('/profile/')
        else:        
            fm= SetPasswordForm(user=request.user)
        return render(request, 'enroll/setpassword.html',{'fm':fm})
    else:
        return HttpResponseRedirect('/login/')