import django_filters
from django_filters import DateTimeFromToRangeFilter, ModelChoiceFilter
from django_filters.widgets import RangeWidget
from .models import Dado, Dispositivo


def dispositivo(request):
    dispo_pk = str.split(request.path_info, '/')[3]
    dispos = Dispositivo.objects.get(pk=dispo_pk)
    return Dispositivo.objects.filter(proxy=dispos.proxy.pk, tipo=1).all()


class DadoFilter(django_filters.FilterSet):
    date_range = DateTimeFromToRangeFilter(field_name='date', widget=RangeWidget(
        attrs={'placeholder': 'DD/MM/YYYY hh:mm'}))

    sensor = ModelChoiceFilter(queryset=dispositivo)

    class Meta:
        model = Dado
        fields = ['valor_char', 'valor_int']
