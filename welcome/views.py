from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from .forms import chatModelForm
from .models import chat

def index(request):
    context = {}
    context["name"] = "Hello, World."
    
    return render(request, "temp.html", context)
    #return  HttpResponse("Hello, Django.")

def chatPage(request):
    context = {}
    context = {'name':'cooper'}

    chatList = chat.objects.all().values()

    form = chatModelForm(request.POST or None)
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            form.save()
        
    return render(request, 'chat.html', context)
