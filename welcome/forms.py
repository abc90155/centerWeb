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
            'chatOwner': forms.HiddenInput(),
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

    def __init__(self, *args, **kwargs):
        super(chatModelForm, self).__init__(*args, **kwargs)
        # show only the users you want
        self.fields['chatReceiver'].queryset = User.objects.filter(profile__type__in=['htc_user', 'aicenter'])
        

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
            'replyContent' : forms.Textarea(attrs={'id':'replyMessageArea','class':'form-control','placeholder':'Send message', 'rows': 3, 'cols' : 100}),
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
            'company': '公司',
            'department': '部門',
            'workid': '員工編號',
            'type': '部門分類'
        }
        widgets = {
            'company': forms.Select(choices=USER_COMPANY_CHOICES, attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'workid': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(choices=USER_TYPE_CHOICES, attrs={'class': 'form-control'}),
        }
