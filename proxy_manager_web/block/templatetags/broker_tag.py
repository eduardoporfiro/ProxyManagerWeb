from django.template import Library
from block.models import Relation
register = Library()

@register.simple_tag
def load_my_broker(user):
    return Relation.objects.filter(user=user)
