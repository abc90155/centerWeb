from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from .forms import chatModelForm, replyModelForm, LoginForm
from .models import chat, replys
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def index(request):
    context = {}
    context["name"] = "Hello, World."
    
    return render(request, "temp.html", context)
        
def logout_view(request):
    logout(request)
    return redirect('login')

def login_user(request):
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect('chat')
    else:
        if request.method =='POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                name = request.user.first_name + ' ' + request.user.last_name
                request.session['name'] = name  
                return redirect('chat')                  
            else:
                messages.error(request, _("Username and password does not match."))
                return redirect('login')
            print('hereeeeeeeeeeeeeeee',user)
        else:
            return render(request, 'login.html',{'form':form})
    
@login_required(login_url='login')
def chatPage(request):
    chatList = chat.objects.all().values()
    form = chatModelForm(request.POST or None)

    context = {"form": form,
                "name":'YOOOOOOOO~Cooper',
                "chatListAll":chatList,
                }

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/welcome/chat')
    return render(request, 'chat.html', context)

# 留言檢視
class chatDetail(DetailView):
    model = chat
    template_name = 'chatDetail.html'
    replys = replyModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #todo: add a filter to login user in the future
        context['chatListAll'] = chat.objects.all().values()

        #replys about this topic
        context['replys'] = replys.objects.filter(replyBelongsTo_id = self.kwargs['pk']).all().values()

        #need to modify afetr add user model; 
        context['replyForm'] = replyModelForm(initial={'replyBelongsTo': self.get_object(),}) # 'replyerID': 'abc90155'})
        
        return context
    @login_required(login_url='login')
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = replyModelForm(request.POST or None)

        print("<<<<<<<<<<<<<<<<<<")
        print(form)
        print("<<<<<<<<<<<<<<<<<<<")
        
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect('/welcome/chat/' + str(pk))
        else:
            print("YOU SHALL NOT PASS!")
