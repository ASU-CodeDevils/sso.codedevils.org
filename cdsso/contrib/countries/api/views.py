from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from cdsso.contrib.countries.models import Country

from .serializers import CountrySerializer


class CountryViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    lookup_field = "name"
