from .models import chat, replys
from django import forms
from django.forms.widgets import NumberInput


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
            'replyerID' : forms.Select(attrs={'class':'form-control'}),#forms.HiddenInput(),
            'replyDate' : forms.HiddenInput(),
            'replyContent' : forms.Textarea(attrs={'class':'form-control','placeholder':'Send message'}),
        }