from django.http import HttpResponse
from django.template import loader
from block.models import Dado

def index(request):
    testes = Dado.objects.filter(user=request.User).all()
    template = loader.get_template('block/index.html')
    context = {
        'testes': testes,
    }
    return HttpResponse(template.render(context, request))
