from django.shortcuts import render,redirect
from product.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from .filters import *


# Create your views here.
def homepage(request):
    user = request.user.id
    product = Product.objects.all().order_by('-id')[:4]
    item = Cart.objects.filter(user=user)
    context = {
        'product':product,
        'items':item
    }
    return render(request, 'users/index.html', context)

def productpage(request):
    user = request.user.id
    product = Product.objects.all().order_by('-id')
    item = Cart.objects.filter(user=user)
    product_filter = ProductFilter(request.GET, queryset=product)
    product_final = product_filter.qs
    context = {
        'product': product_final,
        'product_filter': product_filter,
        'items':item
    }
    return render(request, 'users/products.html', context)

def product_detail(request,product_id):
    user = request.user.id
    product = Product.objects.get(id=product_id)
    item = Cart.objects.filter(user=user)
    context = {
        'product': product,
        'items':item
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

@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)

    check_items_present = Cart.objects.filter(user=user,product=product)
    if check_items_present:
        messages.add_message(request, messages.ERROR, 'Product already added in the cart')
        return redirect('/productpages')
    else:
        cart = Cart.objects.create(product=product,user=user )
        if cart:
            messages.add_message(request, messages.SUCCESS, 'Product added to the cart Successfully')
            return redirect('/cart')
        else:
            messages.add_message(request, messages.ERROR,'Some Error Occured')
            
@login_required
def viewcart(request):
    user = request.user
    items = Cart.objects.filter(user=user)
    context = {
        'items': items
    }
    return render(request,'users/cart.html',context)

@login_required
def deletecart(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    messages.add_message(request, messages.ERROR, 'Item deleted from cart Successfully ')
    return redirect('/cart')

@login_required
def order(request, product_id, cart_id):
    user = request.user
    products = Product.objects.get(id=product_id)
    cart = Cart.objects.get(id=cart_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        product= products
        price = products.product_price
        quantity = request.POST.get('quantity')
        total_price = int(price)*int(price)
        payment_method = request.POST.get('payment_method')
        contact_no = request.POST.get('contact_no')
        address = request.POST.get('address')
         
        order = Order.objects.create(
            product=products,
            user=user,
            quantity=quantity,
            total_price=total_price,
            payment_method=payment_method,
            contact_no=contact_no,
            address=address,
            
        )
        if order.payment_method == 'Cash on Delivery':
            cart.delete()
            messages.add_message(request, messages.SUCCESS, 'Please Provide Cash in Delivery')
            return redirect('/myorder')


    context = {
        'form': OrderForm
    }
    return render(request, 'users/order.html', context)

@login_required
def myorder(request):
    order = Order.objects.all()
    context = {
        'Order': order
    }
    return render(request, 'users/myorder.html', context )
