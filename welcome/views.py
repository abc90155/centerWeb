from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from .forms import chatModelForm
from .models import chat

def index(request):
    context = {}
    context["name"] = "Hello, World."
    
    return render(request, "temp.html", context)

def chatPage(request):
    context = {}

    chatList = chat.objects.all().values()

    form = chatModelForm(request.POST or None)
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            form.save()
    elif request.is_ajax:
        "todo: ajax to load chat content"
        return render(request, 'chat.html', context)
    else:
        context = {"form": form,
                    "name":'YOOOOOOOO~Cooper',
                    "chatListAll":chatList,
                    }
        
    return render(request, 'chat.html', context)
