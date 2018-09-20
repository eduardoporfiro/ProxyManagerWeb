from django.template import Library
from block.models import Proxy
register = Library()

@register.simple_tag
def load_my_proxy(user):
    return Proxy.objects.filter(user=user)
