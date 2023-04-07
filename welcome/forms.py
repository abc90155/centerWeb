from .models import chat, replys
from django import forms
from django.forms.widgets import NumberInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class chatModelForm(forms.ModelForm):
    class Meta:
        model = chat
        fields = [
            'chatOwner',
            'chatTitle',
            'createdData',
            'chatReceiver',
            'chatContent',
        ]

        widgets= {
            'chatOwner': forms.Select(attrs={'class':'form-control'}),
            'chatTitle' : forms.TextInput(attrs={'class':'form-control'}),
            'createdData' : forms.DateTimeInput(attrs={'class':'form-control'}),
            'chatReceiver' : forms.TextInput(attrs={'class':'form-control'}),
            'chatContent' : forms.Textarea(attrs={'class':'form-control'}),
        }

        labels = {
            'chatOwner': "提問人",
            'chatTitle' : "標題",
            'createdData' : "建立時間",
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
            'replyContent' : forms.Textarea(attrs={'class':'form-control','placeholder':'Send message', 'rows': 2}),
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