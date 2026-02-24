from django.shortcuts import render
from .forms import RegistrationForm

# Create your views here.

def register(request):
    form = RegistrationForm()
    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context=context)

def login(request):
    return render(request, "accounts/login.html")
    pass

def logout(request):
    return
    # return render(request, "accounts/logout.html")
    # pass