from django import forms
from models import *
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    class Meta:
        model = Register
        widgets = {"passwd":forms.PasswordInput(), "repasswd":forms.PasswordInput()}

    def clean_repasswd(self):
        if "passwd" in self.cleaned_data:
            passwd = self.cleaned_data["passwd"]
            repasswd = self.cleaned_data["repasswd"]
            if passwd == repasswd:
                return repasswd
        raise forms.ValidationError("两次密码输入不一致")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Register.objects.filter(username=username):
            raise forms.ValidationError("该用户名已存在")
        return username
