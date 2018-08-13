from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):#Form padrão de criação de user
    email = forms.EmailField(label='E-mail') #quero que coloque o e-mail

    def clean_email(self):#verificação de e-mail
        email = self.cleaned_data['email'] #pego o e-mail
        if User.objects.filter(email=email).exists():#verifico se já existe
            raise forms.ValidationError('Already exists user with this e-mail') #retorno se já existe
        return email


    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']#adicionando o campo e-mail no salvamento
        if commit:
            user.save()
        return user