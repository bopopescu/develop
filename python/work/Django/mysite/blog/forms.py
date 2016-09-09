#-*- encoding:utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from models import *


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length = 50)
    file = forms.FileField()

class UserForm(forms.ModelForm):
    class Meta:
        model = Register
        widgets = {"password":forms.PasswordInput(), "repassword":forms.PasswordInput()}

        def clean_repassword(self):
            if "password" in self.cleaned_data:
                password = self.cleaned_data["password"]
                repassword = self.cleaned_data["repassword"]
                if password == repassword:
                    return repassword
            raise forms.ValidatinError("两次密码输入不一致")

        def clean_username(self):
            username = self.cleaned_data["username"]
            if Register.objects.filter(username=username):
                raise forms.ValidationError("该用户已存在")
            return username
