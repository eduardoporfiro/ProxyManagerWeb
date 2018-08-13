from .forms import RegisterForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login

def register(request):
    template_name = 'core/signup.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():#Vê se ta tudo okay
            user = form.save()#salva o usuário
            user = authenticate(
                username=user.username,
                password=form.cleaned_data['password1']
            )#autentica
            login(request, user)#loga ele na sessão e retorna para a página definida no redirect login
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)