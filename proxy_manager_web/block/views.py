from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from block.forms import ProxyAdd, ProxyEdit
from block.models import Dado, Broker, Relation

def index(request):
    testes = Dado.objects.filter(user=request.User).all()
    template = loader.get_template('block/index.html')
    context = {
        'testes': testes,
    }
    return HttpResponse(template.render(context, request))

@login_required
def relation (request, slug):
    broker = get_object_or_404(Broker, slug=slug)
    relation, created = Relation.objects.get_or_create(user=request.User, broker=broker)
    return redirect('account.dashboard')

@login_required
def add_proxy(request):
    template_name = 'block/proxy/proxy_add.html'
    if request.method == 'POST':
        form = ProxyAdd(request.POST)
        if form.is_valid():  # Vê se ta tudo okay
            proxy = form.save()  # salva o usuário
            relation = Relation(proxy=proxy, user=request.user)
            relation.save()
            return redirect('core:home')  # loga ele na sessão e retorna para a página definida no redirect login
    else:
        form = ProxyAdd()
    context = {
        'form': form
    }
    return render(request, template_name, context)

@login_required
def edit_proxy(request):
    template_name = 'block/proxy/proxy_edit.html'
    context = {}
    if request.method == 'POST':
        form = ProxyEdit(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Os dados da sua conta foram alterados com sucesso'
            )
            return redirect('accounts:dashboard')
    else:
        form = ProxyEdit(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)