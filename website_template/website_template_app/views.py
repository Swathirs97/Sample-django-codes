from django.shortcuts import render

def home(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def menu(request):
    return render(request,"menu.html")

def newsdetail(request):
    return render(request,"news-detail.html")

def news(request):
    return render(request,"news.html")
