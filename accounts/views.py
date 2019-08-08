from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm


# Create your views here.
def index(request):
    return render(request, 'index.html')
    
def logout(request):
    auth.logout(request)
    messages.success(request, "You have logged out, bye!")
    return redirect(reverse('index'))

def login(request):
    
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    
    """This shows the login form"""
    if request.method == 'POST':
        #process the form
        form = UserLoginForm(request.POST)
        
        # if the form contains valid data
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)
            if user is not None:
                auth.login(user=user, request=request)
                messages.success(request, "Welcome back!")
                return redirect(reverse('index'))
            else:
                form.add_error('None', 'Please provide a valid user name and password')
        return render(request, 'login.html', {
            'form':form
        })
    else:
        form = UserLoginForm()
        return render(request, 'login.html', {
            'form' : form
        })

@login_required        
def profile(request):
    return render(request, 'profile.html')
    
def register(request):
    if request.method == "POST":
        # process the form
        form = UserRegistrationForm(request.POST) #create the form object and populate it with the data from the user input
        if form.is_valid():
            pass
        else:
            return render(request, 'register.html',{
                'form':form
            })
    else:
        form = UserRegistrationForm()
        return render(request, 'register.html',{
            'form':form
        })