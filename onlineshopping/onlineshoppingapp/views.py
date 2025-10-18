from django.shortcuts import render
from onlineshoppingapp.models import Product,Category
from onlineshoppingapp.forms import ProductForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def home(request):
    # Fetch all categories
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})


def register(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return HttpResponse("Invalid request ")
    
    form = ProductForm()
    return render(request, 'register.html', {'form': form})

def productlist(request):
    pdt = Product.objects.all()
    return render(request, 'list.html', {'products': pdt})

def category_detail(request, id):
    category = Category.objects.get(id=id)
    return render(request, 'list.html', {'category': category})

def edit_product(request, p_id):
    p=Product.objects.get(id=p_id)
    f=ProductForm(request.POST or None, request.FILES or None, instance=p)
    if f.is_valid():
        f.save()
        return redirect('list')
    return render(request,'register.html',{'form':f})

def delete_product(request, p_id):
    p=Product.objects.get(id=p_id)
    p.delete()
    return redirect('list')

def signup(request):
    if request.method == 'POST':
        u=request.POST['username']
        e=request.POST['email']
        p=request.POST['password']
        f=request.POST['first_name']
        l=request.POST['last_name']
        user=User.objects.create_user(username=u,email=e,password=p,first_name=f,last_name=l)
        user.save()
    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        u=request.POST['username']
        p=request.POST['password']
        user=authenticate(username=u,password=p)
        if user is not None:
            login(request,user)
            f=user.first_name
            l=user.last_name
            return render(request, 'dashboard.html',{'fname':f,'lname':l})
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return redirect('home')