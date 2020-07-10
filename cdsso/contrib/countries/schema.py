"""Defines the GraphQL schema for custom URLs."""
import graphene
from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from cdsso.contrib.countries.models import Country


class CountryNode(DjangoObjectType):
    """Provides links to all CodeDevils custom URLs."""
    class Meta:
        model = Country
        interfaces = (Node,)
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "native_name": ["exact", "icontains", "istartswith"],
            "alpha2_code": ["exact", "icontains", "istartswith"],
            "alpha3_code": ["exact", "icontains", "istartswith"],
            "numeric_code": ["exact", "icontains", "istartswith"]
        }
        description = "Country and its identifiers"


class Query(object):
    country = graphene.Node.Field(CountryNode)
    countries = DjangoFilterConnectionField(CountryNode)
