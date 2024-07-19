from django.shortcuts import render,redirect
from product.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import *


# Create your views here.
def homepage(request):
    product = Product.objects.all().order_by('-id')[:4]
    context = {
        'product':product
    }
    return render(request, 'users/index.html', context)

def productpage(request):
    product = Product.objects.all().order_by('-id')
    context = {
        'product': product
    }
    return render(request, 'users/products.html', context)

def product_detail(request,product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product
    }
    return render(request, 'users/productdetail.html',context)

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'Account created successfully! ')
            return redirect('/register')
        else:
            messages.add_message(request, messages.ERROR, 'kindly verify the fields')
            return render(request, 'users/register.html', {'form':form})
        
    context = {
        'form':UserCreationForm
    }
    return render(request,'users/register.html', context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username = data['username'], password = data['password'])

            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('/ecommerceadmin')
                else:
                    return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Kindly provide correct credentials')
            return render(request, 'users/login.html' , {'form': forms })
        
    context = {
            'form': LoginForm
    }
    return render(request, 'users/login.html',context)
    
def user_logout(request):
    logout(request)
    return redirect('/login')


def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)

    check_items_present = Cart.objects.filter(user=user,product=product)
    if check_items_present:
        messages.add_message(request, messages.ERROR, 'Product alreadu added in the cart')
        return redirect('/productpages')
    else:
        cart = Cart.objects.create(product=product,user=user )
        if cart:
            messages.add_message(request, messages.SUCCESS, 'Product added to the cart Successfully')
            return redirect('/cart')
        else:
            messages.add_message(request, messages.ERROR,'Some Error Occured')
            

def viewcart(request):
    user = request.user
    items = Cart.objects.filter(user=user)
    context = {
        'items': items
    }
    return render(request,'users/cart.html',context)

