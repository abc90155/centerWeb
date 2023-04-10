from .models import chat, replys, Profile, USER_COMPANY_CHOICES, USER_TYPE_CHOICES
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class chatModelForm(forms.ModelForm):
    class Meta:
        model = chat
        fields = [
            'chatOwner',
            'chatTitle',
            'chatReceiver',
            'chatContent',
        ]

        widgets= {
            'chatOwner': forms.HiddenInput(),#Select(attrs={'class':'form-control'}),
            'chatTitle' : forms.TextInput(attrs={'class': 'form-control'}),
            'chatReceiver' : forms.Select(attrs={'class': 'form-control'}),
            'chatContent' : forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'chatOwner': "提問人",
            'chatTitle' : "標題",
            'chatReceiver' : "收件人",
            'chatContent' : "內容",

        }

class replyModelForm(forms.ModelForm):

    class Meta:
        model = replys
        fields =[
            'replyBelongsTo',
            'replyerID',
            'replyDate',
            'replyContent',
        ] 

        widgets= {
            'replyBelongsTo' : forms.HiddenInput(),
            'replyerID' : forms.HiddenInput(),
            'replyDate' : forms.HiddenInput(),
            'replyContent' : forms.Textarea(attrs={'class':'form-control','placeholder':'Send message', 'rows': 3, 'cols' : 100}),
        }

        labels = {
            'replyBelongsTo' : "主題",
            'replyerID' : "回覆者",
            'replyDate' : "回覆日期",
            'replyContent' : "回覆", 
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['company', 'department', 'workid', 'type']
        labels = {
            'company': 'Company',
            'department': 'Department',
            'workid': 'Work ID',
            'type': 'User Type'
        }
        widgets = {
            'company': forms.Select(choices=USER_COMPANY_CHOICES, attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'workid': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(choices=USER_TYPE_CHOICES, attrs={'class': 'form-control'}),
        }
