from django.shortcuts import render
from onlineshoppingapp.models import Product,Category
from onlineshoppingapp.forms import ProductForm
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
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

# def signup(request):
#     if request.method == 'POST':
#         u=request.POST['username']
#         e=request.POST['email']
#         p=request.POST['password']
#         f=request.POST['first_name']
#         l=request.POST['last_name']
#         user=User.objects.create_user(username=u,email=e,password=p,first_name=f,last_name=l)
#         user.save()
#     return render(request, 'signup.html')

#importing and using UserCreationForm for signup
def signup(request):
    if request.method == 'POST':
        s = UserCreationForm(request.POST)
        if s.is_valid():
            s.save()
            return redirect('signin')
    else:
        s = UserCreationForm()
            
    return render(request,'signup.html',{'form':s})

# def signin(request):
#     if request.method == 'POST':
#         u=request.POST['username']
#         p=request.POST['password']
#         user=authenticate(username=u,password=p)
#         if user is not None:
#             login(request,user)
#             f=user.first_name
#             l=user.last_name
#             return render(request, 'dashboard.html',{'fname':f,'lname':l})
#         else:
#             return HttpResponse("Invalid credentials")
#     return render(request, 'signin.html')

#importing and using authenticate for signin
def signin(request):
    if request.method == 'POST':
        a = AuthenticationForm(request, data=request.POST)
        if a.is_valid():
            user = a.get_user()
            login(request, user)
            return render(request, 'dashboard.html')
    else:
        a = AuthenticationForm()

    return render(request, 'signin.html', {'form': a})

def signout(request):
    logout(request)
    return redirect('home')

def search(request):
    n=request.POST['n1']
    products=Product.objects.filter(name=n)
    return render(request,'list.html',{'products':products})
