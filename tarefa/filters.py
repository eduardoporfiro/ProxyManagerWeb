import django_filters
from django_filters import DateTimeFromToRangeFilter
from django_filters.widgets import RangeWidget
from .models import Dado, Dispositivo


class DadoFilter(django_filters.FilterSet):
    date_range = DateTimeFromToRangeFilter(field_name='date', widget=RangeWidget(
        attrs={'placeholder': 'DD/MM/YYYY hh:mm'}))

    class Meta:
        model = Dado
        fields = ['sensor', 'valor_char', 'valor_int']

    @property
    def qs(self):
        dado = super(DadoFilter, self).qs
        dispo_pk = str.split(self.request.path_info, '/')[3]
        dispos = Dispositivo.objects.get(pk=dispo_pk)
        dispos = Dispositivo.objects.filter(proxy=dispos.proxy.pk).all()
        return dado.filter(sensor__in=dispos)
