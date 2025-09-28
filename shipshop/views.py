from django.shortcuts import HttpResponse, redirect, render
from store.models import Product 
def home(request):
    products = Product.objects.all().filter(is_available = True)
    
    context = {
        'products': products
    }
    return render(request, "home.html", context=context)

def search(request):
    pass

def login(request):
    pass

def register(request):
    pass

def cart(request):
    pass


# def store(request):
#     pass