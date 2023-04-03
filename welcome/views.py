from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponse
from .forms import chatModelForm, replyModelForm
from .models import chat, replys
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin, ModelFormMixin


def index(request):
    context = {}
    context["name"] = "Hello, World."
    
    return render(request, "temp.html", context)

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
