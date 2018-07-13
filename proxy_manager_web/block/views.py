from django.http import HttpResponse
from django.template import loader
from block.models import Teste

def index(request):
    testes = Teste.objects.all()
    template = loader.get_template('block/index.html')
    context = {
        'testes': testes,
    }
    return HttpResponse(template.render(context, request))
