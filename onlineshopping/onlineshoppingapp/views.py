from django.shortcuts import render
from onlineshoppingapp.models import Product,Category
from onlineshoppingapp.forms import ProductForm
from django.shortcuts import redirect
from django.http import HttpResponse
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