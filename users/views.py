from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Register new user"""
    if request.method != 'POST':
        #Empty registration form
        form = UserCreationForm()
    else:
        #Processing filled form
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            #Log in user, redirect to home page
            login(request, new_user)
            return redirect('learnify_app:index')
    #View empty form
    context = {'form': form}
    return render(request, 'registration/register.html', context)
