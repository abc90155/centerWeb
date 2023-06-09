from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from .forms import chatModelForm, replyModelForm, LoginForm,SignUpForm
from .models import chat, replys, Profile
from django.views.generic import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.db.models import Q,F
from .utils import send_signup_email
from django.utils import timezone
from django.core.paginator import Paginator
from sendmail import sendamail
from django.urls import reverse

import secrets



@login_required(login_url='login')
def index(request):
    context = {}
    context["name"] = "Hello, World."
    
    return render(request, "chat_home.html", context)
        
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
                    request.session['user']['type'] = 'User'
                    if request.user.is_staff:
                        request.session['user']['type'] = 'Administrator'
                except Profile.DoesNotExist:
                    messages.info(request,_('Set up your profile'))
                    return redirect('settings')  
                if not request.user.first_name:
                    messages.info(request, _('Set up your profile'))
                    return redirect('settings')
                if request.user.is_staff:
                    return redirect('admin_home')                          
                return redirect('talking')                  
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
            user = form.save(commit=False)
            user.is_active = False  # Set user account as inactive
            user.save()

            # Generate activation token
            token = secrets.token_urlsafe(32)

            # Create and associate profile model with user model
            profile = Profile(user=user, activation_token=token)
            profile.save()


            # Send activation link to user's email
            # activation_link = request.build_absolute_uri(f'/activate/{token}/')
            activation_link = request.build_absolute_uri(reverse('activate', args=[token]))
            message = "Dear user, <br> Thank you for signing up to our service. follow the link belwow to activate your account <br>  <h2> <a href = '{}'>ACTIVATE ACCOUNT</a></h2>".format(activation_link)
            sendamail(content = message, to=user.email)  # Implement your own email sending logic

            messages.warning(request, _('Please check your inbox to continue signup'))
            return redirect('signup')
        else:
            print(form.errors)
            messages.warning(request, form.errors)
    
    context['signupform'] = signup_form
    return render(request, 'signup.html', context)

def activate(request, token):
    try:
        # Find the profile associated with the activation token
        profile = Profile.objects.get(activation_token=token)
        user = profile.user

        # Set the user account to active
        user.is_active = True
        user.save()

        # Delete the activation token from the profile
        profile.activation_token = None
        profile.save()

        messages.success(request, 'Your account has been activated. You can now login.')
        return redirect('login')
    except Profile.DoesNotExist:
        messages.warning(request, 'Invalid activation link.')
        return redirect('signup')

def signupold(request):
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
        
        receiv = chat.objects.filter(Q(id=selected_chat)).values('chatReceiver')
        if self.request.user.id == receiv[0]['chatReceiver']:
            chat.objects.filter(id=selected_chat).update(is_viewed=True, viewedDate=timezone.now())
        
        if str(user) != 'aicenter':
            chats = chat.objects.filter(Q(chatOwner=user) | Q(chatReceiver=user), archived=False).order_by('-createdDate')
        else:
            chats = chat.objects.all().order_by('-createdDate').values()
        context['chatListAll'] = chats.annotate(chatReceiver_username=F('chatReceiver__username')).values()
            
        # Paginate chatListAll
        paginator = Paginator(context['chatListAll'], 10)
        page = self.request.GET.get('page')
        self.request.session['page'] = page
        context['chatListAll'] = paginator.get_page(page) 
        
        form = chatModelForm()

        context['form'] = form

        context['title'] = self.get_object()

        #replys about this topic
        context['replys'] = replys.objects.filter(replyBelongsTo_id = self.kwargs['pk']).all().values()
        
        context['replyForm'] = replyModelForm(initial={'replyBelongsTo': self.get_object(), 'replyerID': self.request.user,})

        return context
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        page = 1
        if self.request.session.get('page'):
            page = self.request.session['page']

        pk = self.kwargs['pk']
        form = replyModelForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            
            selected_chat = self.kwargs['pk']
            receiv = chat.objects.filter(Q(id=selected_chat)).values('chatReceiver')
            mailReceiver = User.objects.filter(Q(id = receiv[0]['chatReceiver'])).values('email')
            sendamail(content = "You have a message from CCH AI platform.", to = mailReceiver[0]['email'])
            
            return HttpResponseRedirect('/welcome/chat/' + str(pk)+'?page='+str(page))
        else:
            print("YOU SHALL NOT PASS!")


@login_required(login_url='login')
def settings(request):
    # Get the profile of the current user or create one if it doesn't exist
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile_dict = {'profile': profile, 'first_name': request.user.first_name, 'last_name': request.user.last_name}
    if request.method == 'POST':
        # Update the profile with the form data
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        request.user.save()

        name = request.user.first_name + ' ' + request.user.last_name
        request.session['user'] = {'name':name}

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

    form = chatModelForm(request.POST or None)
    context['form'] = form
    context['chatListAll'] = chats.annotate(chatReceiver_username=F('chatReceiver__username')).values()
    
    # Paginate chatListAll queryset with 10 items per page
    paginator = Paginator(context['chatListAll'], 10)
    page = request.GET.get('page') # Get current page number from request GET parameters
    if not request.session.get('page'):
        request.session['page'] = page
    context['chatListAll'] = paginator.get_page(page) # Get paginated queryset for current page

    if request.method == "POST":
        if form.is_valid():
            form.instance.chatOwner = request.user
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
    paginator = Paginator(context['chats'], 10)  # Assuming 10 chats per page
    

    # count the messages
    info_chats = chat.objects.filter(is_viewed=True)
    info = {'read_messages':len(info_chats)}
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
    
    context['info'] = info
    return render(request, 'admin_home.html', context=context)
