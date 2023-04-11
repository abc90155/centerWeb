from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import chatModelForm, replyModelForm, LoginForm,SignUpForm
from .models import chat, replys, Profile
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q,F
from .utils import send_signup_email
from django.utils import timezone
from django.core.paginator import Paginator



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
                request.session['user'] = {
                    'name':name
                }
                try:
                    profile = Profile.objects.get(user=request.user)
                    request.session['user']['type'] = 'test'
                except Profile.DoesNotExist:
                    messages.info(request,_('Set up your profile'))
                    return redirect('settings')  
                if request.user.is_staff:
                    return redirect('admin_home')                          
                return redirect('chat')                  
            else:
                messages.error(request, _("Username and password does not match."))
                return redirect('login')
        else:
            return render(request, 'login.html',{'form':form})

def signup(request):
    if request.user.is_authenticated:
        return redirect('welcome')
    context = {"test":'tested'}
    signup_form = SignUpForm()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                send_signup_email(user.email)
            except TimeoutError:
                # messages.warning(request, _('Sorry, the email confirmation message could not be sent. Please try again later.'))
                return redirect('login')
            send_signup_email(user.email)
            messages.warning(request, _('Please check your inbox to continue signup'))
            return redirect('signup')
        else:
            print(form.errors)
            messages.warning(request, form.errors)
    
    context['signupform'] = signup_form
    return render(request, 'signup.html', context)


@login_required(login_url='login')
def chatPage(request):
    userNow = str(request.user)
    if str(request.user) != 'admin':
        chatList = chat.objects.filter(Q(chatOwner = request.user) | Q(chatReceiver = request.user)).all().order_by('-createdDate').values()
    else:
        chatList = chat.objects.all().order_by('-createdDate').values()
    
    #todo : add a initial value
    form = chatModelForm(request.POST or None)
    
    context = {"form": form,
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
        user = self.request.user
        selected_chat = self.kwargs['pk']
        chat.objects.filter(id=selected_chat).update(is_viewed=True, viewedDate=timezone.now())


        if str(self.request.user) != 'admin':
            # context['chatListAll'] = chat.objects.filter(Q(chatOwner = self.request.user) | Q(chatReceiver = self.request.user)).all().order_by('-createdDate').values()
            context['chatListAll'] = chat.objects.filter(Q(chatOwner=user) | Q(chatReceiver=user), archived=False).order_by('-createdDate')

        else:
            context['chatListAll'] = chat.objects.all().order_by('-createdDate').values()

        # Paginate chatListAll queryset with 10 items per page
        paginator = Paginator(context['chatListAll'], 5)
        page = self.request.GET.get('page')
        context['chatListAll'] = paginator.get_page(page) # Get paginated queryset for current page
        
        form = chatModelForm()

        context['form'] = form

        context['title'] = self.get_object()

        #replys about this topic
        context['replys'] = replys.objects.filter(replyBelongsTo_id = self.kwargs['pk']).all().values()

        context['replyForm'] = replyModelForm(initial={'replyBelongsTo': self.get_object(), 'replyerID': self.request.user,})

        return context
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = replyModelForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect('/welcome/chat/' + str(pk))
        else:
            print("YOU SHALL NOT PASS!")


@login_required(login_url='login')
def settings(request):
    # Get the profile of the current user or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_dict = {'profile': profile, 'first_name': request.user.first_name, 'last_name': request.user.last_name}
    if request.method == 'POST':
        # Update the profile with the form data
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        request.user.save()

        profile.company = request.POST['company']
        profile.workid = request.POST['work_id']
        profile.department = request.POST['department']
        # profile.type = 'request.POST['user_type']'
        profile.user.save()
        profile.save()
        messages.success(request, 'Profile updated successfully.')

        # Redirect the user back to the settings page
        return redirect('settings')

    # Render the settings.html template with the profile as context
    return render(request, 'settings.html', profile_dict)
    
@login_required(login_url='login')
def talking(request):
    context = {}
    user = request.user

    if str(request.user) != 'admin':
        # chats = chat.objects.filter(Q(chatOwner = user) | Q(chatReceiver = user)).all().order_by('-createdDate').values()
        chats = chat.objects.filter(Q(chatOwner=user) | Q(chatReceiver=user), archived=False).order_by('-createdDate')
    else:
        chats = chat.objects.filter(archived=False).order_by('-createdDate').values()

    form = chatModelForm(request.POST or None, initial={'chatOwner': user,})
    context['form'] = form
    context['chatListAll'] = chats.annotate(chatReceiver_username=F('chatReceiver__username')).values()
    print(context['chatListAll'])
    # Paginate chatListAll queryset with 10 items per page
    paginator = Paginator(context['chatListAll'], 10)
    page = request.GET.get('page') # Get current page number from request GET parameters
    context['chatListAll'] = paginator.get_page(page) # Get paginated queryset for current page
    # print('kkkkkkkkkkkk',context['chatListAll'])

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/welcome/talking')
    
    return render(request, 'chat_home.html', context=context)

def delete_chat(request):
    if request.method == 'POST':
        # Get the list of IDs of the selected chats
        selected_ids = request.POST.getlist('selected_chats')      
        # Archive the selected chats
        chat.objects.filter(id__in=selected_ids).update(archived=True)
        
        # Redirect back to the same page
        return redirect('talking')
    

@login_required(login_url='login')
def admin_home(request):
    context = {}
    user = request.user
    
    # Get the chats that belong to the logged-in user and are not archived
    chats = chat.objects.filter(archived=False).order_by('-createdDate').values()
    context['chats'] = chats.annotate(chatReceiver_username=F('chatReceiver__username')).values()
    
    # Get the current page number from the request's GET parameters
    page = request.GET.get('page', 1)
    
    # Create a Paginator object with the chats queryset and the desired number of items per page
    paginator = Paginator(context['chats'], 5)  # Assuming 10 chats per page
    
    # Get the Page object for the current page
    page_obj = paginator.get_page(page)
    
    context['chats'] = page_obj
    
    if request.method == 'POST':
        # Get the list of IDs of the selected chats
        selected_ids = request.POST.getlist('selected_chats')
        
        # Archive the selected chats
        chat.objects.filter(id__in=selected_ids).update(archived=True)
        
        # Redirect back to the same page
        return redirect(request.META.get('HTTP_REFERER'))
    
    return render(request, 'admin_home.html', context=context)
